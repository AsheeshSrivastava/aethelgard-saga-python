# Developer Contract: Claude Code ↔ ChatGPT

**Mediated By**: Asheesh
**Purpose**: Ensure seamless code integration between two AI developers
**Timeline**: Experimental Phase (Nov 8-17, 2025)
**Version**: 2.0
**Created**: 2025-11-06
**Updated**: 2025-11-06 (Production-grade upgrade)

---

## 🎯 Purpose

Claude Code and ChatGPT are building different parts of **The Zyric AI Ecosystem** in parallel. This contract ensures their code integrates smoothly without conflicts.

**Think of it like**: Two construction crews building different floors of the same building. They need to agree on:
- Staircase locations (API endpoints)
- Electrical outlets (data formats)
- Plumbing connections (request/response protocols)

---

## 👥 Work Division

### Claude Code Builds:
- ✅ **Quality Checker** (FastAPI + Gradio)
  - Content validation logic
  - Question validation logic
  - Scoring algorithms (**10 criteria**, 100 points total, pass ≥85)
  - **4 quality gates**: coverage_score ≥0.65, citation_density ≥1.0, exec_ok, scope_ok
  - **Telemetry integration**: LangSmith tracking with 14 metrics
  - API endpoints: `/api/v1/content/validate`, `/api/v1/questions/validate`
  - Batch validation: `/api/v1/content/batch-validate` (Quick/Full modes, max 100 items)
  - Gradio UI for manual testing
  - **Authentication**: Bearer token validation (4 API keys from environment)
  - **Idempotency**: 24-hour cache for validation requests

### ChatGPT Builds:
- ✅ **Research Portal** (FastAPI + LangChain)
  - Python concept generation
  - PSW framework implementation
  - Content management
  - Sends **AethelgardConcept** to Quality Checker with authentication

- ✅ **AXIS AI** (LangGraph + Agentic RAG)
  - Chatbot with coaching modes (Coach/Hybrid/Socratic)
  - Retrieval from validated content (quality_score ≥85, gates passed)
  - Web search integration (Day 12 bootcamp)
  - Mode-specific question ratios (Coach: 15-30%, Hybrid: 30-45%, Socratic: 50-70%)

- ✅ **Aethelgard Backend** (FastAPI + LangGraph)
  - Stores validated content (quality_score ≥85 AND all gates passed)
  - Serves content to AXIS AI with quality metadata
  - Database management
  - Quality filtering on retrieval

### Joint Responsibility:
- ✅ API contracts (both review and agree)
- ✅ Integration testing (Days 6-7)
- ✅ Bug fixes (whoever can fix it faster)

---

## 🛠️ Technology Stack Agreement

**Both MUST Use:**

| Category | Technology | Version | Why |
|----------|-----------|---------|-----|
| Language | Python | 3.11+ | User's environment |
| Web Framework | FastAPI | 0.120.4 | Async, fast, auto docs |
| Data Models | Pydantic | 2.x | Type safety, validation |
| LLM | OpenAI API | Latest | GPT-4o or GPT-4o-latest |
| Type Hints | Required | PEP 484 | Code clarity |
| Async | async/await | Always for I/O | Performance |
| Authentication | Bearer Tokens | Environment vars | API security |
| Telemetry | LangSmith | Latest | Quality tracking |

**Specific to Each:**

| Developer | Can Choose |
|-----------|------------|
| Claude | LlamaIndex 0.9.14 OR LangChain 1.0.3 |
| ChatGPT | LangGraph OR custom state machine |
| Claude | Gradio for UI |
| ChatGPT | Gradio OR Streamlit for UI |

**Critical Dependencies:**
- NumPy: Must use `<2` (1.26.4 recommended) for compatibility
- Pydantic: v2 migration complete (`.dict()` → `.model_dump()`)
- OpenAI: ≥1.40.0 for proxy compatibility

---

## 📦 Shared Data Structures (CRITICAL)

**Rule #1**: EVERYONE imports from `contracts/shared_models.py`
**Rule #2**: NO ONE creates their own versions
**Rule #3**: Changes require ALL developers to agree

### Core Models (v2.0 - UPDATED)

