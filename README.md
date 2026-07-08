<p align="center">
<a href="https://www.linkedin.com/in/soriamaximilianorodrigo/" target="_blank" rel="noopener noreferrer">
<img width="100%" height="100%" src="docs/img/banner.gif" alt="multi-agent-orchestration"></a>
</p>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white" alt="Python"></a>
  <a href="#"><img src="https://img.shields.io/badge/Orquestaci%C3%B3n-LangGraph-14B8A6" alt="LangGraph"></a>
  <a href="#"><img src="https://img.shields.io/badge/Human--in--the--loop-si-1DE9B6" alt="HITL"></a>
  <a href="#"><img src="https://img.shields.io/badge/LLM-OpenAI_%7C_Anthropic-22D3EE" alt="LLM"></a>
</p>

<p align="center">
  <a href="https://github.com/DietrichGebert/ponytail"><img src="https://img.shields.io/badge/built_with-ponytail-111111?style=flat-square" alt="ponytail"></a>
  <img src="https://img.shields.io/badge/layout-src%2Fpackage-14B8A6?style=flat-square" alt="src layout">
  <img src="https://img.shields.io/badge/license-MIT-success?style=flat-square" alt="MIT">
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=1DE9B6&center=true&vCenter=true&width=820&lines=Orquestaci%C3%B3n+multi-agente+con+human-in-the-loop;planner+%C2%B7+researcher+%C2%B7+executor+%C2%B7+critic;LangGraph+%2B+aprobaci%C3%B3n+antes+de+acciones+cr%C3%ADticas" alt="typing SVG">
</p>

<hr/>

<h1 align="center">multi-agent-orchestration</h1>

<p align="center">
Sistema <b>multi-agente</b> con orquestación y un paso de <b>human-in-the-loop</b>:
antes de ejecutar una acción crítica, el flujo se detiene y espera aprobación humana.
</p>

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

## Criterios de "terminado"

El sistema procesa un caso del negocio de punta a punta, **se detiene ante una acción crítica esperando aprobación humana**, y reanuda correctamente según la decisión (aprobar/rechazar/editar). Todo el recorrido queda trazado.
