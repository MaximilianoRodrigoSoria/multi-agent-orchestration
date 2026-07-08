"""Researcher: recupera contexto. Seam para enchufar el RAG / búsqueda web."""

from __future__ import annotations

from multi_agent_orchestration.state import TicketState


def research(state: TicketState, retriever=None) -> TicketState:
    """Si se inyecta un `retriever` (p. ej. el RAG del portfolio), se usa; si no,
    deja una nota. Mantener el seam evita acoplar el agente a una fuente."""
    query = state.ticket.get("subject", "")
    if retriever is not None:
        state.findings = str(retriever(query))
    else:
        state.findings = f"(sin retriever) contexto base para: {query!r}"
    state.log("researcher: contexto recuperado")
    return state
