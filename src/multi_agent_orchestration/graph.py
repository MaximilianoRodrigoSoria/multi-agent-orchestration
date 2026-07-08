"""Construcción del grafo de orquestación con gate human-in-the-loop.

Flujo:  planner → researcher → executor → [PAUSA: approval] → send/rejected → critic

El gate se implementa con `interrupt_before=["approval"]`: el grafo se detiene
ANTES del nodo de aprobación y persiste su estado en el checkpointer. Un humano
setea la decisión (`app.update_state(...)`) y el grafo se reanuda con
`app.invoke(None, config)`.
"""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from .agents.critic import make_critic
from .agents.executor import make_executor
from .agents.planner import make_planner
from .agents.researcher import make_researcher
from .state import TicketState
from .tools.ticket_tools import send_reply


def _approval_node(state: TicketState) -> dict:
    """Nodo de aprobación. No hace nada por sí mismo: el grafo se pausa ANTES
    (interrupt_before) para que un humano fije `decision`/`final_reply`."""
    return {}


def _route_after_approval(state: TicketState) -> str:
    """Enruta según la decisión humana: aprobar/editar → enviar; rechazar → no."""
    return "send" if state.get("decision") in ("approve", "edit") else "rejected"


def _send_node(state: TicketState) -> dict:
    receipt = send_reply(state.get("ticket_id", ""), state.get("final_reply", ""))
    return {
        "sent": receipt["status"] == "sent",
        "history": state.get("history", []) + [f"send: {receipt['status']} ({receipt['chars']} chars)"],
    }


def _rejected_node(state: TicketState) -> dict:
    return {
        "sent": False,
        "history": state.get("history", []) + ["rejected: la respuesta no se envió"],
    }


def build_graph(llm, checkpointer=None):
    """Arma y compila el grafo. `llm` se inyecta a los agentes (mockeable).

    Si no se pasa checkpointer, usa un `MemorySaver` en memoria (necesario para
    que funcione el interrupt/reanudación).
    """
    graph = StateGraph(TicketState)
    graph.add_node("planner", make_planner(llm))
    graph.add_node("researcher", make_researcher(llm))
    graph.add_node("executor", make_executor(llm))
    graph.add_node("approval", _approval_node)
    graph.add_node("send", _send_node)
    graph.add_node("rejected", _rejected_node)
    graph.add_node("critic", make_critic(llm))

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "executor")
    graph.add_edge("executor", "approval")
    graph.add_conditional_edges(
        "approval",
        _route_after_approval,
        {"send": "send", "rejected": "rejected"},
    )
    graph.add_edge("send", "critic")
    graph.add_edge("rejected", "critic")
    graph.add_edge("critic", END)

    if checkpointer is None:
        from langgraph.checkpoint.memory import MemorySaver

        checkpointer = MemorySaver()

    return graph.compile(checkpointer=checkpointer, interrupt_before=["approval"])
