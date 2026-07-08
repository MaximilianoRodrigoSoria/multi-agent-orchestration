"""Configuración del sistema multi-agente."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Proveedor de LLM para los agentes (seam; hoy la lógica corre heurística).
    llm_provider: str = Field(default="none", alias="LLM_PROVIDER")
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    # Acciones consideradas críticas → pasan por aprobación humana.
    critical_actions: tuple[str, ...] = ("send_reply", "close_ticket", "refund")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