```python
from contracts.shared_models import (
    # Core content models
    AethelgardConcept,   # Python concept (RENAMED from PythonConcept)
    CodeExample,         # NEW: Code with optional output + runnable flag
    Citation,            # NEW: Citation with source, title, locator, URL, license

    # Question models
    Question,            # Question data structure (unchanged)
    QuestionType,        # NEW: Enum for question types
    BloomsLevel,         # NEW: Enum for Bloom's taxonomy levels
    DifficultyLevel,     # NEW: Enum for difficulty levels

    # Quality models
    QualityReport,       # Validation results (10 criteria + gates + telemetry)

    # Supporting models
    CitationSource,      # NEW: Enum (vector, api, manual)
    Mode,                # NEW: Enum (coach, hybrid, socratic)
    Library,             # NEW: Enum (approved libraries)

    # API models
    ValidationRequest,   # API request format (deprecated - use model directly)
    ValidationResponse,  # API response format (deprecated - use QualityReport)
    ErrorResponse,       # Standard error format
    SuccessResponse,     # Standard success format

    # Helper functions
    create_success_response,
    create_error_response
)
```

### v2.0 Model Changes

**BREAKING CHANGE:** `PythonConcept` → `AethelgardConcept`

```python
# ❌ OLD (v1.0)
from contracts.shared_models import PythonConcept

concept = PythonConcept(
    concept_id="python-variables-01",
    title="Variables",
    problem="How do you store data?",
    system="Use variables like x = 5",
    win="Now you can store data",
    # ... other fields
)

# ✅ NEW (v2.0)
from contracts.shared_models import AethelgardConcept, CodeExample, Citation

concept = AethelgardConcept(
    concept_id="python-variables-01",
    title="Variables",
    problem="How do you store data in Python so you can use it later?",
    system="Variables work like labeled boxes that store values.",
    win="Now you can store any data (numbers, text, lists) and reuse it.",
    code_examples=[
        CodeExample(
            code="age = 25\nprint(age)  # Output: 25",
            expected_output="25",
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
    tags=["variables", "basics"],
    mode="coach",
    libraries=["core-python"]
)
```

**NEW FIELDS in AethelgardConcept:**
- `code_examples: List[CodeExample]` (structured, with runnable flag)
- `provisional_citations: List[Citation]` (structured, with source tracking)
- `mode: Mode` (coach/hybrid/socratic for AXIS AI)
- `libraries: List[Library]` (approved library scope enforcement)

**Question Model** (unchanged - no new fields):
```python
Question(
    question_id="q-variables-mc-01",
    concept_id="python-variables-01",
    question_text="What happens when you assign a value to a variable?",
    question_type="multiple_choice",
    options=["...", "...", "...", "..."],
    correct_answer="...",
    difficulty="beginner",
    blooms_level="understand",
    explanation="Variables work like labeled containers.",
    hints=["Think about what a variable represents"]
)
```

**QualityReport** (10 criteria + gates + telemetry):
```python
QualityReport(
    item_id="python-variables-01",
    item_type="content",
    overall_score=87,  # Pass threshold: ≥85

    # 10-criterion scores (100 points total)
    groundedness_citation_score=18,      # 0-20 pts
    technical_correctness_score=14,      # 0-15 pts
    people_first_pedagogy_score=13,      # 0-15 pts
    psw_actionability_score=9,           # 0-10 pts
    mode_fidelity_score=9,               # 0-10 pts
    self_paced_scaffolding_score=8,      # 0-10 pts
    retrieval_quality_score=9,           # 0-10 pts
    clarity_score=4,                     # 0-5 pts
    bloom_alignment_score=2,             # 0-3 pts
    people_first_language_score=1,       # 0-2 pts

    # Quality gates (all must pass)
    gates=[
        {"name": "coverage_score", "passed": True, "details": "0.72 >= 0.65"},
        {"name": "citation_density", "passed": True, "details": "1.2 >= 1.0"},
        {"name": "exec_ok", "passed": True, "details": "All code executed"},
        {"name": "scope_ok", "passed": True, "details": "Only core-python used"}
    ],

    # Telemetry (LangSmith integration)
    telemetry={
        "run_id": "run_abc123",
        "trace_url": "https://langsmith.com/trace/abc123",
        "model": "gpt-4o-2024-11-20",
        "provider": "openai",
        "prompt_version": "v2.0",
        "graph_version": "v1.0",
        "coverage_score": 0.72,
        "citation_density": 1.2,
        "unique_sources": 3,
        "mode_ratio": 0.25,
        "scaffold_depth": 2,
        "exec_ok": True,
        "latency_ms": 1234,
        "tokens": 567
    },

    issues=[...],
    strengths=[...],
    suggestions=[...],
    passes_quality=True,  # overall_score >= 85 AND all gates passed
    validated_at="2025-11-08T10:30:00Z",
    validator_version="2.0"
)
```

