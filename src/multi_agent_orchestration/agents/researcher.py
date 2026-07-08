"""Researcher: recupera contexto relevante para el ticket.

Acá usa una base de conocimiento simple por categoría (determinística, sin LLM
ni red). En un sistema real, este nodo consultaría el RAG de `rag-pipeline-eval`
o un MCP server para traer artículos de ayuda, tickets similares, etc.
"""

from __future__ import annotations

from ..state import TicketState

_KB: dict[str, list[str]] = {
    "facturacion": [
        "Política de facturación: los cargos se emiten el día 1 de cada mes.",
        "Reembolsos: se procesan en 5 a 7 días hábiles a la forma de pago original.",
    ],
    "tecnico": [
        "Cerrar sesión y volver a entrar resuelve la mayoría de los errores de login.",
        "Estado del servicio en tiempo real: status.tuempresa.com",
    ],
    "cuenta": [
        "El cambio de email requiere verificación en dos pasos.",
        "El enlace de recuperación de cuenta es válido por 24 horas.",
    ],
    "otro": [
        "Si el caso no encaja en una categoría, derivar a un agente humano.",
    ],
}


def make_researcher(_llm=None):
    """Devuelve el nodo `researcher`. El LLM no se usa acá (KB determinística)."""

    def researcher_node(state: TicketState) -> dict:
        category = state.get("category", "otro")
        context = _KB.get(category, _KB["otro"])
        return {
            "context": context,
            "history": state.get("history", []) + [f"researcher: {len(context)} docs de '{category}'"],
        }

    return researcher_node
