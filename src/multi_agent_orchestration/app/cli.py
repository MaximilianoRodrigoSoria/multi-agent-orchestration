"""CLI interactiva: corre los tickets de ejemplo con gate humano real."""

from __future__ import annotations

import json
from pathlib import Path

from multi_agent_orchestration.orchestrator import run_interactive

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    sample = ROOT / "examples" / "sample_tickets.jsonl"
    for line in sample.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        ticket = json.loads(line)
        print(f"\n=== Ticket #{ticket.get('id')} — {ticket.get('subject')} ===")
        state = run_interactive(ticket)
        print("Resultado:", state.result)
        print("Traza:", " | ".join(state.trace))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
