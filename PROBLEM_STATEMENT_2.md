# Problem Statement 2 - AI/ML Assessment

**Name:** Vishal Pandey  
**Email:** vishal70687934@gmail.com

---

## Overview

This document answers the assessment questions based on my practical experience designing and deploying enterprise-grade multi-agent LLM systems.

Rather than building a single chatbot, I have engineered a scalable agentic platform integrating multiple HR workflows including:

- Leave Policy & Leave Application Automation  
- Talent Acquisition (TA) Intelligence Agent  
- Background Verification (BGV) Operations Agent  

The architecture combines:

- AutoGen-based multi-agent orchestration  
- MCP (Model Context Protocol) tool servers  
- Role-based tool access control (RBAC)  
- Retrieval-Augmented Generation (RAG)  
- CosmosDB vector storage  
- Real-time session-based backend  
- Human-in-the-loop governance  

This submission reflects production-level system engineering rather than theoretical experimentation.

---

## Question 1: Self-Rating on AI/ML Technologies

**Where would you rate yourself on (LLM, Deep Learning, AI, ML)?**

### My Rating

| Domain | Rating | Reason |
|--------|--------|--------|
| Large Language Models (LLM) | A | Independently designed & deployed multi-agent production systems |
| Artificial Intelligence (AI) | A | Built intelligent automation workflows across HR systems |
| Machine Learning (ML) | B | Applied embeddings, similarity search, ranking logic |
| Deep Learning | B | Used transformer-based APIs; limited custom model training |

---

### Detailed Explanation

#### LLM – Rating: A

I rate myself A in Large Language Models because I have independently designed and deployed a production-grade multi-agent LLM platform handling three enterprise HR workflows:

- Leave Policy & Leave Application Agent  
- Talent Acquisition (TA) Agent  
- Background Verification (BGV) Agent  

This was not a single chatbot implementation. It was a structured, agentic system built using AutoGen where each agent had clearly defined responsibilities and connected tool layers.

**1. Leave Policy & Application Agent**

This agent integrates:

- Retrieval-Augmented Generation (RAG)
- CosmosDB vector storage
- Embeddings using `text-embedding-3-small`
- Policy validation logic
- Leave balance checking
- Prevention of invalid leave combinations
- Human-in-the-loop approval enforcement

The system chunks policy documents, stores embeddings with metadata, retrieves top-K relevant policy segments, and injects them into the LLM context to ensure grounded responses.

**2. Talent Acquisition (TA) Agent**

The TA Agent is connected to an MCP server exposing 50+ structured tools including:

- Job analytics
- Application counts
- Assessment tracking
- Interview status updates
- Candidate CRUD operations
- Real-time email triggering
- Follow-up notifications
- Status modifications across hiring pipeline

This agent functions as a conversational analytics and operations engine capable of querying live databases and executing workflow actions in real time.

**3. Background Verification (BGV) Agent**

The BGV Agent manages operational workflows such as:

- Case publishing decisions
- Document verification tracking
- Supplier assignment
- Case status transitions
- Compliance monitoring

It integrates CRUD operations and workflow state management through MCP tools.

**Security & Governance (Critical Component)**

Each agent connects to its own MCP server where I implemented Role-Based Access Control (RBAC) to ensure:

- Agents cannot execute unauthorized tools
- Tool execution is permission-controlled
- Security boundaries exist between workflows
- Enterprise governance is enforced

**Architectural Depth**

The overall system includes:

- AutoGen-based multi-agent orchestration
- Real-time socket-based session management
- RAG-based contextual reasoning
- Deterministic tool execution
- Vector database integration (CosmosDB)
- Human-in-the-loop governance controls

This reflects independent ownership of architecture design, tool integration, context injection strategies, security modeling, workflow automation, and production deployment thinking.

For these reasons, I confidently rate myself as A in LLM systems.

---

#### AI – Rating: A

My systems combine:

- Rule-based validation
- LLM reasoning
- Workflow automation
- Deterministic execution
- Governance-aware controls

I have built intelligent automation workflows that go beyond simple API calls into structured decision-making systems.

---

#### ML – Rating: B

I have practical experience with:

- Embedding generation (`text-embedding-3-small`)
- Semantic similarity search
- Ranking logic
- Metadata filtering
- Retrieval optimization

However, I am not currently training large-scale models from scratch. My focus has been on applying ML techniques within production systems rather than building models from the ground up.

---

#### Deep Learning – Rating: B

I use transformer-based APIs and embedding models in production systems. My exposure to building and training deep neural networks independently is moderate. I understand the concepts but haven't done extensive custom model training.

---

## Question 2: Key Architectural Components for an LLM-Based Chatbot

**What are the key architectural components required to build an LLM-based chatbot? Explain at a high level.**

### My Answer (Based on My Production System)

An enterprise LLM chatbot is not just a model API call. It requires layered architecture and controlled orchestration.

Based on my implementation, here are the key components:

---

### 1. Presentation Layer

- Built using Next.js
- Real-time socket communication
- Session-specific conversation handling
- Concurrent multi-user support

This ensures conversational continuity and state isolation across users.

---

### 2. Backend Orchestration Layer

- Python service
- Session manager
- AutoGen agent initialization
- Request routing

This layer separates user interaction from AI reasoning logic and handles the coordination between different components.

---

### 3. Multi-Agent Intelligence Layer

In my platform, I implemented three specialized agents:

| Agent | Responsibility |
|-------|----------------|
| Leave Policy & Application Agent | Policy queries, leave applications, balance checks |
| Talent Acquisition (TA) Agent | Hiring workflows, candidate management, analytics |
| Background Verification (BGV) Agent | Case management, document verification, compliance |

