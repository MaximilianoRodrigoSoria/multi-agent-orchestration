"""Critic: valida el output final y deja una nota de calidad.

Validación por reglas (determinística, sin LLM) para que la traza sea
reproducible y los tests corran offline. Se puede enriquecer con el LLM.
"""

from __future__ import annotations

from ..state import TicketState


def make_critic(_llm=None):
    """Devuelve el nodo `critic`. Valida por reglas simples."""

    def critic_node(state: TicketState) -> dict:
        reply = (state.get("final_reply") or state.get("draft_reply") or "").strip()
        issues: list[str] = []

        if not state.get("sent"):
            issues.append("no se envió respuesta (rechazado o pendiente)")
        if len(reply) < 20:
            issues.append("respuesta demasiado corta")
        if state.get("priority") == "alta" and not reply:
            issues.append("prioridad alta sin respuesta")

        critique = "OK" if not issues else "; ".join(issues)
        return {
            "critique": critique,
            "history": state.get("history", []) + [f"critic: {critique}"],
        }

    return critic_node
