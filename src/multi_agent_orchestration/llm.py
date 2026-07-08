"""Factory del LLM conmutable (Ollama local / Claude).

Los agentes reciben el LLM ya construido (inyección de dependencias), lo que
permite mockearlo en los tests sin tocar red ni API.
"""

from __future__ import annotations

from typing import Protocol


class ChatLLM(Protocol):
    """Contrato mínimo que usan los agentes: un `.invoke(prompt)`."""

    def invoke(self, prompt: str) -> object: ...


def get_chat_llm(settings) -> ChatLLM:
    """Devuelve el chat model según el proveedor configurado (imports diferidos)."""
    if settings.llm_provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=0.0,
        )
    from langchain_anthropic import ChatAnthropic

    # Nota: los modelos Claude 5+ deprecaron `temperature`; no se envía.
    return ChatAnthropic(
        model=settings.llm_model,
        api_key=settings.anthropic_api_key,
        max_tokens=settings.llm_max_tokens,
    )


def llm_text(llm: ChatLLM, prompt: str) -> str:
    """Llama al LLM y devuelve texto plano, tolerante al tipo de retorno."""
    resp = llm.invoke(prompt)
    content = getattr(resp, "content", resp)
    return str(content).strip()
