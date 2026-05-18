# Enterprise Agent Framework (EAF) 🏢🤖

A state-of-the-art orchestration layer for production AI systems, combining **LangGraph**, **multi-modal RAG**, and **long-term memory** for enterprise-scale autonomous agents.

---

## 🌟 Vision
Most AI agents are prototypes. EAF is built to be a resilient, scalable system that companies can deploy to handle complex, stateful multi-agent workflows with human-in-the-loop (HITL) capabilities.

---

## ✨ Key Features
- **LangGraph Orchestration**: Complex state management for cyclical and multi-agent workflows.
- **Unified RAG Stack**: Pluggable vector database support (Pinecone, Chroma, Milvus).
- **Tool-Calling Memory**: Persistent storage for tool results and agent reasoning steps.
- **FastAPI Core**: Enterprise-grade REST interface for frontend/mobile integration.

---

## 🏗️ Architecture

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    "primaryColor": "#14A800",
    "primaryTextColor": "#FFFFFF",
    "primaryBorderColor": "#108A00",
    "lineColor": "#3C8224",
    "secondaryColor": "#E1F0DA",
    "tertiaryColor": "#F2F7F2",
    "background": "#FFFFFF",
    "mainBkg": "#FFFFFF",
    "nodeBorder": "#108A00",
    "clusterBkg": "#F2F7F2",
    "clusterBorder": "#14A800",
    "titleColor": "#001E00",
    "edgeLabelBackground": "#FFFFFF",
    "fontFamily": "Segoe UI, sans-serif"
  }
}}%%
flowchart TD

    classDef core fill:#14A800,stroke:#108A00,color:#FFF,stroke-width:2px
    classDef agent fill:#3C8224,stroke:#2E6B1B,color:#FFF,stroke-width:2px
    classDef memory fill:#E1F0DA,stroke:#3C8224,color:#001E00,stroke-width:2px
    classDef orchestrator fill:#001E00,stroke:#14A800,color:#FFF,stroke-width:3px
    classDef external fill:#FFFFFF,stroke:#14A800,color:#001E00,stroke-width:2px

    EXT[/"Enterprise Data Sources\n(APIs, DBs, Documents)"/]
    ORCH(["ORCHESTRATOR\nDynamic State Router"])

    subgraph INTAKE["PHASE 1 · DATA INGESTION & TRIAGE"]
        direction TB
        DA["Agent 1\nData Analyzer"]
        IC["Agent 2\nIntent Classifier"]
    end

    subgraph LOGIC["PHASE 2 · REASONING & EXECUTION"]
        direction TB
        SA["Agent 3\nSemantic Searcher"]
        CA["Agent 4\nCode/Task Executor"]
        VA(["Human-in-the-loop\nApproval Gate"])
    end

    subgraph OUTPUT["PHASE 3 · DELIVERY & SYNTHESIS"]
        direction TB
        QA["Agent 5\nQA & Validation"]
        SYN["Agent 6\nResponse Synthesizer"]
        DEL[/"Client / End-User Application"/]
    end

    subgraph MEMORY["MEMORY & RAG STACK"]
        direction LR
        VDB[("Vector DB\nPinecone / Milvus")]
        LTM["Long-Term\nInteraction Memory"]
    end

    EXT --> DA
    DA --> IC
    IC -->|"Task Definition"| ORCH

    ORCH -->|"Retrieval Required"| SA
    ORCH -->|"Execution Required"| CA
    
    SA <--> VDB
    CA <--> LTM

    CA -->|"High-Risk Action"| VA
    VA -->|"Approved"| QA
    SA --> QA

    QA --> SYN
    SYN --> DEL
```

## 🚀 Proposal: Building AI-Augmented Applications

The traditional approach to software relies on static APIs and rigid conditional logic. This framework serves as a strategic proposal and architectural foundation for the next generation of **AI-Augmented Enterprise Applications**. 

By transitioning to an agentic architecture, businesses can:
1. **Reduce Overhead**: Automate complex, multi-step reasoning tasks that traditionally require human intervention.
2. **Increase Accuracy**: Utilize specialized agent roles (e.g., Semantic Searchers, Code Executors, QA Validation) to cross-check outputs before delivery.
3. **Maintain Safety**: Integrate strict Human-in-the-Loop (HITL) approval gates for high-risk operations while allowing autonomous execution for low-risk tasks.

### Core Implementation Strategy
- **Orchestrator Node**: Acts as the central brain, dynamically routing context between specialized agents rather than relying on linear scripts.
- **Unified Memory Stack**: Combines Vector Databases for semantic RAG with Long-Term Memory nodes to retain conversational context across sessions.
- **Decoupled Architecture**: Designed to be integrated directly into existing infrastructure via FastAPI, cleanly separating the AI logic from the frontend presentation.
