"""Critic: valida la acción propuesta antes de darla por buena."""

from __future__ import annotations

from multi_agent_orchestration.state import TicketState


def review(state: TicketState) -> tuple[bool, str]:
    action = state.proposed_action or {}
    body = action.get("payload", {}).get("body", "")
    if len(body.strip()) < 20:
        return False, "respuesta demasiado corta"
    return True, "ok"
