# The Zyric AI Ecosystem - System Architecture

**Version:** 2.0
**Created:** 2025-11-06
**Updated:** 2025-11-06 (Production-grade upgrade)

---

## 🏗️ COMPLETE SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     THE ZYRIC AI ECOSYSTEM                              │
│                    (5 Systems, 4 Communication Flows)                   │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│  FLOW 1: Content Generation & Validation                                │
└──────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐
    │ Research Portal │
    │  (ChatGPT)      │
    │                 │
    │ • Generates     │
    │   Python        │
    │   concepts      │
    │ • PSW framework │
    │ • Code examples │
    │ • Citations     │
    │ • Mode metadata │
    └────────┬────────┘
             │
             │ POST /api/v1/content/validate
             │ (sends AethelgardConcept)
             │ Authorization: Bearer <RESEARCH_PORTAL_API_KEY>
             │ Idempotency-Key: <UUID>
             │
             ▼
    ┌─────────────────┐
    │ Quality Checker │
    │   (Claude)      │
    │                 │
    │ • Validates     │
    │   content       │
    │ • 10 criteria   │
    │ • Score 0-100   │
    │ • Pass ≥85      │
    │ • 4 Gates       │
    │ • Telemetry     │
    └────────┬────────┘
             │
             │ Returns QualityReport
             │ (overall_score, gates, telemetry, issues, strengths)
             │
             ▼
    ┌─────────────────┐
    │ Aethelgard      │
    │   Backend       │
    │  (ChatGPT)      │
    │                 │
    │ • Stores only   │
    │   validated     │
    │   content       │
    │ • Database +    │
    │   Vector DB     │
    └─────────────────┘


┌──────────────────────────────────────────────────────────────────────────┐
│  FLOW 2: Question Generation & Validation                               │
└──────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐
    │ QuestionForge   │
    │   (Existing)    │
    │                 │
    │ • Generates     │
    │   practice      │
    │   questions     │
    │ • Multiple      │
    │   choice, T/F,  │
    │   code writing  │
    └────────┬────────┘
             │
             │ POST /api/v1/questions/validate
             │ (sends Question)
             │ Authorization: Bearer <QUESTIONFORGE_API_KEY>
             │ Idempotency-Key: <UUID>
             │
             ▼
    ┌─────────────────┐
    │ Quality Checker │
    │   (Claude)      │
    │                 │
    │ • Validates     │
    │   questions     │
    │ • 10 criteria   │
    │ • Bloom's level │
    │ • Difficulty    │
    │ • Pass ≥85      │
    │ • 4 Gates       │
    └────────┬────────┘
             │
             │ Returns QualityReport
             │ (overall_score, gates, blooms_alignment_score, issues)
             │
             ▼
    ┌─────────────────┐
    │ Aethelgard      │
    │   Backend       │
    │  (ChatGPT)      │
    │                 │
    │ • Stores only   │
    │   validated     │
    │   questions     │
    │ • Links to      │
    │   concepts      │
    └─────────────────┘


┌──────────────────────────────────────────────────────────────────────────┐
│  FLOW 3: Backend Batch Validation (Optimization)                        │
└──────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐
    │ Aethelgard      │
    │   Backend       │
    │  (ChatGPT)      │
    │                 │
    │ • Receives      │
    │   multiple      │
    │   items         │
    │ • Needs batch   │
    │   validation    │
    │ • Max 100 items │
    └────────┬────────┘
             │
             │ POST /api/v1/content/batch-validate
             │ (sends List[AethelgardConcept | Question], max 100)
             │ Authorization: Bearer <BACKEND_API_KEY>
             │ Idempotency-Key: <UUID>
             │ mode: "quick" | "full" (optional)
             │
             ▼
    ┌─────────────────┐
    │ Quality Checker │
    │   (Claude)      │
    │                 │
    │ • Validates     │
    │   batch         │
    │ • Quick mode:   │
    │   80% accuracy  │
    │ • Full mode:    │
    │   99% accuracy  │
    │ • 207 Multi-    │
    │   Status        │
    └────────┬────────┘
             │
             │ Returns BatchValidationResponse
             │ (total: 10, passed: 8, failed: 2, results: [...])
             │ HTTP 207 Multi-Status for partial success
             │
             ▼
    ┌─────────────────┐
    │ Aethelgard      │
    │   Backend       │
    │  (ChatGPT)      │
    │                 │
    │ • Stores passed │
    │ • Rejects       │
    │   failed        │
    │ • Retry failed  │
    │   (idempotent)  │
    └─────────────────┘


