from __future__ import annotations

from multi_agent_orchestration.orchestrator import run

TICKET = {"id": 1, "from": "ana@example.com", "subject": "No funciona el login", "body": "urgente"}


def test_flujo_aprobado_ejecuta():
    state = run(TICKET, approve_fn=lambda a: "approve")
    assert "enviada" in (state.result or "")
    assert state.decision == "approve"
    assert state.trace  # dejó traza


def test_flujo_rechazado_no_ejecuta():
    state = run(TICKET, approve_fn=lambda a: "reject")
    assert "NO ejecutada" in (state.result or "")


def test_accion_critica_pasa_por_gate():
    seen = {}
    def approve(action):
        seen["critical"] = action["critical"]
        return "approve"
    run(TICKET, approve_fn=approve)
    assert seen["critical"] is True
