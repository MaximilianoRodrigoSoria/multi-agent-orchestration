"""Lógica pura del gate human-in-the-loop.

Se mantiene separada del grafo para poder testearla sin LangGraph: dada una
decisión humana, devuelve el update de estado correspondiente.
"""

from __future__ import annotations

from ..state import TicketState

VALID_DECISIONS = ("approve", "edit", "reject")


def apply_decision(
    state: TicketState, decision: str, edited_reply: str | None = None
) -> dict:
    """Traduce la decisión humana en un update de estado.

    - ``approve``: usa el borrador tal cual como respuesta final.
    - ``edit``: usa el texto editado (requiere ``edited_reply``).
    - ``reject``: no se envía nada; la respuesta final queda vacía.

    Lanza ``ValueError`` si la decisión es inválida o falta el texto editado.
    """
    decision = (decision or "").strip().lower()
    if decision not in VALID_DECISIONS:
        raise ValueError(f"Decisión inválida: {decision!r} (esperado {VALID_DECISIONS})")

    if decision == "approve":
        return {"decision": "approve", "final_reply": state.get("draft_reply", "")}

    if decision == "edit":
        if not edited_reply or not edited_reply.strip():
            raise ValueError("La decisión 'edit' requiere un texto editado no vacío.")
        return {"decision": "edit", "final_reply": edited_reply.strip()}

    # reject
    return {"decision": "reject", "final_reply": ""}
