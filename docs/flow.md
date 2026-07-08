# Flujo de orquestación

```mermaid
flowchart TD
    A[Ticket] --> B[Planner: clasifica y arma pasos]
    B --> C[Researcher: recupera contexto (seam RAG/web)]
    C --> D[Executor: PROPONE respuesta]
    D --> E[Critic: valida]
    E -->|inválida| X[Rechazo: no se ejecuta]
    E -->|válida y crítica| F[[HITL: espera aprobación]]
    E -->|válida y segura| H[Ejecuta acción]
    F -->|approve| H
    F -->|reject/edit| X
    H --> Z[Resultado + traza]
```

Roles: **planner** (descompone), **researcher** (recupera), **executor**
(propone), **critic** (valida). El gate **human-in-the-loop** se dispara para
acciones marcadas como críticas en la config (`send_reply`, `close_ticket`,
`refund`).