┌──────────────────────────────────────────────────────────────────────────┐
│  FLOW 4: AXIS AI Content Retrieval                                      │
└──────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐
    │  AXIS AI        │
    │  Chatbot        │
    │  (ChatGPT)      │
    │                 │
    │ • Learner asks  │
    │   question      │
    │ • Needs content │
    │   to answer     │
    └────────┬────────┘
             │
             │ GET /api/v1/content/search?q=how to store data
             │   &min_quality_score=85
             │   &min_citation_density=1.0
             │ (semantic search with RAG)
             │ Authorization: Bearer <AXIS_API_KEY>
             │
             ▼
    ┌─────────────────┐
    │ Aethelgard      │
    │   Backend       │
    │  (ChatGPT)      │
    │                 │
    │ • RAG search    │
    │ • Retrieves     │
    │   relevant      │
    │   concepts      │
    │ • Returns only  │
    │   validated     │
    │   (score ≥85)   │
    └────────┬────────┘
             │
             │ Returns List[AethelgardConcept]
             │ (ranked by relevance, includes quality_score)
             │
             ▼
    ┌─────────────────┐
    │  AXIS AI        │
    │  Chatbot        │
    │  (ChatGPT)      │
    │                 │
    │ • Uses content  │
    │   to generate   │
    │   answer        │
    │ • LangGraph     │
    │   orchestrates  │
    │ • Mode-specific │
    │   prompts       │
    └─────────────────┘


┌──────────────────────────────────────────────────────────────────────────┐
│  SUPPORTING FLOW: Learning Path Navigation                              │
└──────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐
    │  AXIS AI        │
    │  Chatbot        │
    │  (ChatGPT)      │
    │                 │
    │ • Learner       │
    │   completed     │
    │   concept       │
    │ • Asks "what    │
    │   next?"        │
    └────────┬────────┘
             │
             │ GET /api/v1/content/{concept_id}/next
             │   ?min_quality_score=85
             │ Authorization: Bearer <AXIS_API_KEY>
             │
             ▼
    ┌─────────────────┐
    │ Aethelgard      │
    │   Backend       │
    │  (ChatGPT)      │
    │                 │
    │ • Checks        │
    │   prerequisites │
    │ • Recommends    │
    │   next concepts │
    │ • Quality       │
    │   filtered      │
    └────────┬────────┘
             │
             │ Returns List[AethelgardConcept]
             │ (next recommended concepts, quality ≥85)
             │
             ▼
    ┌─────────────────┐
    │  AXIS AI        │
    │  Chatbot        │
    │  (ChatGPT)      │
    │                 │
    │ • Presents      │
    │   learning path │
    │ • Guides        │
    │   learner       │
    └─────────────────┘