### Change Process

**If anyone needs to modify these models:**

1. **Request** (via Asheesh):
   ```
   ChatGPT (via Asheesh): "I need to add 'learning_objectives'
                           field to AethelgardConcept"
   ```

2. **Review** (Claude):
   ```
   Claude: "Good idea. Will this break existing code?
            Let me check... No conflicts. Approved."
   ```

3. **Update** (Claude updates file):
   ```python
   class AethelgardConcept(BaseModel):
       # ... existing fields ...
       learning_objectives: List[str] = Field(
           default_factory=list,
           description="Learning objectives for this concept"
       )
   ```

4. **Notify** (Asheesh notifies ChatGPT):
   ```
   Asheesh to ChatGPT: "shared_models.py updated.
                        New field: learning_objectives (optional list).
                        Update your code."
   ```

5. **Acknowledge** (ChatGPT confirms):
   ```
   ChatGPT: "Got it. Updating Research Portal to use new field."
   ```

---

## 🎨 Code Style Agreement

**Both follow Python PEP 8:**

### Naming Conventions

```python
# ✅ CORRECT
class AethelgardConcept:       # PascalCase for classes
    pass

def validate_content():        # snake_case for functions
    pass

API_BASE_URL = "http://..."    # UPPER_CASE for constants

user_name = "Alice"            # snake_case for variables
```

```python
# ❌ WRONG
class aethelgardConcept:       # Wrong case
    pass

def ValidateContent():         # Wrong case
    pass

apiBaseUrl = "http://..."      # Wrong case
```

### Type Hints (REQUIRED)

```python
# ✅ CORRECT
async def validate_content(
    concept: AethelgardConcept
) -> QualityReport:
    """Validate Python concept."""
    pass

def get_score(report: QualityReport) -> int:
    return report.overall_score
```

```python
# ❌ WRONG - No type hints
def validate_content(concept):
    pass

def get_score(report):
    return report.overall_score
```

### Docstrings (REQUIRED)

```python
# ✅ CORRECT
def validate_content(concept: AethelgardConcept) -> QualityReport:
    """
    Validate Python concept against quality criteria.

    Args:
        concept: Python concept to validate

    Returns:
        Quality report with scores and feedback

    Raises:
        ValueError: If concept format invalid
    """
    pass
```

```python
# ❌ WRONG - No docstring
def validate_content(concept: AethelgardConcept) -> QualityReport:
    pass
```

### Comments

```python
# ✅ CORRECT - Explain WHY
# Use exponential backoff to handle rate limits
await asyncio.sleep(2 ** retry_count)

# ❌ WRONG - Explain WHAT (code already shows this)
# Sleep for 2 to the power of retry_count
await asyncio.sleep(2 ** retry_count)
```

### Pydantic v2 Migration

```python
# ❌ OLD (Pydantic v1)
concept.dict()
report.dict()

# ✅ NEW (Pydantic v2)
concept.model_dump()
report.model_dump()
```

---

## 🌐 API Response Format Agreement

**All APIs MUST return these formats:**

### Success Response

