"""Executor: redacta la respuesta PROPUESTA al cliente.

Ojo: el executor no envía nada. Solo prepara el borrador. El envío (la acción
con efecto real) ocurre después del gate human-in-the-loop, en el nodo `send`.
"""

from __future__ import annotations

from ..llm import ChatLLM, llm_text
from ..state import TicketState

_PROMPT = """Sos un agente de soporte al cliente. Redactá una respuesta breve,
cordial y accionable al ticket, apoyándote en el contexto provisto.

Asunto: {subject}
Cuerpo: {body}
Contexto disponible:
{context}

Escribí solo la respuesta (máximo 5 líneas, tono profesional y claro):"""


def make_executor(llm: ChatLLM):
    """Devuelve el nodo `executor` con el LLM inyectado."""

    def executor_node(state: TicketState) -> dict:
        context = "\n".join(f"- {c}" for c in state.get("context", [])) or "- (sin contexto)"
        draft = llm_text(
            llm,
            _PROMPT.format(
                subject=state.get("subject", ""),
                body=state.get("body", ""),
                context=context,
            ),
        )
        return {
            "draft_reply": draft,
            "decision": "",
            "history": state.get("history", []) + ["executor: borrador de respuesta listo"],
        }

    return executor_node
