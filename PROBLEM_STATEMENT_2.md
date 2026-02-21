# Problem statement- assignment 2  
**Name:** Vishal Pandey  
**Email:** vishal70687934@gmail.com

---

# Overview

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

# Question 1  
## Where would you rate yourself on (LLM, Deep Learning, AI, ML)?  


### My Rating

| Domain | Rating | Reason |
|--------|--------|--------|
| Large Language Models (LLM) | A | Independently designed & deployed multi-agent production systems |
| Artificial Intelligence (AI) | A | Built intelligent automation workflows across HR systems |
| Machine Learning (ML) | B | Applied embeddings, similarity search, ranking logic |
| Deep Learning | B | Used transformer-based APIs; limited custom model training |

---

### Explanation

## LLM – A

I rate myself A in Large Language Models because I have independently designed and deployed a production-grade multi-agent LLM platform handling three enterprise HR workflows:

- Leave Policy & Leave Application Agent  
- Talent Acquisition (TA) Agent  
- Background Verification (BGV) Agent  

This was not a single chatbot implementation. It was a structured, agentic system built using AutoGen where each agent had clearly defined responsibilities and connected tool layers.

### 1. Leave Policy & Application Agent

This agent integrates:

- Retrieval-Augmented Generation (RAG)
- CosmosDB vector storage
- Embeddings using `text-embedding-3-small`
- Policy validation logic
- Leave balance checking
- Prevention of invalid leave combinations
- Human-in-the-loop approval enforcement

The system chunks policy documents, stores embeddings with metadata, retrieves top-K relevant policy segments, and injects them into the LLM context to ensure grounded responses.

---

### 2. Talent Acquisition (TA) Agent

The TA Agent is connected to an MCP server exposing **50+ structured tools** including:

- Job analytics
- Application counts
- Assessment tracking
- Interview status updates
- Candidate CRUD operations
- Real-time email triggering
- Follow-up notifications
- Status modifications across hiring pipeline

This agent functions as a conversational analytics and operations engine capable of querying live databases and executing workflow actions in real time.

---

### 3. Background Verification (BGV) Agent

The BGV Agent manages operational workflows such as:

- Case publishing decisions
- Document verification tracking
- Supplier assignment
- Case status transitions
- Compliance monitoring

It integrates CRUD operations and workflow state management through MCP tools.

---

### Security & Governance (Critical Component)

Each agent connects to its own MCP server where I implemented **Role-Based Access Control (RBAC)** to ensure:

- Agents cannot execute unauthorized tools
- Tool execution is permission-controlled
- Security boundaries exist between workflows
- Enterprise governance is enforced

---

### Architectural Depth

The overall system includes:

- AutoGen-based multi-agent orchestration
- Real-time socket-based session management
- RAG-based contextual reasoning
- Deterministic tool execution
- Vector database integration (CosmosDB)
- Human-in-the-loop governance controls

This reflects independent ownership of:

- Architecture design
- Tool integration
- Context injection strategies
- Security modeling
- Workflow automation
- Production deployment thinking

For these reasons, I confidently rate myself as A in LLM systems.
---

## AI – A

My systems combine:

- Rule-based validation
- LLM reasoning
- Workflow automation
- Deterministic execution
- Governance-aware controls

---

## ML – B

I have practical experience with:

- Embedding generation (`text-embedding-3-small`)
- Semantic similarity search
- Ranking logic
- Metadata filtering
- Retrieval optimization

However, I am not currently training large-scale models from scratch.

---

## Deep Learning – B

I use transformer-based APIs and embedding models in production systems.  
My exposure to building and training deep neural networks independently is moderate.

---

# Question 2  
## What are the key architectural components required to build an LLM-based chatbot? Explain at a high level.

### My Answer (Based on My Production System)

An enterprise LLM chatbot is not just a model API call. It requires layered architecture and controlled orchestration.

Based on my implementation, the key components are:

---

## 1. Presentation Layer

- Built using Next.js
- Real-time socket communication
- Session-specific conversation handling
- Concurrent multi-user support

This ensures conversational continuity and state isolation.

---

## 2. Backend Orchestration Layer

- Python service
- Session manager
- AutoGen agent initialization
- Request routing

This layer separates user interaction from AI reasoning logic.

---

## 3. Multi-Agent Intelligence Layer

In my platform, I implemented three specialized agents:

- Leave Policy & Application Agent  
- Talent Acquisition (TA) Agent  
- Background Verification (BGV) Agent  

Each agent handles a distinct workflow and connects to its own MCP server.

---

## 4. MCP Tool Execution Layer

Each agent is connected to an MCP server providing structured tools.

For example:

### Leave Agent
- Leave balance check
- Policy validation
- Leave submission
- Policy rule enforcement

### TA Agent (50+ Tools)
- Job analytics
- Application counts
- Assessment tracking
- Interview tracking
- Candidate CRUD operations
- Real-time email triggering
- Status updates

### BGV Agent
- Case publishing decisions
- Document verification tracking
- Supplier assignment
- Status transitions

I also implemented **Role-Based Access Control (RBAC)** inside MCP to ensure:

- Agents cannot execute unauthorized tools
- Tool usage remains secure
- Enterprise governance is enforced

---

## 5. Knowledge Layer (RAG)

The Leave Agent uses Retrieval-Augmented Generation:

- Policy documents chunked semantically
- Embeddings generated using `text-embedding-3-small`
- Stored in CosmosDB
- Hybrid vector + metadata search
- Top-K retrieval injected into prompt

This ensures context-grounded responses and reduces hallucination.

---

## 6. Governance Layer

Human-in-the-loop approval is enforced where required:

- Leave approvals require human confirmation
- Certain TA and BGV operations remain governed
- Automation is applied selectively

This balances efficiency and compliance.

---

### High-Level Flow (Simplified)

Layer 1 – User Interface  
Layer 2 – Backend + Session Manager  
Layer 3 – AutoGen Multi-Agent Orchestration  
Layer 4 – MCP Tool Execution  
Layer 5 – Vector Database (CosmosDB)  
Layer 6 – Human Governance  

This layered architecture ensures scalability, security, and maintainability.

---

# Question 3  
## Please explain vector databases. If you were to select one for a hypothetical problem, which would you choose and why?

---

## What is a Vector Database?

A vector database stores high-dimensional numerical embeddings that represent unstructured data such as text.

Process:

1. Convert text → embedding vector  
2. Store embedding + metadata  
3. Convert user query → embedding  
4. Perform similarity search (cosine similarity)  
5. Retrieve top-K relevant results  

Unlike traditional databases, vector databases enable semantic search rather than keyword matching.

---

## Hypothetical Problem

Enterprise Leave Policy Automation System:

Employees ask:

- “Can I combine casual and medical leave?”
- “How many sick leaves are left?”
- “What is maternity leave eligibility?”

Policies are stored as unstructured documents.  
Keyword search is insufficient.  
Semantic similarity is required.

## Why a Vector Database Was Required

In the enterprise leave automation system, policy documents are stored as unstructured text. Employees may ask questions in natural language such as:

- “Can I combine casual and medical leave?”
- “How many sick leaves are available?”
- “What is maternity leave eligibility criteria?”

Traditional keyword-based search would not be sufficient because:

- Users may phrase the same question differently
- Exact keyword matching may fail
- Contextual understanding is required
- Policy answers often depend on semantic similarity rather than literal word matching

To solve this, we needed:

- Text → embedding conversion
- Semantic similarity search
- Top-K contextual retrieval
- Metadata-based filtering
- Context injection into LLM prompts

A vector database enables high-dimensional similarity search using cosine similarity, making semantic retrieval efficient and scalable.