```python
{
    "status": "success",
    "message": "Content validated successfully",
    "data": {
        "item_id": "python-variables-01",
        "item_type": "content",
        "overall_score": 87,

        # 10-criterion scores
        "groundedness_citation_score": 18,
        "technical_correctness_score": 14,
        # ... all 10 scores ...

        # Quality gates
        "gates": [
            {"name": "coverage_score", "passed": true, "details": "0.72 >= 0.65"},
            {"name": "citation_density", "passed": true, "details": "1.2 >= 1.0"},
            {"name": "exec_ok", "passed": true, "details": "All code executed"},
            {"name": "scope_ok", "passed": true, "details": "Only core-python used"}
        ],

        # Telemetry
        "telemetry": {
            "run_id": "run_abc123",
            "trace_url": "https://langsmith.com/trace/abc123",
            "model": "gpt-4o-2024-11-20",
            "coverage_score": 0.72,
            "citation_density": 1.2,
            "exec_ok": true,
            "latency_ms": 1234,
            "tokens": 567
        },

        "passes_quality": true,
        "validated_at": "2025-11-08T10:30:00Z"
    },
    "timestamp": "2025-11-08T10:30:00Z"
}
```

### Error Response

```python
{
    "status": "error",
    "error": "Invalid concept format",
    "details": "Field 'problem' is too short (minimum 50 characters)",
    "code": 400,
    "timestamp": "2025-11-08T10:30:00Z"
}
```

### Example Implementation

```python
from contracts.shared_models import (
    SuccessResponse,
    ErrorResponse,
    create_success_response,
    create_error_response
)

# ✅ CORRECT (Pydantic v2)
@app.post("/api/v1/content/validate")
async def validate_content(
    concept: AethelgardConcept,
    authorization: str = Header(...),
    idempotency_key: str = Header(None)
):
    # Verify API key
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization")

    api_key = authorization.split("Bearer ")[1]
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Check idempotency
    if idempotency_key:
        cached_result = check_idempotency_cache(idempotency_key)
        if cached_result:
            return cached_result

    try:
        report = await quality_checker.validate(concept)
        response = create_success_response(
            message="Content validated successfully",
            data=report.model_dump()  # Pydantic v2
        )

        # Store in idempotency cache
        if idempotency_key:
            store_idempotency_cache(idempotency_key, response)

        return response
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                error="Invalid concept format",
                details=str(e),
                code=400
            ).model_dump()  # Pydantic v2
        )
```

---

## 🔒 Authentication & Security

**All API calls MUST include authentication:**

### Environment Variables

```bash
# Quality Checker (validates 3 API keys)
RESEARCH_PORTAL_API_KEY=<secret>
QUESTIONFORGE_API_KEY=<secret>
BACKEND_API_KEY=<secret>
LANGSMITH_API_KEY=<secret>  # For telemetry

# Backend (validates 2 API keys)
AXIS_API_KEY=<secret>
BACKEND_API_KEY=<secret>

# AXIS AI
AXIS_API_KEY=<secret>
```

### Request Headers

**Validation Endpoints** (Quality Checker):
```python
Authorization: Bearer <API_KEY>
Idempotency-Key: <UUID>  # Optional, recommended for retry safety
```

**Retrieval Endpoints** (Backend):
```python
Authorization: Bearer <API_KEY>
```

### Dev Defaults (for local testing)

```python
RESEARCH_PORTAL_API_KEY = os.getenv(
    "RESEARCH_PORTAL_API_KEY",
    "dev-key-research-portal"
)
```

### Idempotency Support

**Validation endpoints support idempotency:**
- Cache TTL: 24 hours
- Key format: UUID v4
- Auto-generated if not provided (client-side)
- Same request = same response (from cache)

---

## 📁 File Structure Agreement

**Both follow this structure:**

```
project_name/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── models.py            # Import from contracts/shared_models.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── validator.py
│   │   └── generator.py
│   └── api/                 # API routes
│       ├── __init__.py
│       └── routes.py
├── contracts/               # Shared models (DO NOT MODIFY)
│   ├── shared_models.py     # v2.0 - All 5 systems import from here
│   ├── api_research_portal.py
│   ├── api_questionforge.py
│   ├── api_backend.py
│   ├── api_axis.py
│   ├── SYSTEM_ARCHITECTURE.md
│   └── DEVELOPER_CONTRACT.md  # This file
├── tests/                   # Unit and integration tests
│   ├── test_models.py
│   ├── test_services.py
│   └── test_api.py
├── requirements.txt         # Python dependencies
├── README.md                # Setup instructions
└── .env.example             # Environment variables template
```

---

## 🔌 Endpoint Naming Agreement

**Pattern**: `/api/{version}/{resource}/{action}`

### Examples

