"""Human-in-the-loop: gate de aprobación antes de acciones críticas.

`request_approval` recibe una función de entrada inyectable, así en la CLI usa
`input()` y en los tests se le pasa una función que simula la decisión.
"""

from __future__ import annotations

from collections.abc import Callable

VALID = {"approve", "reject", "edit"}


def requires_approval(action: dict | None) -> bool:
    return bool(action and action.get("critical"))


def request_approval(action: dict, input_fn: Callable[[str], str] = input) -> str:
    """Devuelve 'approve' | 'reject' | 'edit'. Reintenta ante entradas inválidas."""
    prompt = (
        f"\nAcción propuesta: {action['type']}\n"
        f"Payload: {action.get('payload')}\n"
        "¿Aprobar? [approve/reject/edit]: "
    )
    for _ in range(3):
        choice = (input_fn(prompt) or "").strip().lower()
        if choice in VALID:
            return choice
    return "reject"