```

---

## 📊 SYSTEM RESPONSIBILITIES

### 1. Research Portal (ChatGPT builds)

**Technology Stack:**
- FastAPI (web framework)
- LangChain (LLM orchestration)
- OpenAI API (GPT-4o or GPT-4o-latest)
- Pydantic v2 (data validation)
- Vector database (for RAG context)

**Responsibilities:**
- Generate Python learning concepts using LLM
- Structure content in PSW framework (Problem-System-Win)
- Create beginner-friendly code examples (CodeExample model)
- Add citations from curriculum (Citation model)
- Specify mode (Coach, Hybrid, Socratic)
- Enforce library scope (core-python, numpy, pandas, etc.)
- Send concepts to Quality Checker for validation
- Store validated concepts in Backend

**API Endpoints (provides):**
- None (internal system)

**API Endpoints (consumes):**
- POST /api/v1/content/validate (Quality Checker)

**Data Models Used:**
- AethelgardConcept (creates) - formerly PythonConcept
- CodeExample (creates for code_examples field)
- Citation (creates for provisional_citations field)
- QualityReport (receives)

**Environment Variables:**
```bash
RESEARCH_PORTAL_API_KEY=<secret>  # For Quality Checker authentication
OPENAI_API_KEY=<sk-...>           # For LLM generation
```

---

### 2. QuestionForge (Existing system)

**Technology Stack:**
- Python (existing codebase)
- Gradio (UI)
- YAML configuration
- Pydantic v2 (validation)

**Responsibilities:**
- Generate practice questions from concepts
- Support multiple question types (MCQ, True/False, Code Writing, etc.)
- Validate questions meet quality criteria locally
- Send questions to Quality Checker for validation
- Store validated questions in Backend

**API Endpoints (provides):**
- None (CLI/Gradio interface)

**API Endpoints (consumes):**
- POST /api/v1/questions/validate (Quality Checker)

**Data Models Used:**
- Question (creates)
- QuestionType, BloomsLevel, DifficultyLevel (uses)
- QualityReport (receives)

**Environment Variables:**
```bash
QUESTIONFORGE_API_KEY=<secret>  # For Quality Checker authentication
```

---

### 3. Quality Checker (Claude builds) ⭐ **YOUR RESPONSIBILITY**

**Technology Stack:**
- FastAPI (web framework)
- Gradio (UI for manual testing)
- Pydantic v2 (validation)
- OpenAI API (for advanced quality checks)
- LangSmith (telemetry tracing)
- Pyodide (code execution sandbox)

**Responsibilities:**
- Validate Python concepts (10 criteria, 4 gates)
- Validate practice questions (10 criteria, 4 gates)
- Score content 0-100 (pass threshold: 85+, raised from 70)
- Provide detailed feedback (issues, strengths, suggestions)
- Support batch validation (max 100 items, Quick/Full modes)
- Execute code examples to verify correctness (exec_ok gate)
- Track telemetry (LangSmith integration: run_id, trace_url, 9+ metrics)
- Provide Gradio UI for manual testing

**API Endpoints (provides):**
- POST /api/v1/content/validate
- POST /api/v1/questions/validate
- POST /api/v1/content/batch-validate

**API Endpoints (consumes):**
- None (standalone validation service)

**Data Models Used:**
- AethelgardConcept (validates) - formerly PythonConcept
- Question (validates)
- QualityReport (creates)
- ValidationRequest, ValidationResponse (API)
- BatchValidationRequest, BatchValidationResponse (batch)

**Authentication:**
```bash
# Accepted API keys (from environment)
RESEARCH_PORTAL_API_KEY=<secret>
QUESTIONFORGE_API_KEY=<secret>
BACKEND_API_KEY=<secret>

# Authorization header format
Authorization: Bearer <API_KEY>

