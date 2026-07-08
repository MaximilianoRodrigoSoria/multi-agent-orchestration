"""Tests del gate human-in-the-loop (lógica pura, sin LangGraph ni LLM)."""

from __future__ import annotations

import pytest

from multi_agent_orchestration.hitl.approval import apply_decision


def test_approve_usa_el_borrador():
    update = apply_decision({"draft_reply": "Hola, ya lo resolvemos."}, "approve")
    assert update["decision"] == "approve"
    assert update["final_reply"] == "Hola, ya lo resolvemos."


def test_edit_usa_el_texto_editado():
    update = apply_decision({"draft_reply": "borrador"}, "edit", "  texto corregido  ")
    assert update["decision"] == "edit"
    assert update["final_reply"] == "texto corregido"


def test_edit_sin_texto_falla():
    with pytest.raises(ValueError):
        apply_decision({"draft_reply": "x"}, "edit")


def test_edit_texto_vacio_falla():
    with pytest.raises(ValueError):
        apply_decision({"draft_reply": "x"}, "edit", "   ")


def test_reject_no_deja_respuesta():
    update = apply_decision({"draft_reply": "x"}, "reject")
    assert update["decision"] == "reject"
    assert update["final_reply"] == ""


def test_decision_invalida_falla():
    with pytest.raises(ValueError):
        apply_decision({}, "quiza")


def test_decision_normaliza_mayusculas_y_espacios():
    update = apply_decision({"draft_reply": "ok"}, "  APPROVE ")
    assert update["decision"] == "approve"
