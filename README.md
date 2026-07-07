# multi-agent-orchestration

Sistema **multi-agente** con orquestación explícita y un paso de **human-in-the-loop (HITL)**: antes de ejecutar cualquier acción crítica (enviar un correo, cerrar un ticket, escribir en un sistema externo), el flujo se detiene y espera aprobación humana.

## Objetivo

Demostrar diseño de sistemas agénticos serios, no un demo de "un agente que llama tools". El foco está en tres cosas que separan un juguete de un sistema productivo:

1. **Orquestación con roles claros** — varios agentes especializados (planner, investigador, ejecutor, crítico) coordinados por un grafo de estados, no un loop opaco.
2. **Human-in-the-loop** — las acciones con efectos secundarios reales pasan por un gate de aprobación; el estado se persiste y el flujo puede reanudarse.
3. **Caso de negocio concreto** — aplicado a **triage de tickets de soporte** (clasificar, priorizar, proponer respuesta, y solo enviar tras aprobación) o, como alternativa, **investigación web automatizada** (planificar, buscar, sintetizar, y solo publicar tras aprobación).

## Stack tecnológico sugerido

- **Lenguaje:** Python 3.11+
- **Framework de orquestación:** LangGraph (recomendado por su soporte nativo de `interrupt`/checkpointing para HITL) — alternativas: CrewAI, AutoGen
- **LLM:** OpenAI / Anthropic (con function/tool calling)
- **Persistencia de estado:** checkpointer de LangGraph sobre SQLite/Postgres (para pausar y reanudar en el gate humano)
- **Herramientas de los agentes:** consumir el `mcp-server-demo` de este portfolio y/o el RAG de `rag-pipeline-eval`; búsqueda web vía Tavily/SerpAPI para el caso de investigación
- **Interfaz de aprobación:** CLI interactiva para empezar; opción de UI mínima con Streamlit o FastAPI + un endpoint `/approve`
- **Testing / calidad:** pytest, ruff, black

## Estructura de carpetas propuesta

```
multi-agent-orchestration/
├── README.md
├── pyproject.toml
├── .env.example
├── src/
│   ├── config.py
│   ├── state.py             # Definición del estado compartido del grafo
│   ├── graph.py             # Construcción del grafo de orquestación
│   ├── agents/
│   │   ├── planner.py       # Descompone el objetivo en pasos
│   │   ├── researcher.py    # Recupera/investiga (RAG, web, MCP tools)
│   │   ├── executor.py      # Propone/ejecuta acciones (tras aprobación)
│   │   └── critic.py        # Valida y refina el output
│   ├── tools/
│   │   ├── ticket_tools.py  # Acciones del caso de negocio
│   │   └── web_tools.py     # Búsqueda web (alternativa)
│   ├── hitl/
│   │   └── approval.py      # Gate de aprobación humana + reanudación
│   └── app/
│       └── cli.py           # Punto de entrada interactivo
├── examples/
│   └── sample_tickets.jsonl # Datos de ejemplo del caso de negocio
├── docs/
│   └── flow.md              # Diagrama del flujo (Mermaid) y roles
└── tests/
    ├── test_graph.py
    └── test_approval.py
```

## Diagrama de flujo (referencia)

```mermaid
flowchart TD
    A[Entrada: ticket / objetivo] --> B[Planner: descompone en pasos]
    B --> C[Researcher: recupera contexto (RAG / web / MCP)]
    C --> D[Executor: PROPONE acción crítica]
    D --> E{Human-in-the-loop:\naprobación requerida?}
    E -- No / acción segura --> G[Critic: valida output]
    E -- Sí --> F[[Pausa: espera aprobación humana]]
    F -- Aprueba --> H[Ejecuta acción real]
    F -- Rechaza / edita --> B
    H --> G
    G --> I[Resultado final + traza]
```

## Checklist de implementación

### Fase 1 — Diseño

- [ ] Elegir el caso de negocio (triage de tickets **o** investigación web) y documentarlo.
- [ ] Definir los roles de cada agente y el contrato de entrada/salida entre ellos.
- [ ] Definir `state.py`: qué información viaja por el grafo (objetivo, pasos, hallazgos, acción propuesta, decisión humana).

### Fase 2 — Agentes y herramientas

- [ ] Implementar el `planner` (descomposición del objetivo en pasos accionables).
- [ ] Implementar el `researcher` conectado a una fuente real (RAG del portfolio, web, o herramientas MCP).
- [ ] Implementar el `executor` que **propone** acciones y las marca como críticas/seguras.
- [ ] Implementar el `critic` para validar y refinar antes de cerrar.
- [ ] Implementar las tools del caso de negocio en `tools/`.

### Fase 3 — Orquestación

- [ ] Construir el grafo en `graph.py` conectando los agentes.
- [ ] Configurar el checkpointer (SQLite/Postgres) para persistir estado.

### Fase 4 — Human-in-the-loop (el diferenciador)

- [ ] Implementar el `interrupt`/pausa antes de toda acción crítica.
- [ ] Mostrar al humano la acción propuesta con contexto suficiente para decidir.
- [ ] Soportar tres decisiones: **aprobar**, **rechazar** y **editar/reencaminar**.
- [ ] Verificar que el flujo **reanuda** correctamente desde el estado persistido tras la aprobación.

### Fase 5 — Interfaz y robustez

- [ ] CLI interactiva que muestre el progreso y el gate de aprobación.
- [ ] Manejo de errores y reintentos por agente; timeouts en llamadas a tools.
- [ ] Trazabilidad: registrar cada decisión (agente, tool, aprobación) para auditoría.

### Fase 6 — Documentación

- [ ] `docs/flow.md` con el diagrama Mermaid y la descripción de roles.
- [ ] README con cómo correr el caso de ejemplo y ver el gate humano en acción.
- [ ] ADR breve: por qué orquestación explícita (grafo) frente a un loop autónomo.

## Criterios de "terminado"

El sistema procesa un caso del negocio de punta a punta, **se detiene ante una acción crítica esperando aprobación humana**, y reanuda correctamente según la decisión (aprobar/rechazar/editar). Todo el recorrido queda trazado.