# Idempotency support (validation endpoints)
Idempotency-Key: <UUID>  # Cache TTL: 24 hours
```

**Quality Criteria (10-Criterion Rubric - 100 points total):**

**For Content (AethelgardConcept):**

| Criterion | Points | Description |
|-----------|--------|-------------|
| 1. Groundedness & Citation Quality | 0-20 | Citations present, accurate, relevant |
| 2. Technical Correctness | 0-15 | Factually accurate, no errors, current |
| 3. People-First Pedagogy | 0-15 | Problem-oriented, experiential, applicable |
| 4. PSW Actionability | 0-10 | Clear Problem-System-Win structure |
| 5. Mode Fidelity | 0-10 | Question ratio matches declared mode |
| 6. Self-Paced Scaffolding | 0-10 | Progressive complexity, hints |
| 7. Retrieval Quality | 0-10 | Keyword-rich, context-independent, parseable |
| 8. Clarity | 0-5 | Beginner-friendly language, clear |
| 9. Bloom Alignment | 0-3 | Tests correct cognitive level |
| 10. People-First Language | 0-2 | Inclusive, respectful, gender-neutral |

**For Questions:**

| Criterion | Points | Description |
|-----------|--------|-------------|
| 1. Groundedness & Citation Quality | 0-20 | Less critical for questions (weight reduced) |
| 2. Technical Correctness | 0-15 | Factually accurate, correct answer |
| 3. People-First Pedagogy | 0-15 | Problem-oriented, applicable |
| 4. PSW Actionability | 0-10 | Less critical for questions (weight reduced) |
| 5. Mode Fidelity | 0-10 | Less critical for questions (weight reduced) |
| 6. Self-Paced Scaffolding | 0-10 | Hints, explanation helps learner |
| 7. Retrieval Quality | 0-10 | Keyword-rich, searchable |
| 8. Clarity | 0-5 | Clear question text, no ambiguity |
| 9. Bloom Alignment | 0-3 | Tests correct cognitive level |
| 10. People-First Language | 0-2 | Inclusive language |

**Quality Gates (must all pass):**

| Gate | Threshold | Description |
|------|-----------|-------------|
| coverage_score | ≥0.65 | Content covers concept adequately |
| citation_density | ≥1.0 | Minimum citations per concept (≥1.0 for content, relaxed for questions) |
| exec_ok | true | All runnable code examples execute successfully (Pyodide sandbox) |
| scope_ok | true | Only approved libraries used (core-python, numpy, pandas, matplotlib, seaborn, scikit-learn) |

**Pass Criteria:**
- Overall score ≥85 (raised from 70) AND all core gates passed

**Telemetry Object (9+ metrics tracked via LangSmith):**

| Metric | Type | Description |
|--------|------|-------------|
| run_id | str | LangSmith run identifier |
| trace_url | str | LangSmith trace URL |
| model | str | LLM model used (e.g., gpt-4o-2024-11-20) |
| provider | str | LLM provider (e.g., openai) |
| prompt_version | str | Validation prompt version |
| graph_version | str | Validation graph version |
| coverage_score | float | Content coverage metric (0.0-1.0) |
| citation_density | float | Citations per concept |
| unique_sources | int | Number of unique citation sources |
| mode_ratio | float | Question/total content ratio (Mode fidelity) |
| scaffold_depth | int | Progressive scaffolding levels |
| exec_ok | bool | All code executed successfully |
| latency_ms | int | Validation latency in milliseconds |
| tokens | int | Total tokens consumed |

**Mode System (Coach/Hybrid/Socratic):**

| Mode | Question Ratio | Description |
|------|----------------|-------------|
| Coach | 0.15-0.30 | Mostly explanations, occasional questions |
| Hybrid | 0.30-0.45 | Balanced explanations and questions |
| Socratic | 0.50-0.70 | Mostly questions, minimal direct answers |

**Library Scope Enforcement:**
- Approved libraries: core-python, numpy, pandas, matplotlib, seaborn, scikit-learn
- scope_ok gate rejects topics using unapproved libraries
- Ensures curriculum stays within defined boundaries

**Batch Validation Modes:**

| Mode | Accuracy | Code Exec | Telemetry | Use Case |
|------|----------|-----------|-----------|----------|
| Quick | ~80% | No | Partial | Fast pre-filtering |
| Full | ~99% | Yes | Complete | Production validation |

**Batch Validation Limits:**
- Max items per request: 100
- HTTP 207 Multi-Status for partial success
- Individual status per item in results array

---

### 4. Aethelgard Backend (ChatGPT builds)

**Technology Stack:**
- FastAPI (web framework)
- LangGraph (workflow orchestration)
- Vector database (LanceDB or similar)
- PostgreSQL (structured data)
- Pydantic v2 (validation)

**Responsibilities:**
- Store validated content and questions
- Provide content to AXIS AI (RAG search)
- Learning path management (prerequisites, next concepts)
- Progress tracking (optional)
- Batch validation coordination (max 100 items)
- Quality filtering (min_quality_score ≥85, min_citation_density ≥1.0)
- Database management

**API Endpoints (provides):**
- GET /api/v1/content/{concept_id}
- GET /api/v1/content/list
- GET /api/v1/content/search (RAG)
- GET /api/v1/questions/{concept_id}
- GET /api/v1/questions/random
- GET /api/v1/content/{concept_id}/prerequisites
- GET /api/v1/content/{concept_id}/next
- POST /api/v1/progress/update

**API Endpoints (consumes):**
- POST /api/v1/content/batch-validate (Quality Checker)

**Data Models Used:**
- AethelgardConcept (stores and serves) - formerly PythonConcept
- Question (stores and serves)
- QualityReport (stores with content/questions)

**Authentication:**
```bash
# API key for AXIS AI
AXIS_API_KEY=<secret>

