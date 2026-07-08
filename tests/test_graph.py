"""Tests del grafo de orquestación con el gate HITL (LangGraph + LLM mockeado).

Corren 100% offline: LangGraph orquesta en local y el LLM se reemplaza por un
`FakeLLM` que devuelve respuestas fijas, así no hace falta API ni red.
"""

from __future__ import annotations

from multi_agent_orchestration.graph import build_graph
from multi_agent_orchestration.hitl.approval import apply_decision


class _Resp:
    def __init__(self, content: str):
        self.content = content


class FakeLLM:
    """LLM falso: clasifica si el prompt es del planner; si no, devuelve un borrador."""

    def invoke(self, prompt: str) -> _Resp:
        low = prompt.lower()
        if "categoria" in low or "clasific" in low:
            return _Resp("categoria: tecnico\nprioridad: alta")
        return _Resp("Hola, probá cerrar sesión y volver a entrar. Si sigue, avisanos. Saludos.")


def _initial():
    return {
        "ticket_id": "T-1",
        "subject": "No puedo entrar",
        "body": "Error de login desde ayer",
        "history": [],
    }


def _config(thread_id: str = "t1"):
    return {"configurable": {"thread_id": thread_id}}


def test_pausa_en_el_gate_de_aprobacion():
    app = build_graph(FakeLLM())
    cfg = _config("pausa")
    app.invoke(_initial(), cfg)

    snap = app.get_state(cfg)
    # El grafo quedó detenido justo antes del nodo de aprobación.
    assert snap.next == ("approval",)
    # Y ya clasificó y redactó el borrador, pero NO envió.
    assert snap.values["category"] == "tecnico"
    assert snap.values["priority"] == "alta"
    assert snap.values["draft_reply"]
    assert not snap.values.get("sent")


def test_aprobar_envia_la_respuesta():
    app = build_graph(FakeLLM())
    cfg = _config("aprueba")
    app.invoke(_initial(), cfg)
    snap = app.get_state(cfg)

    app.update_state(cfg, apply_decision(snap.values, "approve"))
    final = app.invoke(None, cfg)

    assert final["sent"] is True
    assert final["final_reply"] == snap.values["draft_reply"]
    assert final["critique"] == "OK"


def test_editar_envia_el_texto_corregido():
    app = build_graph(FakeLLM())
    cfg = _config("edita")
    app.invoke(_initial(), cfg)
    snap = app.get_state(cfg)

    nuevo = "Respuesta revisada por un humano, más clara y completa."
    app.update_state(cfg, apply_decision(snap.values, "edit", nuevo))
    final = app.invoke(None, cfg)

    assert final["sent"] is True
    assert final["final_reply"] == nuevo


def test_rechazar_no_envia():
    app = build_graph(FakeLLM())
    cfg = _config("rechaza")
    app.invoke(_initial(), cfg)
    snap = app.get_state(cfg)

    app.update_state(cfg, apply_decision(snap.values, "reject"))
    final = app.invoke(None, cfg)

    assert final["sent"] is False
    assert final["final_reply"] == ""
    # El critic deja constancia de que no se envió.
    assert "no se envió" in final["critique"]