Each agent handles a distinct workflow and connects to its own MCP server.

---

### 4. MCP Tool Execution Layer

Each agent is connected to an MCP server providing structured tools.

**Leave Agent Tools:**
- Leave balance check
- Policy validation
- Leave submission
- Policy rule enforcement

**TA Agent Tools (50+ tools):**
- Job analytics
- Application counts
- Assessment tracking
- Interview tracking
- Candidate CRUD operations
- Real-time email triggering
- Status updates

**BGV Agent Tools:**
- Case publishing decisions
- Document verification tracking
- Supplier assignment
- Status transitions

I also implemented Role-Based Access Control (RBAC) inside MCP to ensure:

- Agents cannot execute unauthorized tools
- Tool usage remains secure
- Enterprise governance is enforced

---

### 5. Knowledge Layer (RAG)

The Leave Agent uses Retrieval-Augmented Generation:

- Policy documents chunked semantically
- Embeddings generated using `text-embedding-3-small`
- Stored in CosmosDB
- Hybrid vector + metadata search
- Top-K retrieval injected into prompt

This ensures context-grounded responses and reduces hallucination.

---

### 6. Governance Layer

Human-in-the-loop approval is enforced where required:

- Leave approvals require human confirmation
- Certain TA and BGV operations remain governed
- Automation is applied selectively

This balances efficiency and compliance.

---

### High-Level Architecture Flow

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: User Interface (Next.js + WebSocket)              │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│  Layer 2: Backend + Session Manager (Python)                │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│  Layer 3: AutoGen Multi-Agent Orchestration                 │
│  ┌──────────────┬──────────────┬──────────────┐            │
│  │ Leave Agent  │  TA Agent    │  BGV Agent   │            │
│  └──────────────┴──────────────┴──────────────┘            │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│  Layer 4: MCP Tool Servers (with RBAC)                      │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│  Layer 5: Vector Database (CosmosDB) + RAG Pipeline         │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│  Layer 6: Human-in-the-Loop Governance                      │
└─────────────────────────────────────────────────────────────┘
```

This layered architecture ensures scalability, security, and maintainability.

---

## Question 3: Vector Databases

**Please explain vector databases. If you were to select one for a hypothetical problem, which would you choose and why?**

---

### What is a Vector Database?

A vector database stores high-dimensional numerical embeddings that represent unstructured data such as text, images, or audio.

**How it works:**

1. Convert text → embedding vector (e.g., 1536 dimensions)
2. Store embedding + metadata in the database
3. Convert user query → embedding
4. Perform similarity search (cosine similarity)
5. Retrieve top-K relevant results

Unlike traditional databases that match exact keywords, vector databases enable semantic search - finding content that is conceptually similar even if the words are different.

---

### Hypothetical Problem: Enterprise Leave Policy Automation

**Scenario:**

An enterprise needs a leave policy assistant where employees ask questions like:

- "Can I combine casual and medical leave?"
- "How many sick leaves do I have left?"
- "What is the maternity leave eligibility criteria?"

**Why keyword search fails:**

- Users phrase the same question differently
- Exact keyword matching often misses relevant policies
- Contextual understanding is required
- Policy answers depend on semantic similarity, not literal word matching

**Why a Vector Database is needed:**

- Text → embedding conversion
- Semantic similarity search
- Top-K contextual retrieval
- Metadata-based filtering (department, employee type)
- Context injection into LLM prompts

---

### My Choice: Azure CosmosDB with Vector Search

For this enterprise scenario, I chose CosmosDB because:

| Factor | Why CosmosDB |
|--------|--------------|
| Enterprise Integration | Already part of Azure ecosystem used by the organization |
| Hybrid Storage | Stores both structured metadata and vector embeddings |
| Metadata Filtering | Supports combining vector search with traditional filters |
| Scalability | Handles large document collections efficiently |
| Security | Enterprise-grade security and compliance (SOC, HIPAA) |
| Managed Service | No operational overhead for infrastructure |

**Implementation Details:**

```
Document Processing Pipeline:

Policy PDF → Text Extraction → Chunking (500 chars)
     ↓
Embedding Generation (text-embedding-3-small)
     ↓
Store in CosmosDB (vector + metadata)
     ↓
Query: User question → Embedding → Similarity Search
     ↓
Top-K chunks → Inject into LLM prompt → Grounded response
```

---

### Alternative Vector Databases (When to Use)

| Database | Best For |
|----------|----------|
| Pinecone | Fully managed, zero ops, quick prototyping |
| Milvus | Self-hosted, billion-scale vectors, on-premise requirements |
| ChromaDB | Local development, simple Python integration |
| Weaviate | Hybrid search (BM25 + vector), GraphQL API |
| pgvector | Existing PostgreSQL stack, ACID compliance needed |

For my use case, CosmosDB made sense because the enterprise was already on Azure and needed tight integration with existing services.

---

## Summary

This document reflects my hands-on experience building production-grade AI systems rather than theoretical knowledge. The key takeaways:

1. **LLM Systems (A)** - Built multi-agent platforms with AutoGen, MCP tools, RBAC, and RAG
2. **AI Systems (A)** - Designed intelligent automation workflows combining rules + LLM reasoning
3. **ML (B)** - Applied embeddings and similarity search in production
4. **Deep Learning (B)** - Used transformer APIs; limited custom training

The architectural insights come from real implementation experience, not textbook definitions.

---

**Submitted by:** Vishal Pandey  
**For:** AI/ML Position Assessment at AccuKnox
