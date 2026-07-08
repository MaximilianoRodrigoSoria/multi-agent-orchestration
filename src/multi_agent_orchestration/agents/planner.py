"""Planner: clasifica el ticket (categoría + prioridad) y arma el plan de pasos.

Usa el LLM para clasificar, con parseo tolerante y fallback por reglas para no
romper si el modelo no respeta el formato.
"""

from __future__ import annotations

from ..llm import ChatLLM, llm_text
from ..state import TicketState

CATEGORIES = ("facturacion", "tecnico", "cuenta", "otro")
PRIORITIES = ("baja", "media", "alta")

_PROMPT = """Sos un clasificador de tickets de soporte. Clasificá el siguiente ticket.

Asunto: {subject}
Cuerpo: {body}

Respondé EXACTAMENTE en dos líneas, sin nada más:
categoria: <facturacion|tecnico|cuenta|otro>
prioridad: <baja|media|alta>"""


def _extract(text: str, key: str, options: tuple[str, ...], default: str) -> str:
    """Busca `key: valor` en el texto; si no, busca cualquier opción; si no, default."""
    for line in text.splitlines():
        low = line.lower()
        if low.strip().startswith(key):
            for opt in options:
                if opt in low:
                    return opt
    low_all = text.lower()
    for opt in options:
        if opt in low_all:
            return opt
    return default


def make_planner(llm: ChatLLM):
    """Devuelve el nodo `planner` con el LLM inyectado."""

    def planner_node(state: TicketState) -> dict:
        raw = llm_text(
            llm,
            _PROMPT.format(subject=state.get("subject", ""), body=state.get("body", "")),
        )
        category = _extract(raw, "categoria", CATEGORIES, "otro")
        priority = _extract(raw, "prioridad", PRIORITIES, "media")
        plan = [
            f"Clasificar el ticket (→ {category}, prioridad {priority})",
            "Recuperar contexto relevante de la base de conocimiento",
            "Redactar una respuesta propuesta",
            "Solicitar aprobación humana antes de enviar",
            "Enviar la respuesta y validar el resultado",
        ]
        return {
            "category": category,
            "priority": priority,
            "plan": plan,
            "history": state.get("history", []) + [f"planner: {category}/{priority}"],
        }

    return planner_node