```python
# ✅ CORRECT (v2.0)
POST /api/v1/content/validate
POST /api/v1/questions/validate
POST /api/v1/content/batch-validate  # NEW: Batch validation
GET  /api/v1/content/{id}
GET  /api/v1/content/search  # NEW: Quality-filtered search
GET  /api/v1/content/list

# ❌ WRONG
POST /validate-content          # Missing /api/ prefix
POST /api/ValidateContent       # Wrong case
POST /api/content-validation    # Use verbs, not nouns
```

### Quality-Filtered Retrieval

```python
# Backend retrieval endpoint (AXIS AI uses this)
GET /api/v1/content/search?q=variables
    &min_quality_score=85
    &min_citation_density=1.0
Authorization: Bearer <AXIS_API_KEY>

# Returns only content that:
# - overall_score >= 85
# - citation_density >= 1.0
# - passes_quality = true (all gates passed)
```

---

## 🤝 Communication Protocol

**Asheesh is the mediator.** All inter-AI communication goes through him.

### Asking Questions

**ChatGPT → Claude:**
```
ChatGPT (to Asheesh):
"I'm getting 400 error from Quality Checker.
Expected AethelgardConcept but receiving dict.
What format should I send?"

Asheesh (to Claude):
"ChatGPT is sending dict instead of AethelgardConcept JSON.
Can you clarify the expected format?"

Claude (to Asheesh):
"Send as JSON with .model_dump() method:
requests.post(url, json=concept.model_dump())"

Asheesh (to ChatGPT):
"Claude says: Use concept.model_dump() when sending."

ChatGPT:
"Thanks! Fixed. Also updated from .dict() to .model_dump()."
```

### Reporting Bugs

**Claude → ChatGPT:**
```
Claude (to Asheesh):
"Research Portal is sending 'difficulty_level'
but contract says 'difficulty'. Can ChatGPT fix?"

Asheesh (to ChatGPT):
"Claude found a field name mismatch.
Use 'difficulty' not 'difficulty_level'."

ChatGPT:
"Fixed in commit abc123."
```

### Reporting v2.0 Migration Issues

**ChatGPT → Claude:**
```
ChatGPT (to Asheesh):
"Getting import error: 'No module named PythonConcept'.
Was it renamed in v2.0?"

Asheesh (to Claude):
"ChatGPT needs migration guidance for v2.0."

Claude (to Asheesh):
"Yes, breaking change:
- OLD: from shared_models import PythonConcept
- NEW: from shared_models import AethelgardConcept

Also update:
- .dict() → .model_dump() (Pydantic v2)
- Add authentication headers
- Add idempotency-key for validation calls"

Asheesh (to ChatGPT):
"Claude provided migration guide. Update imports and method calls."

ChatGPT:
"Updated. All systems now using AethelgardConcept + v2.0 patterns."
```

---

## ⚙️ Handoff Format

**When delivering code to Asheesh:**

### Checklist

- [ ] Code runs locally without errors
- [ ] All imports from `contracts/shared_models.py` v2.0
- [ ] Uses `AethelgardConcept` (not PythonConcept)
- [ ] Pydantic v2 migration complete (`.model_dump()`)
- [ ] Authentication implemented (Bearer tokens)
- [ ] Idempotency support (validation endpoints)
- [ ] Type hints on all functions
- [ ] Docstrings on all public functions
- [ ] requirements.txt with exact versions (numpy<2)
- [ ] README.md with setup instructions
- [ ] .env.example for environment variables
- [ ] At least basic tests (smoke tests minimum)
- [ ] LangSmith telemetry integration (Quality Checker only)

### Delivery Message Template

```
[AI Name] delivers [Component Name]:

✅ Status: Ready for integration
✅ Tested: All endpoints working locally
✅ Contracts: Uses shared_models.py v2.0
✅ Authentication: Bearer token validation implemented
✅ Quality: 10-criterion rubric, pass ≥85, 4 gates

📦 Files:
- app/main.py (150 lines)
- app/services/validator.py (200 lines)
- requirements.txt (12 dependencies, numpy<2)
- README.md (setup instructions)
- .env.example (API keys template)

🧪 Tests:
- test_models.py: 10 tests passing
- test_api.py: 5 endpoints tested

🔌 Endpoints:
- POST /api/v1/content/validate (with auth + idempotency)
- POST /api/v1/questions/validate (with auth + idempotency)
- POST /api/v1/content/batch-validate (Quick/Full modes)

⚠️ Known Issues:
- None

📝 Next Steps:
- Ready for integration testing
- Asheesh can test at http://localhost:8000
- Use dev-key-* for local testing
```

