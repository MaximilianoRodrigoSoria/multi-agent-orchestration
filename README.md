<p align="center">
<a href="https://www.linkedin.com/in/soriamaximilianorodrigo/" target="_blank" rel="noopener noreferrer">
<img width="100%" height="100%" src="docs/img/banner.gif" alt="multi-agent-orchestration"></a>
</p>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white&style=flat-square" alt="Python"></a>
  <a href="#"><img src="https://img.shields.io/badge/Orquestaci%C3%B3n-LangGraph-14B8A6?style=flat-square" alt="LangGraph"></a>
  <a href="#"><img src="https://img.shields.io/badge/Human--in--the--loop-si-1DE9B6?style=flat-square" alt="HITL"></a>
  <a href="#"><img src="https://img.shields.io/badge/LLM-OpenAI_%7C_Anthropic-22D3EE?style=flat-square" alt="LLM"></a>
</p>

<p align="center">
  <a href="https://github.com/DietrichGebert/ponytail"><img src="https://img.shields.io/badge/built_with-ponytail-111111?style=flat-square" alt="ponytail"></a>
  <img src="https://img.shields.io/badge/layout-src%2Fpackage-14B8A6?style=flat-square" alt="src layout">
  <img src="https://img.shields.io/badge/license-MIT-success?style=flat-square" alt="MIT">
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=1DE9B6&center=true&vCenter=true&width=820&lines=Orquestaci%C3%B3n+multi-agente+con+human-in-the-loop;planner+%C2%B7+researcher+%C2%B7+executor+%C2%B7+critic;LangGraph+%2B+aprobaci%C3%B3n+antes+de+acciones+cr%C3%ADticas" alt="typing SVG">
</p>

<!-- dynamic-badges -->
<p align="center">
  <a href="https://github.com/MaximilianoRodrigoSoria/multi-agent-orchestration/actions"><img src="https://img.shields.io/github/actions/workflow/status/MaximilianoRodrigoSoria/multi-agent-orchestration/ci.yml?style=flat-square&logo=githubactions&logoColor=white&label=CI&labelColor=1A1C1F&color=06C69C" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/MaximilianoRodrigoSoria/multi-agent-orchestration?style=flat-square&labelColor=1A1C1F&color=06C69C" alt="License"></a>
  <img src="https://img.shields.io/github/last-commit/MaximilianoRodrigoSoria/multi-agent-orchestration?style=flat-square&labelColor=1A1C1F&color=06C69C" alt="Last commit">
  <img src="https://img.shields.io/github/repo-size/MaximilianoRodrigoSoria/multi-agent-orchestration?style=flat-square&labelColor=1A1C1F&color=06C69C" alt="Repo size">
  <a href="https://maximilianorodrigosoria.github.io/multi-agent-orchestration/"><img src="https://img.shields.io/badge/GitHub_Pages-online-02ECB6?style=flat-square&logo=githubpages&logoColor=white&labelColor=1A1C1F" alt="Pages"></a>
  <img src="https://img.shields.io/badge/Python-3.12-06C69C?style=flat-square&logo=python&logoColor=white&labelColor=1A1C1F" alt="Python">
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

## Stack tecnológico

- **Lenguaje:** Python 3.11+
- **Framework de orquestación:** LangGraph (recomendado por su soporte nativo de `interrupt`/checkpointing para HITL) — alternativas: CrewAI, AutoGen
- **LLM:** OpenAI / Anthropic (con function/tool calling)
- **Persistencia de estado:** checkpointer de LangGraph sobre SQLite/Postgres (para pausar y reanudar en el gate humano)
- **Herramientas de los agentes:** consumir el `mcp-server-demo` de este portfolio y/o el RAG de `rag-pipeline-eval`; búsqueda web vía Tavily/SerpAPI para el caso de investigación
- **Interfaz de aprobación:** CLI interactiva para empezar; opción de UI mínima con Streamlit o FastAPI + un endpoint `/approve`
- **Testing / calidad:** pytest, ruff, black

