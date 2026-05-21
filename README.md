# Enterprise Agent Framework

> Production-grade multi-agent orchestration system built on LangGraph — deployable on Kubernetes.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-latest-purple.svg)](https://langchain-ai.github.io/langgraph/)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://docker.com)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-deployed-326ce5.svg)](https://kubernetes.io)

## Overview

Most AI agent demos break in production — state is lost, errors cascade, and scaling is an afterthought. This framework moves beyond prototype agents toward a **resilient, stateful, scalable orchestration system** that can handle complex multi-agent workflows in enterprise environments.

## Architecture

Three-phase pipeline with independent, swappable agents at each stage:

```
┌──────────────────────────────────────────────────────┐
│  Phase 1: Triage                                     │
│  Analyzer Agent → Intent Classifier Agent            │
└────────────────────┬─────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────┐
│  Phase 2: Reasoning & Execution                      │
│  Semantic Searcher → Code Executor → Human Gate      │
└────────────────────┬─────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────┐
│  Phase 3: Delivery                                   │
│  QA Validator → Response Synthesizer                 │
└──────────────────────────────────────────────────────┘
```

## Key Features

- **LangGraph state machine** — cyclical workflows with conditional branching and error recovery
- **Pluggable vector DB** — swap between Pinecone, Chroma, and Milvus via config, no code changes
- **Persistent memory** — tool-calling history and reasoning logs survive restarts
- **Human-in-the-loop gate** — configurable approval checkpoint before execution
- **FastAPI REST interface** — submit tasks, poll status, retrieve results
- **Kubernetes-ready** — Helm chart included for horizontal scaling

## Quick Start

```bash
git clone https://github.com/Alan-911/enterprise-agent-framework
cd enterprise-agent-framework

# Local (Docker Compose)
cp .env.example .env   # add your API keys
docker compose up

# Kubernetes
helm install eaf ./helm --values values.yaml

# API
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"task": "Summarize Q3 sales report and flag anomalies", "context": "..."}'
```

## Configuration

```yaml
# config.yaml
vector_db: pinecone          # pinecone | chroma | milvus
llm_provider: openai         # openai | anthropic
memory_backend: redis
human_gate_enabled: true
max_agent_iterations: 10
```

## Repo Structure

```
├── agents/           # Individual agent implementations
├── data/             # Data ingestion and chunking utilities
├── monitoring/       # Prometheus metrics, logging
├── ui/               # React dashboard for task monitoring
├── helm/             # Kubernetes Helm chart
├── main.py           # Application entrypoint
├── dashboard.py      # Monitoring dashboard
└── execute.sh        # Deployment helper
```

## Stack

`Python` `LangGraph` `LangChain` `FastAPI` `Docker` `Kubernetes` `Pinecone` `Chroma` `Milvus` `Redis` `React`

---

Built by [Yves Alain Iragena](https://alan-911.github.io/my-portfolio) | MAIL Lab, Catholic University of America
