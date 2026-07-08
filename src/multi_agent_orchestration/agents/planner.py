"""Planner: descompone el objetivo del ticket en pasos accionables."""

from __future__ import annotations

from multi_agent_orchestration.state import TicketState
from multi_agent_orchestration.tools.ticket_tools import classify


def plan(state: TicketState) -> TicketState:
    meta = classify(state.ticket)
    state.ticket.update(meta)
    state.steps = [
        "clasificar ticket",
        "recuperar contexto relevante",
        "redactar respuesta propuesta",
        "validar y (si es crítico) pedir aprobación",
    ]
    state.log(f"planner: categoría={meta['category']} prioridad={meta['priority']}")
    return state