# API key for Quality Checker
BACKEND_API_KEY=<secret>

# Authorization header format
Authorization: Bearer <AXIS_API_KEY>
```

**Quality Guarantees:**
- All content served has quality_score ≥85
- All content passed 4 quality gates
- All content has citation_density ≥1.0
- All code examples verified via exec_ok gate

---

### 5. AXIS AI Chatbot (ChatGPT builds)

**Technology Stack:**
- LangGraph (agentic workflow)
- LangChain (LLM orchestration)
- OpenAI API (GPT-4o or GPT-4o-latest)
- Gradio or Streamlit (UI)

**Responsibilities:**
- Chat interface for learners
- Retrieve relevant content from Backend (RAG)
- Answer learner questions using validated content
- Guide learning path (suggest next concepts)
- Practice mode (present questions, check answers)
- Multiple coaching modes (Coach, Hybrid, Socratic)
- Mode-specific prompt generation

**API Endpoints (provides):**
- None (user-facing chatbot interface)

**API Endpoints (consumes):**
- GET /api/v1/content/search (Backend)
- GET /api/v1/content/{concept_id} (Backend)
- GET /api/v1/questions/{concept_id} (Backend)
- GET /api/v1/content/{concept_id}/next (Backend)

**Data Models Used:**
- AethelgardConcept (receives from Backend)
- Question (receives from Backend)

**Authentication:**
```bash
# API key for Backend
AXIS_API_KEY=<secret>

# Authorization header format
Authorization: Bearer <AXIS_API_KEY>
```

**Mode System Implementation:**
- Coach Mode: Mostly explanations (0.15-0.30 question ratio)
- Hybrid Mode: Balanced (0.30-0.45 question ratio)
- Socratic Mode: Mostly questions (0.50-0.70 question ratio)

---

## 🔄 DATA FLOW EXAMPLES

### Example 1: New Concept Creation (v2.0)

```
1. Research Portal generates concept:
   AethelgardConcept(
       concept_id="python-variables-01",
       title="Variables",
       problem="How do you store data in Python so you can use it later?",
       system="Variables work like labeled boxes. You create a variable by giving it a name and assigning a value using the equals sign (=).",
       win="Now you can store any data (numbers, text, lists) and reuse it throughout your program without typing it again.",
       code_examples=[
           CodeExample(
               code="age = 25\nprint(age)  # Output: 25",
               expected_output="25",
               runnable=True
           ),
           CodeExample(
               code="name = 'Alice'\nprint(name)  # Output: Alice",
               expected_output="Alice",
               runnable=True
           )
       ],
       provisional_citations=[
           Citation(
               source="vector",
               title="Python Tutorial §2.1: Variables",
               locator="§2.1.1",
               url="https://docs.python.org/3/tutorial/introduction.html",
               license="PSF"
           )
       ],
       difficulty="beginner",
       prerequisites=[],
       tags=["variables", "basics", "data-storage"],
       mode="coach",
       libraries=["core-python"]
   )

2. Research Portal sends to Quality Checker:
   POST /api/v1/content/validate
   Authorization: Bearer <RESEARCH_PORTAL_API_KEY>
   Idempotency-Key: <UUID>
   Body: {concept JSON}

