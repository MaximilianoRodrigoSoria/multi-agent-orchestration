"""Executor: PROPONE la acción (no la ejecuta hasta que se apruebe)."""

from __future__ import annotations

from multi_agent_orchestration.config import get_settings
from multi_agent_orchestration.state import TicketState


def propose(state: TicketState) -> TicketState:
    body = (
        f"Hola, sobre '{state.ticket.get('subject', '')}': {state.findings} "
        "Quedamos atentos."
    )
    action_type = "send_reply"
    state.proposed_action = {
        "type": action_type,
        "critical": action_type in get_settings().critical_actions,
        "payload": {"to": state.ticket.get("from", "cliente"), "body": body},
    }
    state.log(f"executor: propone {action_type} (crítica={state.proposed_action['critical']})")
    return state
