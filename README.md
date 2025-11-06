# Aethelgard Saga - Python Backend Services

**Version:** 2.0 (Production-Grade)
**Created:** November 6, 2025
**Status:** ✅ Contracts Complete | 🔨 Services In Development

---

## 🎯 Overview

This repository contains the **Python backend services** for the **Aethelgard Academy** learning platform ecosystem. It is the companion repository to [Aethelgard_Saga](https://github.com/AsheeshSrivastava/Aethelgard_Saga) (React frontend).

**Purpose:** AI-powered content generation, validation, and backend API services for the Zyric AI Ecosystem.

**Collaborative Workspace:** This repository is designed for real-time collaboration between **Claude Code** and **ChatGPT**, with clearly defined responsibilities in the [Developer Contract](contracts/DEVELOPER_CONTRACT.md).

---

## 🏗️ Repository Structure

```
aethelgard-saga-python/
├── contracts/                  # Production-grade API contracts (v2.0)
│   ├── shared_models.py        # Core data models (Pydantic v2)
│   ├── api_research_portal.py  # Research Portal ↔ Quality Checker
│   ├── api_questionforge.py    # QuestionForge ↔ Quality Checker
│   ├── api_backend.py          # Backend ↔ Quality Checker
│   ├── api_axis.py             # AXIS AI ↔ Backend
│   ├── SYSTEM_ARCHITECTURE.md  # Complete system design
│   ├── DEVELOPER_CONTRACT.md   # Claude ↔ ChatGPT agreement
│   ├── INTEGRATION_CHECKLIST.md # Implementation guide
│   └── README_FOR_ASHEESH.md   # User guide
│
├── quality-checker/            # 🟢 Claude Builds
│   └── [FastAPI + Gradio validation service]
│
├── research-portal/            # 🔵 ChatGPT Builds
│   └── [AI-powered concept generator]
│
├── backend-api/                # 🔵 ChatGPT Builds
│   └── [Main API serving validated content]
│
├── README.md                   # This file
├── .gitignore                  # Python .gitignore
└── requirements.txt            # Shared dependencies
```

---

## 🤖 System Components

### 1. Quality Checker (Claude Builds) 🟢

**Tech Stack:** FastAPI + Gradio + LangSmith
**Responsibility:** Validate content and questions against 10-criterion rubric

**Features:**
- ✅ Content validation (10 criteria, 100 points total, pass ≥85)
- ✅ Question validation (7-8 criteria depending on type)
- ✅ 4 quality gates: coverage, citation, exec_ok, scope_ok
- ✅ Batch validation (Quick/Full modes, max 100 items)
- ✅ Telemetry integration (LangSmith, 14 metrics)
- ✅ Authentication (Bearer tokens, 4 API keys)
- ✅ Idempotency (24-hour cache)

**API Endpoints:**
- `POST /api/v1/content/validate` - Validate single content
- `POST /api/v1/content/batch-validate` - Validate multiple content
- `POST /api/v1/questions/validate` - Validate single question
- `POST /api/v1/questions/batch-validate` - Validate multiple questions

**Status:** 🔨 Week 1 Implementation

---

### 2. Research Portal (ChatGPT Builds) 🔵

**Tech Stack:** Python + OpenAI API + RAG (LlamaIndex/LangChain)
**Responsibility:** Generate educational content using AI

**Features:**
- ✅ PSW framework content generation
- ✅ Code examples with expected output
- ✅ Citation extraction from vector database
- ✅ Difficulty assessment
- ✅ Mode-specific content (Coach/Hybrid/Socratic)
- ✅ Integration with Quality Checker

**Status:** 🔨 Week 2-3 Implementation

---

### 3. Backend API (ChatGPT Builds) 🔵

**Tech Stack:** FastAPI + PostgreSQL/Supabase
**Responsibility:** Serve validated content to frontend

**Features:**
- ✅ RESTful API for frontend consumption
- ✅ Content CRUD operations
- ✅ User progress tracking
- ✅ Learning path recommendations
- ✅ Integration with AXIS AI

**Status:** 🔨 Week 4-7 Implementation

---

## 📊 Production-Grade Quality Framework (v2.0)

### 10-Criterion Content Rubric (100 points total)

| Criterion | Max Points | Description |
|-----------|------------|-------------|
| Groundedness & Citation | 20 | Evidence-based, properly cited |
| Technical Correctness | 15 | Accurate, no errors |
| People-First Pedagogy | 15 | Adult learning principles |
| PSW Actionability | 10 | Problem-System-Win framework |
| Mode Fidelity | 10 | Coach/Hybrid/Socratic alignment |
| Self-Paced Scaffolding | 10 | Progressive difficulty |
| Retrieval Quality | 10 | Context relevance |
| Clarity | 5 | Clear, concise |
| Bloom Alignment | 3 | Cognitive level match |
| People-First Language | 2 | Inclusive, respectful |

**Pass Criteria:**
- Overall score ≥85
- AND all 4 quality gates passed:
  1. `coverage_score` ≥0.65
  2. `citation_density` ≥1.0
  3. `exec_ok` = true
  4. `scope_ok` = true

### 7-8 Criterion Question Rubric (100 points total)

| Question Type | Criteria Count | Specific Focus |
|---------------|----------------|----------------|
| Knowledge Check | 7 | Multiple choice validation |
| Code Writing | 8 | Test cases + quality |
| Debugging | 7 | Error analysis |
| Code Reading | 7 | Comprehension |
| Mini-Project | 8 | Holistic assessment |

---

## 🔒 Code Execution Sandbox (Pyodide)

**Security Constraints:**
- ⏱️ **Timeout:** 5 seconds maximum per code example
- 💾 **Memory:** 50 MB limit per execution
- 🌐 **Network:** No network access allowed
- 📁 **File System:** Read-only, no write access
- 📦 **Approved Libraries Only:**
  - core-python (built-ins)
  - numpy, pandas (data)
  - matplotlib, seaborn (visualization)
  - scikit-learn (ML)

**Rationale:** Secure execution in browser via WebAssembly (Pyodide). Prevents malicious code, ensures reproducibility.

**Gate Enforcement:** `exec_ok` gate fails if any code example times out, exceeds memory, or imports unapproved library.

---

## 📖 Web Citation Allowlist

**Pre-Approved Citation Sources:**

**Official/Academic:**
- docs.python.org (PSF License)
- ocw.mit.edu (MIT OpenCourseWare, CC BY-NC-SA)
- www.cmu.edu (Carnegie Mellon University)
- www.credentialingexcellence.org (ICE/NOCA certification standards)

**Community/Professional:**
- realpython.com (Python tutorials)
- stackoverflow.com (Q&A community)
- github.com (open source code)
- medium.com (technical articles)
- questandcrossfire.com (internal brand domain)

**Escalation Process (for non-allowlisted sources):**
1. Quality Checker flags non-allowlisted citation
2. Manual review by senior engineer (1-3 days)
3. Approval decision (approve/reject with rationale)
4. If approved, domain added to allowlist

**Rationale:** Ensures citation quality, prevents unreliable sources, maintains academic standards.

**Gate Enforcement:** `citation_density` gate checks both quantity (≥1.0) and quality (allowlist compliance).

---

## 🔐 Authentication

**Bearer Token Required:** All API endpoints require `Authorization: Bearer <API_KEY>` header.

**4 API Keys (stored in environment variables):**
1. `RESEARCH_PORTAL_API_KEY` - Research Portal → Quality Checker
2. `QUESTIONFORGE_API_KEY` - QuestionForge → Quality Checker
3. `BACKEND_API_KEY` - Backend → Quality Checker
4. `AXIS_API_KEY` - AXIS AI → Backend

**Idempotency:** Use `Idempotency-Key` header for safe retries (24-hour TTL).

---

## 📈 Telemetry (LangSmith Integration)

**14 Metrics Tracked:**

**Run Metadata:**
- run_id, trace_url, model, provider, prompt_version, graph_version

**Quality Metrics:**
- coverage_score, citation_density, unique_sources

**Pedagogy Metrics:**
- mode_ratio, scaffold_depth, exec_ok

**Performance Metrics:**
- latency_ms, tokens

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- OpenAI API key
- LangSmith API key (optional, for telemetry)

### Installation

```bash
# Clone repository
git clone https://github.com/AsheeshSrivastava/aethelgard-saga-python.git
cd aethelgard-saga-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Running Services

**Quality Checker (Claude builds):**
```bash
cd quality-checker
uvicorn main:app --reload --port 8000
```

**Research Portal (ChatGPT builds):**
```bash
cd research-portal
python main.py
```

**Backend API (ChatGPT builds):**
```bash
cd backend-api
uvicorn main:app --reload --port 8001
```

---

## 📚 Key Documentation

**Start Here:**
1. [README_FOR_ASHEESH.md](contracts/README_FOR_ASHEESH.md) - Simple user guide
2. [DEVELOPER_CONTRACT.md](contracts/DEVELOPER_CONTRACT.md) - Claude ↔ ChatGPT agreement
3. [SYSTEM_ARCHITECTURE.md](contracts/SYSTEM_ARCHITECTURE.md) - Complete system design

**API Contracts:**
4. [shared_models.py](contracts/shared_models.py) - Core data models
5. [api_research_portal.py](contracts/api_research_portal.py) - Research Portal API
6. [api_questionforge.py](contracts/api_questionforge.py) - QuestionForge API
7. [api_backend.py](contracts/api_backend.py) - Backend API
8. [api_axis.py](contracts/api_axis.py) - AXIS AI API

**Implementation:**
9. [INTEGRATION_CHECKLIST.md](contracts/INTEGRATION_CHECKLIST.md) - Step-by-step guide

---

## ⚠️ BREAKING CHANGES (v2.0)

**From v1.0 to v2.0:**

1. **`PythonConcept` → `AethelgardConcept`** (BREAKING)
   - Renamed for brand consistency
   - New fields: `code_examples`, `provisional_citations`, `mode`, `libraries`

2. **Pydantic v2 Migration:**
   - `.dict()` → `.model_dump()`
   - Update all serialization code

3. **Authentication Required:**
   - All endpoints now require Bearer token
   - Add `Authorization` header to all requests

4. **Pass Threshold Raised:**
   - v1.0: 70 points to pass
   - v2.0: 85 points to pass (higher quality bar)

5. **4 Quality Gates Added:**
   - Score ≥85 is not enough
   - Must pass all 4 gates (coverage, citation, exec_ok, scope_ok)

**Migration Guide:** See [DEVELOPER_CONTRACT.md](contracts/DEVELOPER_CONTRACT.md) § Migration Guide

---

## 🗓️ Development Timeline

**10-Week Roadmap (Nov 13, 2025 - Jan 21, 2026)**

### Tier 1: Foundation (Weeks 1-3)
- **Week 1:** Quality Checker implementation (Claude)
- **Week 2-3:** Research Portal implementation (ChatGPT)
- **Milestone:** Brother demo with working content generation + validation

### Tier 2: Core Platform (Weeks 4-7)
- **Week 4-5:** Backend API implementation (ChatGPT)
- **Week 6-7:** AXIS AI integration (ChatGPT)
- **Milestone:** Complete backend ready for frontend integration

### Tier 3: Advanced Features (Weeks 8-9)
- **Week 8-9:** Narration Generator (AI-powered)
- **Milestone:** Full narrative-driven learning experience

### Polish & Launch (Week 10)
- **Week 10:** Bug fixes, optimization, documentation
- **Milestone:** Production-ready for public launch

---

## 🔗 Related Repositories

- **Frontend:** [Aethelgard_Saga](https://github.com/AsheeshSrivastava/Aethelgard_Saga) (React 18 + TypeScript + Vite)
- **Portfolio:** [claude-projects](https://github.com/AsheeshSrivastava/claude-projects) (Root workspace)
- **Question Bank:** QuestionForge (existing validation system)

---

## 🤝 Collaboration

**Claude Code Responsibilities:**
- Quality Checker (FastAPI + Gradio)
- Validation logic (10 criteria, 4 gates)
- Test suite for validation
- API contract enforcement
- Code review for ChatGPT's work

**ChatGPT Responsibilities:**
- Research Portal (content generation)
- Backend API (FastAPI)
- Frontend integration
- Database schema
- User-facing features

**Shared Responsibilities:**
- Following contracts in `contracts/shared_models.py`
- API contract adherence
- Documentation updates
- Integration testing
- Performance optimization

---

## 📄 License

**License:** AGPL-3.0

**Trademarks:**
- **AETHELGARD ACADEMY™** - Filed, awaiting certification
- **AETHELGARD AXIS™** - Filed, awaiting certification
- **QUEST AND CROSSFIRE™** - Filed, awaiting certification

**AI Assistance:** This project was developed with assistance from:
- Claude Code (Anthropic) - Quality Checker, contracts, architecture
- ChatGPT (OpenAI) - Research Portal, Backend API, content generation

---

## 👤 Author

**Asheesh Ranjan Srivastava**
- **Email:** asheeshsrivastava9@gmail.com
- **GitHub:** [@AsheeshSrivastava](https://github.com/AsheeshSrivastava)
- **LinkedIn:** [asheesh-ranjan-srivastava](https://www.linkedin.com/in/asheesh-ranjan-srivastava/)

---

## 📊 Repository Statistics

- **Contract Files:** 9 files, 5,133 lines, ~197KB
- **Services:** 3 services (Quality Checker, Research Portal, Backend API)
- **Quality Framework:** 10 criteria, 4 gates, 100-point scale
- **API Endpoints:** 4 main endpoints + batch variants
- **Timeline:** 10 weeks (Nov 13, 2025 - Jan 21, 2026)

---

**Last Updated:** November 6, 2025
**Version:** 2.0 (Production-Grade)
**Status:** ✅ Contracts Complete | 🔨 Services In Development

---

**◇ Where chaos becomes clarity. Small fixes, big clarity.**

---

**For questions or collaboration inquiries, please contact Asheesh Ranjan Srivastava.**
