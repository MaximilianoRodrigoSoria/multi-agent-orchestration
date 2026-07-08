"""Estado compartido que viaja por el grafo de orquestación."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TicketState:
    ticket: dict
    steps: list[str] = field(default_factory=list)
    findings: str = ""
    proposed_action: dict | None = None  # {"type", "critical", "payload"}
    decision: str | None = None          # "approve" | "reject" | "edit"
    result: str | None = None
    trace: list[str] = field(default_factory=list)

    def log(self, msg: str) -> None:
        self.trace.append(msg)
