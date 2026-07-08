"""CLI interactiva del sistema multi-agente con gate human-in-the-loop.

Corre el grafo sobre un ticket, se detiene en el gate de aprobación, muestra el
borrador propuesto y pide la decisión humana (aprobar / editar / rechazar).
Recién tras la aprobación se ejecuta la acción crítica (enviar).

Uso:
    set PYTHONPATH=src
    python -m multi_agent_orchestration.app.cli --ticket-id T-1001
    python -m multi_agent_orchestration.app.cli --auto-approve   # demo no interactiva
"""

from __future__ import annotations

import argparse
import json
import uuid
from pathlib import Path

from ..config import ROOT_DIR, get_settings
from ..graph import build_graph
from ..hitl.approval import apply_decision
from ..llm import get_chat_llm


def _load_ticket(path: Path, ticket_id: str | None) -> dict:
    """Carga un ticket del JSONL (el primero, o el que matchee `ticket_id`)."""
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if ticket_id is None or row.get("ticket_id") == ticket_id:
                return row
    raise SystemExit(f"Ticket no encontrado: {ticket_id}")


def _ask_decision() -> tuple[str, str | None]:
    """Pregunta la decisión humana por consola."""
    raw = input("\n¿Qué hacemos? [a]probar / [e]ditar / [r]echazar: ").strip().lower()
    decision = {"a": "approve", "e": "edit", "r": "reject"}.get(raw, "reject")
    edited = None
    if decision == "edit":
        edited = input("Escribí la respuesta corregida: ").strip()
    return decision, edited


def main() -> int:
    parser = argparse.ArgumentParser(description="Triage de tickets multi-agente (HITL).")
    parser.add_argument("--tickets", default="examples/sample_tickets.jsonl")
    parser.add_argument("--ticket-id", default=None, help="ID del ticket a procesar.")
    parser.add_argument(
        "--auto-approve",
        action="store_true",
        help="Aprobar automáticamente, sin preguntar (demo no interactiva).",
    )
    args = parser.parse_args()

    settings = get_settings()
    llm = get_chat_llm(settings)
    app = build_graph(llm)

    tickets_path = Path(args.tickets)
    if not tickets_path.is_absolute():
        tickets_path = ROOT_DIR / tickets_path
    ticket = _load_ticket(tickets_path, args.ticket_id)

    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    app.invoke(
        {
            "ticket_id": ticket["ticket_id"],
            "subject": ticket["subject"],
            "body": ticket["body"],
            "history": [],
        },
        config,
    )

    # El grafo se pausó ANTES de 'approval'. Leemos el estado actual.
    snapshot = app.get_state(config)
    state = snapshot.values
    print("\n" + "=" * 60)
    print(f"Ticket {state['ticket_id']}: {state['subject']}")
    print(f"Clasificación: {state.get('category')} · prioridad {state.get('priority')}")
    print("-" * 60)
    print("Respuesta PROPUESTA (aún no enviada):\n")
    print(state.get("draft_reply", "(vacío)"))
    print("=" * 60)

    if args.auto_approve or settings.auto_approve:
        decision, edited = "approve", None
        print("\n[AUTO_APPROVE] Aprobando automáticamente.")
    else:
        decision, edited = _ask_decision()

    app.update_state(config, apply_decision(state, decision, edited))
    final = app.invoke(None, config)

    print("\n" + "=" * 60)
    print(f"Decisión: {decision.upper()} · Enviado: {final.get('sent')}")
    if final.get("sent"):
        print(f"Respuesta final:\n{final.get('final_reply')}")
    print(f"Crítica: {final.get('critique')}")
    print("-" * 60)
    print("Traza de agentes:")
    for step in final.get("history", []):
        print(f"  · {step}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