3. Quality Checker validates (10-criterion rubric):
   - Groundedness & Citation: 18/20 ✓
   - Technical Correctness: 14/15 ✓
   - People-First Pedagogy: 13/15 ✓
   - PSW Actionability: 9/10 ✓
   - Mode Fidelity: 9/10 ✓
   - Self-Paced Scaffolding: 8/10 ✓
   - Retrieval Quality: 9/10 ✓
   - Clarity: 4/5 ✓
   - Bloom Alignment: 2/3 ✓
   - People-First Language: 1/2 ✓
   - Overall: 87/100 ✓ (PASS ≥85)

   Gates:
   - coverage_score: 0.72 ≥0.65 ✓
   - citation_density: 1.2 ≥1.0 ✓
   - exec_ok: true (both code examples executed) ✓
   - scope_ok: true (only core-python used) ✓

4. Quality Checker responds:
   QualityReport(
       item_id="python-variables-01",
       item_type="content",
       overall_score=87,
       groundedness_citation_score=18,
       technical_correctness_score=14,
       people_first_pedagogy_score=13,
       psw_actionability_score=9,
       mode_fidelity_score=9,
       self_paced_scaffolding_score=8,
       retrieval_quality_score=9,
       clarity_score=4,
       bloom_alignment_score=2,
       people_first_language_score=1,
       gates=[
           {"name": "coverage_score", "passed": true, "details": "0.72 >= 0.65"},
           {"name": "citation_density", "passed": true, "details": "1.2 >= 1.0"},
           {"name": "exec_ok", "passed": true, "details": "All code executed"},
           {"name": "scope_ok", "passed": true, "details": "Only core-python used"}
       ],
       telemetry={
           "run_id": "run_abc123",
           "trace_url": "https://langsmith.com/trace/abc123",
           "model": "gpt-4o-2024-11-20",
           "provider": "openai",
           "prompt_version": "v2.0",
           "graph_version": "v1.0",
           "coverage_score": 0.72,
           "citation_density": 1.2,
           "unique_sources": 1,
           "mode_ratio": 0.20,
           "scaffold_depth": 1,
           "exec_ok": true,
           "latency_ms": 1234,
           "tokens": 567
       },
       passes_quality=True,
       issues=[],
       strengths=[
           "Strong groundedness with citations",
           "Clear PSW structure",
           "All code examples executable"
       ],
       suggestions=[
           "Add more scaffolding prompts for self-paced learning"
       ],
       validated_at="2025-11-08T10:30:00Z",
       validator_version="2.0"
   )

5. Research Portal stores in Backend:
   POST /api/backend/store
   Authorization: Bearer <RESEARCH_PORTAL_API_KEY>
   Body: {concept + quality_report}

6. Backend saves to database:
   - Validated content table (only score ≥85)
   - Vector embeddings for RAG
   - Quality report stored (gates, telemetry, scores)
```

### Example 2: Learner Asks Question (v2.0)

```
1. Learner asks AXIS AI:
   "How do I store data in Python?"

2. AXIS AI searches Backend:
   GET /api/v1/content/search?q=how to store data
     &min_quality_score=85
     &min_citation_density=1.0
   Authorization: Bearer <AXIS_API_KEY>

3. Backend returns relevant concepts (quality-filtered):
   [
       {
           concept_id: "python-variables-01",
           title: "Variables",
           relevance_score: 0.92,
           quality_score: 87,
           citation_density: 1.2,
           gates_passed: true,
           excerpt: "Variables work like labeled boxes..."
       },
       {
           concept_id: "python-datatypes-01",
           title: "Data Types",
           relevance_score: 0.85,
           quality_score: 89,
           citation_density: 1.5,
           gates_passed: true,
           excerpt: "Python has several data types..."
       }
   ]

4. AXIS AI retrieves top concept:
   GET /api/v1/content/python-variables-01
   Authorization: Bearer <AXIS_API_KEY>

