"""Acciones del caso de negocio (triage de tickets)."""

from __future__ import annotations

PRIORITY_KEYWORDS = {
    "urgent": {"caído", "urgente", "no funciona", "producción", "bloqueado"},
    "billing": {"factura", "cobro", "reembolso", "pago"},
}


def classify(ticket: dict) -> dict:
    """Clasifica un ticket en categoría y prioridad (heurística, sin LLM)."""
    text = f"{ticket.get('subject', '')} {ticket.get('body', '')}".lower()
    priority = "high" if any(k in text for k in PRIORITY_KEYWORDS["urgent"]) else "normal"
    category = "billing" if any(k in text for k in PRIORITY_KEYWORDS["billing"]) else "support"
    return {"category": category, "priority": priority}


def send_reply(payload: dict) -> str:
    """Acción CRÍTICA: enviaría la respuesta al cliente. Aquí solo la simula."""
    to = payload.get("to", "cliente")
    return f"Respuesta enviada a {to} ({len(payload.get('body', ''))} chars)."