---

## 🐛 Conflict Resolution

**If Claude and ChatGPT disagree:**

### Example Conflict

```
ChatGPT: "Let's use 'difficulty_level' for clarity"
Claude:   "Let's use 'difficulty' for brevity"
```

### Resolution Process

1. **Present Options** (both to Asheesh):
   ```
   Claude: "Two options:
   Option A: 'difficulty' (shorter, follows Python conventions)
   Option B: 'difficulty_level' (more explicit)
   I prefer A but can do B."
   ```

2. **Asheesh Decides**:
   ```
   Asheesh: "Let's go with Option A ('difficulty').
            Matches existing QuestionForge code."
   ```

3. **Both Follow**:
   ```
   Claude: "Using 'difficulty'. Updated shared_models.py v2.0."
   ChatGPT: "Using 'difficulty'. Updated Research Portal."
   ```

4. **Document Decision**:
   ```
   Add to contracts/DECISIONS.md:

   ## Decision 001: Field Naming
   Date: 2025-11-08
   Decision: Use 'difficulty' not 'difficulty_level'
   Rationale: Shorter, matches existing QuestionForge
   Agreed by: Claude, ChatGPT, Asheesh
   ```

---

## 🧪 Testing Agreement

**Both responsible for:**

### Unit Tests

```python
# Test your own code
def test_validate_content():
    concept = AethelgardConcept(...)
    report = validate_content(concept)
    assert report.overall_score > 0
    assert len(report.gates) == 4
    assert report.passes_quality == True
```

### Integration Tests

```python
# Test cross-system communication with authentication
def test_research_portal_to_quality_checker():
    # ChatGPT tests this
    concept = generate_concept()
    response = requests.post(
        "http://localhost:8000/api/v1/content/validate",
        json=concept.model_dump(),  # Pydantic v2
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer dev-key-research-portal",
            "Idempotency-Key": str(uuid.uuid4())
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["overall_score"] >= 85
    assert len(data["data"]["gates"]) == 4
    assert data["data"]["passes_quality"] == True
```

### Quality Gate Tests

```python
# Test quality gates enforcement
def test_quality_gates():
    # Test coverage_score gate
    concept_low_coverage = create_concept(coverage_score=0.5)
    report = validate_content(concept_low_coverage)
    assert report.gates[0]["passed"] == False
    assert report.passes_quality == False

    # Test citation_density gate
    concept_low_citation = create_concept(citation_density=0.8)
    report = validate_content(concept_low_citation)
    assert report.gates[1]["passed"] == False
    assert report.passes_quality == False

    # Test exec_ok gate
    concept_bad_code = create_concept(code_with_errors=True)
    report = validate_content(concept_bad_code)
    assert report.gates[2]["passed"] == False
    assert report.passes_quality == False
```

### Test Coverage Targets

- Unit tests: 70%+ coverage
- Integration tests: All API endpoints
- Smoke tests: All critical paths
- Quality gate tests: All 4 gates tested
- Authentication tests: Valid/invalid API keys
- Idempotency tests: Duplicate requests cached

---

## 📅 Integration Schedule

### Day 6 (Nov 11): Individual Testing

**Morning (AM):**
- Claude tests Quality Checker endpoints (10 criteria + gates)
- ChatGPT tests Research Portal endpoints (AethelgardConcept)
- Both systems run locally with authentication

**Afternoon (PM):**
- First integration attempt
- Research Portal → Quality Checker
- Fix format mismatches
- Verify authentication works
- Test idempotency caching

### Day 7 (Nov 12): Full Integration

**Morning (AM):**
- Quality Checker → Backend (quality filtering)
- AXIS AI → Backend (retrieval with quality scores)
- Complete flow testing
- Test batch validation

**Afternoon (PM):**
- Bug fixes
- Performance testing (< 3s per validation)
- Deployment prep
- Verify telemetry tracking