5. Backend returns full concept:
   AethelgardConcept(
       ...full concept with quality_score, citation_density, gates_passed...
   )

6. AXIS AI uses LLM to generate answer (Coach mode):
   Context: {concept.problem, concept.system, concept.win, code_examples}
   User question: "How do I store data?"
   Mode: Coach (0.15-0.30 question ratio)
   LLM generates: "Great question! In Python, you store data using variables. Variables work like labeled boxes..."

7. AXIS AI responds to learner with answer
```

### Example 3: Batch Validation (v2.0)

```
1. Backend receives 50 new concepts from Research Portal

2. Backend sends batch to Quality Checker:
   POST /api/v1/content/batch-validate
   Authorization: Bearer <BACKEND_API_KEY>
   Idempotency-Key: <UUID>
   Body: {
       items: [concept1, concept2, ..., concept50],
       validation_type: "full"  # 99% accuracy, all gates, telemetry
   }

3. Quality Checker validates all 50 (10-criterion rubric, 4 gates):
   - concept1: 87/100 PASS (all gates passed)
   - concept2: 89/100 PASS (all gates passed)
   - concept3: 72/100 FAIL (citation_density: 0.8 < 1.0)
   - concept4: 81/100 FAIL (overall < 85)
   - ...
   - concept50: 90/100 PASS (all gates passed)

4. Quality Checker responds:
   HTTP 207 Multi-Status
   BatchValidationResponse(
       total_items=50,
       passed=46,
       failed=4,
       results=[
           BatchValidationResult(
               item_id="concept1",
               status="passed",
               quality_score=87,
               gates_passed=true,
               report={...full QualityReport with gates, telemetry...}
           ),
           ...
           BatchValidationResult(
               item_id="concept3",
               status="failed",
               quality_score=72,
               gates_passed=false,
               report={
                   ...gates=[
                       {"name": "citation_density", "passed": false, "details": "0.8 < 1.0"}
                   ]...
               }
           ),
           ...
       ]
   )

5. Backend processes results:
   - Store 46 passed concepts (quality ≥85, all gates passed)
   - Reject 4 failed concepts
   - Log failed items for Research Portal review
   - Can retry failed items with same Idempotency-Key (idempotent)
```

---

## 🔐 SECURITY & AUTHENTICATION

### API Key Management

**Quality Checker accepts:**
- RESEARCH_PORTAL_API_KEY (Research Portal → Quality Checker)
- QUESTIONFORGE_API_KEY (QuestionForge → Quality Checker)
- BACKEND_API_KEY (Backend → Quality Checker)

**Backend accepts:**
- AXIS_API_KEY (AXIS AI → Backend)

**Environment Variables:**
```bash
# Quality Checker
RESEARCH_PORTAL_API_KEY=<secret>
QUESTIONFORGE_API_KEY=<secret>
BACKEND_API_KEY=<secret>
OPENAI_API_KEY=sk-...
QUALITY_CHECKER_PORT=8000
LANGSMITH_API_KEY=<secret>  # For telemetry

# Backend
DATABASE_URL=postgresql://...
VECTOR_DB_PATH=/path/to/vector/db
BACKEND_PORT=9000
AXIS_API_KEY=<secret>
BACKEND_API_KEY=<secret>  # For Quality Checker

# AXIS AI
AXIS_API_KEY=<secret>
OPENAI_API_KEY=sk-...
AXIS_PORT=8501

# Research Portal
RESEARCH_PORTAL_API_KEY=<secret>
OPENAI_API_KEY=sk-...

