"""Orquestador (plain Python) con el gate human-in-the-loop.

Corre sin dependencias pesadas para poder testear el flujo y la reanudación. La
versión con LangGraph vive en `graph.py` (usa el mismo estado y agentes).
"""

from __future__ import annotations

from collections.abc import Callable

from multi_agent_orchestration.agents.critic import review
from multi_agent_orchestration.agents.executor import propose
from multi_agent_orchestration.agents.planner import plan
from multi_agent_orchestration.agents.researcher import research
from multi_agent_orchestration.hitl.approval import request_approval, requires_approval
from multi_agent_orchestration.state import TicketState
from multi_agent_orchestration.tools.ticket_tools import send_reply


def run(ticket: dict, approve_fn: Callable[[dict], str], retriever=None) -> TicketState:
    """Procesa un ticket de punta a punta. `approve_fn(action) -> decisión`."""
    state = TicketState(ticket=dict(ticket))
    plan(state)
    research(state, retriever=retriever)
    propose(state)

    ok, reason = review(state)
    if not ok:
        state.result = f"rechazado por el crítico: {reason}"
        state.log(state.result)
        return state

    action = state.proposed_action
    if requires_approval(action):
        state.decision = approve_fn(action)
        state.log(f"hitl: decisión={state.decision}")
        if state.decision != "approve":
            state.result = f"acción NO ejecutada (decisión: {state.decision})"
            state.log(state.result)
            return state

    state.result = send_reply(action["payload"])
    state.log(f"ejecutada: {state.result}")
    return state


def run_interactive(ticket: dict, retriever=None) -> TicketState:
    return run(ticket, approve_fn=lambda a: request_approval(a), retriever=retriever)