---

## 🚨 Emergency Protocol

**If integration fails badly on Day 6:**

### Fallback Plan

1. **Assess** (5 PM IST):
   ```
   Asheesh: "Is integration possible by end of Day 7?"
   Claude + ChatGPT: Honest assessment
   ```

2. **Decision**:
   - ✅ **If yes**: Continue, work late if needed
   - ❌ **If no**: Activate fallback

3. **Fallback** (if integration impossible):
   - Focus on Quality Checker + Research Portal only
   - Skip AXIS AI integration
   - Simplified brother demo (content generation + validation)
   - Return to full 10-week plan on Nov 17

### Decision Criteria

**Continue if:**
- Systems can exchange data (even if buggy)
- Bugs are fixable in <4 hours
- Core functionality works
- Authentication works
- Quality gates work

**Fallback if:**
- Fundamental architecture mismatch
- Would take >1 day to fix
- Data formats completely incompatible
- Authentication broken beyond quick fix

---

## ✅ Success Criteria

**Developer Contract succeeds if:**

- ✅ Systems integrate on first attempt (or within 2 hours)
- ✅ No data format errors (Pydantic v2 validation passes)
- ✅ No import errors (AethelgardConcept used consistently)
- ✅ Authentication works without issues
- ✅ API calls work without URL changes
- ✅ Both code bases have consistent style
- ✅ Integration takes <2 days (not 1 week)
- ✅ No "it works on my machine" issues
- ✅ Quality gates enforce minimum standards
- ✅ Telemetry tracking works (LangSmith)

**Metrics:**
- Time to integration: <2 days
- Format errors: <5 total
- API mismatches: <3 total
- Integration bugs: <10 total
- Quality gate failures: Intentional (testing enforcement)
- Authentication errors: 0 (must work perfectly)

---

## 📝 Version History

**v1.0 (2025-11-06):**
- Initial developer contract
- Work division defined
- Technology stack agreed
- Code style standards set
- Communication protocol established
- Testing agreement defined
- Emergency protocol created

**v2.0 (2025-11-06):**
- **PRODUCTION-GRADE UPGRADE**
- Updated: 7-criterion → 10-criterion rubric (100 points)
- Raised: Pass threshold 70 → 85
- Added: 4 quality gates (coverage, citation, exec_ok, scope_ok)
- Renamed: PythonConcept → AethelgardConcept (BREAKING CHANGE)
- Added: CodeExample, Citation, CitationSource, Mode, Library models
- Added: Authentication system (Bearer tokens, 4 API keys)
- Added: Idempotency support (24-hour cache, validation endpoints)
- Added: Telemetry integration (LangSmith, 14 metrics)
- Added: Batch validation (Quick/Full modes, max 100 items)
- Updated: Pydantic v1 → v2 (.dict() → .model_dump())
- Updated: All code examples to v2.0 format
- Updated: Testing section with quality gate tests
- Updated: Integration schedule with v2.0 features
- Updated: Success criteria with v2.0 metrics
- Updated: File structure with complete contracts/ folder
- Expanded: Handoff checklist with v2.0 requirements
- Expanded: Communication protocol with migration examples

---

## 🔗 Related Documents

- `shared_models.py` v2.0 - Shared data structures (660 lines)
- `api_research_portal.py` v2.0 - Research Portal API contract (477 lines)
- `api_questionforge.py` v2.0 - QuestionForge API contract (541 lines)
- `api_backend.py` v2.0 - Backend API contract (728 lines)
- `api_axis.py` v2.0 - AXIS AI API contract (677 lines)
- `SYSTEM_ARCHITECTURE.md` v2.0 - System architecture (997 lines)
- `DECISIONS.md` - Decision log (created during development)

**Total API Contract Documentation:** 4,080 lines (v2.0)

---

**Signed** (Virtually):
- Claude Code (Lead Architect)
- ChatGPT (Developer, via Asheesh)
- Asheesh (Mediator & Final Decision Maker)

**Date**: 2025-11-06
**Effective**: Immediate (Experimental Phase)
**Review Date**: 2025-11-17 (Decision Point)
**Version**: 2.0 (Production-grade upgrade)