# QuestionForge
QUESTIONFORGE_API_KEY=<secret>
```

### Authorization Header Format

All API requests require authentication:
```
Authorization: Bearer <API_KEY>
```

### Idempotency Support (Validation Endpoints)

All validation endpoints support idempotency:
```
Idempotency-Key: <UUID>  # Optional, auto-generated if not provided
```

- Cache TTL: 24 hours
- Prevents duplicate validation for same content
- Same Idempotency-Key returns cached result
- Useful for retry logic in batch validation

### Rate Limiting

- Quality Checker: 100 validations/minute per API key
- Backend: 100 requests/minute for AXIS AI
- Research Portal: No limit (internal system)

---

## 📈 PERFORMANCE TARGETS

### Response Times
- Quality Checker (single): < 5 seconds
- Quality Checker (batch of 50 Quick mode): < 15 seconds
- Quality Checker (batch of 50 Full mode): < 45 seconds
- Backend (single concept): < 200ms
- Backend (RAG search): < 500ms
- AXIS AI (full response): < 3 seconds

### Throughput
- Quality Checker: 100 validations/minute (single)
- Quality Checker: 1000 items/minute (batch Quick mode)
- Quality Checker: 500 items/minute (batch Full mode)
- Backend: 1000 requests/minute
- AXIS AI: 50 concurrent users

### Quality (v2.0 Production Standards)
- Validation accuracy (Full mode): 99%+ (matches human expert)
- Validation accuracy (Quick mode): 80%+ (good for pre-filtering)
- False positives: < 3% (good content rejected)
- False negatives: < 1% (bad content passed)
- Pass rate: ~85% of generated content passes ≥85 threshold
- Gate pass rate: ~90% of content passes all 4 gates

### Code Execution Validation
- All runnable code examples executed in Pyodide sandbox
- exec_ok gate: 95%+ code execution success rate
- Execution timeout: 5 seconds per code example
- Sandbox security: Isolated environment, no file system access

---

## 🧪 INTEGRATION TESTING

See `contracts/INTEGRATION_CHECKLIST.md` for detailed Day 6-7 integration plan.

**v2.0 Integration Requirements:**
- All systems must use AethelgardConcept (not PythonConcept)
- All validation requests must include Authorization header
- All validation requests should include Idempotency-Key for retry safety
- Backend must filter content by quality_score ≥85 and gates_passed=true
- AXIS AI must handle quality metadata in responses (quality_score, citation_density, gates_passed)
- Code examples must use CodeExample model format
- Citations must use Citation model format
- Mode field must be one of: coach, hybrid, socratic
- Libraries field must only include approved libraries

---

## 📝 VERSION HISTORY

**v1.0 (2025-11-06):**
- Initial architecture
- 5 systems defined (Research Portal, QuestionForge, Quality Checker, Backend, AXIS AI)
- 4 communication flows documented
- API contracts defined
- Data models specified
- 7-criterion quality rubric
- Pass threshold: 70

**v2.0 (2025-11-06):**
- **PRODUCTION-GRADE UPGRADE**
- Upgraded: 7-criterion → 10-criterion rubric (100 points)
- Added: 4 quality gates (coverage_score ≥0.65, citation_density ≥1.0, exec_ok, scope_ok)
- Raised: Pass threshold 70 → 85
- Added: Telemetry object with 9+ metrics (LangSmith integration)
- Added: Authentication system (4 API keys from environment)
- Added: Idempotency support (Idempotency-Key header, 24-hour cache)
- Renamed: PythonConcept → AethelgardConcept
- Added: CodeExample model for code_examples field (code, expected_output, runnable)
- Added: Citation model for provisional_citations field (source, title, locator, url, license)
- Added: Mode field (Coach 0.15-0.30, Hybrid 0.30-0.45, Socratic 0.50-0.70 question ratios)
- Added: Library scope enforcement (6 approved libraries)
- Updated: Batch validation with Quick/Full modes (80% vs 99% accuracy)
- Added: HTTP 207 Multi-Status for batch partial success
- Added: Max 100 items per batch validation request
- Updated: Code execution validation via Pyodide sandbox
- Updated: All data flow examples to v2.0 format
- Updated: All API endpoint examples with authentication
- Updated: Performance targets with v2.0 metrics
- Updated: Security section with environment variable details
- Pydantic v2 migration: .dict() → .model_dump()

---

**Last Updated:** 2025-11-06 (v2.0 production-grade upgrade)
**Next Review:** After Day 0-5 implementation (Nov 13, 2025)
