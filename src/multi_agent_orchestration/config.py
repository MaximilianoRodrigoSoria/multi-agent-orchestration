"""Configuración central del sistema multi-agente.

Todas las settings se leen desde variables de entorno (o un archivo `.env`)
mediante pydantic-settings. Ver `.env.example` para la lista completa.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Raíz del proyecto (…/multi-agent-orchestration)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Settings tipadas. Se instancian una sola vez (ver `get_settings`)."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    # --- Proveedor de LLM de los agentes ---
    llm_provider: Literal["anthropic", "ollama"] = Field(
        default="ollama", alias="LLM_PROVIDER"
    )

    # --- Claude / Anthropic ---
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    llm_model: str = Field(default="claude-sonnet-5", alias="LLM_MODEL")
    llm_max_tokens: int = Field(default=1024, alias="LLM_MAX_TOKENS")

    # --- Ollama (local) ---
    ollama_model: str = Field(default="llama3.1:8b", alias="OLLAMA_MODEL")
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")

    # --- Gate human-in-the-loop ---
    auto_approve: bool = Field(default=False, alias="AUTO_APPROVE")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Devuelve la instancia única de settings (cacheada)."""
    return Settings()
