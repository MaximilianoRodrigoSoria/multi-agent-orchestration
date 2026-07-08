"""Herramientas del caso de triage de tickets.

`send_reply` es la ACCIÓN CRÍTICA del flujo: en producción dispararía el envío
real (API de email / helpdesk). Por eso solo se ejecuta después de que un humano
aprobó en el gate. Acá se simula y se devuelve un recibo.
"""

from __future__ import annotations


def send_reply(ticket_id: str, reply: str) -> dict:
    """Simula el envío de la respuesta al cliente y devuelve un recibo.

    En un sistema real, acá iría la llamada a la API del helpdesk. Se mantiene
    sin side-effects para que sea seguro de correr en cualquier entorno.
    """
    return {
        "ticket_id": ticket_id,
        "status": "sent",
        "chars": len(reply or ""),
    }
