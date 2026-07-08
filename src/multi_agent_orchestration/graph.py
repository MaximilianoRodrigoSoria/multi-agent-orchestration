"""Wiring con LangGraph (import diferido/guardado).

Reproduce el flujo del orquestador como un StateGraph con `interrupt` antes de la
acción crítica, para poder pausar/reanudar con un checkpointer. Requiere langgraph
(grupo opcional 'graph' del pyproject).
"""

from __future__ import annotations

from multi_agent_orchestration.agents.executor import propose
from multi_agent_orchestration.agents.planner import plan
from multi_agent_orchestration.agents.researcher import research
from multi_agent_orchestration.state import TicketState


def build_graph(checkpointer=None):
    """Construye el grafo. Import de langgraph diferido para no exigirlo al importar."""
    from langgraph.graph import END, StateGraph

    g = StateGraph(TicketState)
    g.add_node("planner", plan)
    g.add_node("researcher", research)
    g.add_node("executor", propose)
    g.set_entry_point("planner")
    g.add_edge("planner", "researcher")
    g.add_edge("researcher", "executor")
    g.add_edge("executor", END)
    # El gate HITL se implementa con interrupt_before=["executor"] al compilar,
    # de modo que el flujo se detenga a esperar aprobación.
    return g.compile(checkpointer=checkpointer, interrupt_before=["executor"])
