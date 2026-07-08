from __future__ import annotations

from multi_agent_orchestration.hitl.approval import request_approval, requires_approval


def test_requires_approval():
    assert requires_approval({"critical": True})
    assert not requires_approval({"critical": False})
    assert not requires_approval(None)


def test_request_approval_valida_y_reintenta():
    respuestas = iter(["quizas", "APPROVE"])
    assert request_approval({"type": "send_reply", "payload": {}}, lambda p: next(respuestas)) == "approve"


def test_request_approval_invalida_termina_en_reject():
    assert request_approval({"type": "x", "payload": {}}, lambda p: "nope") == "reject"
