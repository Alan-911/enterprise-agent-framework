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

    classDef p1agent fill:#14A800,stroke:#108A00,color:#FFF,stroke-width:2px
    classDef p2agent fill:#3C8224,stroke:#2E6B1B,color:#FFF,stroke-width:2px
    classDef p3agent fill:#E1F0DA,stroke:#3C8224,color:#001E00,stroke-width:2px
    classDef orchestrator fill:#001E00,stroke:#14A800,color:#FFF,stroke-width:3px
    classDef humangate fill:#F2F7F2,stroke:#3C8224,color:#001E00,stroke-width:2px
    classDef memnode fill:#C8E6BE,stroke:#3C8224,color:#001E00,stroke-width:2px
    classDef external fill:#FFFFFF,stroke:#14A800,color:#001E00,stroke-width:2px
    classDef success fill:#D1FAE5,stroke:#14A800,color:#001E00,stroke-width:2px
    classDef decision fill:#3C8224,stroke:#2E6B1B,color:#FFF,stroke-width:2px

    EXT[/"Upwork · LinkedIn · Fiverr · Outlier"/]
    ORCH(["ORCHESTRATOR\n17-State Machine"])

    subgraph P1["PHASE 1 · ACQUISITION"]
        direction TB
        CH["Agent 1\nContract Hunter"]
        BE["Agent 2\nBid Evaluator"]
        ABD{"Auto-Bid\nPolicy"}
        HG1(["Human Gate 1\nBid Approval"])
        BD["Agent 3\nBidder"]
    end

    subgraph P2["PHASE 2 · SOLUTION DESIGN"]
        direction TB
        IMP["Agent 4\nImplementer"]
        VA(["Agent 5\nView Agent\n............@cons.org"])
        APD{"Approval\nDecision"}
    end

    subgraph P3["PHASE 3 · DELIVERY EXECUTION"]
        direction TB
        TW["Agent 6\nTicket Writer"]
        CA["Agent 7\nCoding Agent"]
        CR["Agent 8\nCode Reviewer"]
        QA["Agent 9\nQA Agent"]
        DEL[/"Client Delivery"/]
    end

    subgraph ML["MEMORY AND LEARNING"]
        direction LR
        VDB[("Vector DB\nPinecone")]
        WLA["Win/Loss\nAnalytics"]
        NWB["Next Work\nBriefing"]
    end

    EXT --> CH
    CH --> BE
    BE --> ABD
    ABD -->|"Good Range\nAuto-Bid"| BD
    ABD -->|"High Value\nNeeds Review"| HG1
    HG1 -->|"Approved"| BD
    HG1 -->|"Rejected"| WLA
    BD -->|"Bid Submitted"| ORCH

    ORCH -->|"Contract Won"| IMP

    IMP --> VA
    VA --> APD
    APD -->|"Approve"| TW
    APD -->|"Revise"| IMP
    APD -->|"Reject"| WLA

    TW --> CA
    CA --> CR
    CR -->|"Pass"| QA
    CR -->|"Fail"| CA
    QA -->|"Pass"| DEL
    QA -->|"Fail"| CA
    DEL --> WLA

    WLA --> VDB
    VDB --> NWB
    NWB -->|"95-100% Match\nNext Opportunity"| CH
    VDB -.->|"RAG Context"| IMP
    VDB -.->|"Proposal History"| BD
    VDB -.->|"Win Patterns"| BE
    ORCH -.->|"State Sync"| VDB

    class CH,BE,BD p1agent
    class IMP p2agent
    class VA,HG1 humangate
    class TW,CA,CR,QA p3agent
    class DEL success
    class ORCH orchestrator
    class VDB,WLA,NWB memnode
    class EXT external
    class ABD,APD decision
```

---

## 📁 Repository Structure
```text
enterprise-agent-framework/
├── agents/             # specialized agent definitions (LangGraph)
├── memory/             # redis/postgres persistent storage logic
├── tools/              # external API tool handlers
├── rag/                # indexing and retrieval pipelines
├── api/                # FastAPI routes and middleware
└── ui/                 # Next.js admin dashboard
```

---

## 🛠️ Tech Stack
- **Frameworks**: LangGraph, LangChain, FastAPI
- **Intelligence**: Claude 3.5 Sonnet / GPT-4o
- **Database**: PostgreSQL (State/Memory), Pinecone (Vector)
- **Deployment**: Docker, Kubernetes, GitHub Actions

---

## 🚀 Quick Start
```bash
git clone https://github.com/Alan-911/enterprise-agent-framework.git
pip install -r requirements.txt
python main.py
```

---

*Developed by Yves Alain Iragena*  
[Portfolio](https://Alan-911.github.io/my-portfolio) | [LinkedIn](https://www.linkedin.com/in/yves-alain-iragena-91b44b391/)
