"""Estado compartido del grafo de orquestación.

Es el "pizarrón" que todos los agentes leen y escriben mientras el ticket
avanza por el grafo. LangGraph fusiona los updates parciales que devuelve
cada nodo sobre este estado.
"""

from __future__ import annotations

from typing import Literal, TypedDict

Category = Literal["facturacion", "tecnico", "cuenta", "otro"]
Priority = Literal["baja", "media", "alta"]
Decision = Literal["approve", "edit", "reject", ""]


class TicketState(TypedDict, total=False):
    """Estado del flujo de triage de un ticket."""

    # Entrada
    ticket_id: str
    subject: str
    body: str

    # Producido por el planner
    category: Category
    priority: Priority
    plan: list[str]

    # Producido por el researcher
    context: list[str]

    # Producido por el executor (acción propuesta, aún sin enviar)
    draft_reply: str

    # Gate human-in-the-loop
    decision: Decision
    final_reply: str

    # Resultado
    sent: bool
    critique: str

    # Traza acumulada de qué hizo cada agente
    history: list[str]