## Estructura de carpetas

```
multi-agent-orchestration/
├── README.md
├── AGENTS.md                        # Ruleset ponytail (código mínimo)
├── pyproject.toml
├── .env.example
├── src/
│   └── multi_agent_orchestration/   # Paquete importable (src layout)
│       ├── config.py               # Settings (pydantic-settings)
│       ├── state.py                # TicketState: estado compartido del grafo
│       ├── llm.py                  # LLM conmutable (Ollama/Claude) + inyección
│       ├── graph.py                # Grafo LangGraph + interrupt_before (HITL)
│       ├── agents/
│       │   ├── planner.py          # Clasifica el ticket y arma el plan
│       │   ├── researcher.py       # Recupera contexto (KB; extensible a RAG/MCP)
│       │   ├── executor.py         # Redacta la respuesta PROPUESTA (no envía)
│       │   └── critic.py           # Valida el output final
│       ├── tools/
│       │   └── ticket_tools.py     # Acción crítica: enviar la respuesta
│       ├── hitl/
│       │   └── approval.py         # Lógica del gate (aplica la decisión humana)
│       └── app/
│           └── cli.py              # CLI interactiva (punto de entrada)
├── examples/
│   └── sample_tickets.jsonl        # Tickets de ejemplo
├── docs/
│   └── flow.md                     # Diagrama del flujo (Mermaid) y roles
└── tests/                          # Offline, con LLM mockeado
    ├── test_graph.py               # Grafo + gate HITL (LangGraph real)
    └── test_approval.py            # Lógica de decisión humana
```

## Diagrama de flujo (referencia)

```mermaid
flowchart TD
    A[Entrada: ticket] --> B[Planner: clasifica y arma el plan]
    B --> C[Researcher: recupera contexto de la KB]
    C --> D[Executor: PROPONE la respuesta]
    D --> E{Aprobacion humana requerida}
    E -- aprobar / editar --> H[Send: ejecuta la accion real]
    E -- rechazar --> X[No se envia]
    H --> G[Critic: valida el output]
    X --> G
    G --> I[Resultado final + traza]
```

## Puesta en marcha

Stack: **LangGraph** (orquestación + `interrupt` para HITL) con LLM conmutable
(**Ollama** local o **Claude**). Los agentes reciben el LLM inyectado, así los
tests corren offline con un mock.

### 1. Instalar dependencias

```bash
# Con Poetry
poetry install --with dev,local   # + local habilita Ollama

# o con pip (sin Poetry)
python -m pip install --user -r requirements-all.txt
```

### 2. Configurar el entorno

```bash
cp .env.example .env
# Elegir LLM_PROVIDER (ollama/anthropic); si es Claude, completar ANTHROPIC_API_KEY.
```

### 3. Correr el triage (con gate humano)

Si usás Ollama local, levantá el servidor con Docker (la primera vez, para bajar el modelo):

```bash
docker compose up -d ollama
docker compose --profile pull up ollama-pull   # descarga OLLAMA_MODEL una sola vez
```

Después corré el flujo:

```bash
set PYTHONPATH=src
python -m multi_agent_orchestration.app.cli --ticket-id T-1001
```

El flujo se detiene, muestra la respuesta **propuesta** y espera tu decisión:
aprobar, editar o rechazar. Recién si aprobás se ejecuta la acción crítica (enviar).
Para una demo no interactiva:

```bash
python -m multi_agent_orchestration.app.cli --ticket-id T-1001 --auto-approve
```

### 4. Tests (offline, sin API ni red)

```bash
poetry run pytest          # o:  set PYTHONPATH=src  &&  python -m pytest
```

Los tests usan un `FakeLLM` y ejercitan el grafo real de LangGraph, incluyendo
la pausa en el gate y las tres decisiones (aprobar / editar / rechazar).

