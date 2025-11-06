# Contracts - Simple Instructions for Asheesh

**Created**: 2025-11-06
**Status**: Ready to use

---

## What Are These Files?

These are the "agreements" between all systems so they can talk to each other.

**Think of it like**: International shipping standards - everyone agrees on container sizes, so any ship can carry any container.

---

## What YOU Need to Do (Simple 3 Steps)

### Step 1: Tomorrow Morning (After I finish all contracts)

I'll tell you: "Contracts are ready!"

### Step 2: Copy to ChatGPT (5 minutes)

1. Open `contracts/shared_models.py`
2. Copy the ENTIRE file
3. Paste into ChatGPT
4. Say:

```
"I'm building Research Portal and AXIS AI.
Use THESE EXACT models (PythonConcept, Question, QualityReport).
Do not create your own data structures.
Import from: contracts/shared_models.py"
```

### Step 3: That's It!

You're done. ChatGPT will now build code that matches MY code automatically.

---

## Files in This Folder

```
contracts/
├── README_FOR_ASHEESH.md          ← You are here
├── shared_models.py               ← THE FOUNDATION (all data structures)
├── DEVELOPER_CONTRACT.md          ← How Claude + ChatGPT coordinate
├── api_research_portal.py         ← Research Portal → Quality Checker
├── api_questionforge.py           ← QuestionForge → Quality Checker
├── api_backend.py                 ← Backend → Quality Checker
└── api_axis.py                    ← AXIS AI → Backend
```

---

## What Each File Does

### `shared_models.py` ⭐ MOST IMPORTANT

**Contains:**
- `PythonConcept` - Data structure for Python concepts
- `Question` - Data structure for questions
- `QualityReport` - Data structure for validation results
- `ValidationRequest/Response` - API request/response formats
- `ErrorResponse/SuccessResponse` - Standard error/success formats

**Who Uses It:**
- Research Portal (ChatGPT builds) ✅
- QuestionForge (existing system) ✅
- Quality Checker (Claude builds) ✅
- Aethelgard Backend (ChatGPT builds) ✅
- AXIS AI (ChatGPT builds) ✅

**Rule**: EVERYONE imports from this file. NO ONE creates their own data structures.

---

### `DEVELOPER_CONTRACT.md`

**What**: Rules for how Claude and ChatGPT work together

**Contains:**
- Who builds what
- Code style rules (so code looks consistent)
- How to ask each other questions (via you)
- What to do if something breaks

**You need to know**: If ChatGPT wants to change something in `shared_models.py`, they must ask me first (via you).

---

### API Contract Files (4 files)

**What**: Specific rules for each system connection

**Example:** `api_research_portal.py` says:
- Research Portal sends `PythonConcept` to endpoint `/api/validate-content`
- Quality Checker returns `QualityReport`
- If error, returns `ErrorResponse`

**You need to know**: Nothing! These are reference docs. ChatGPT and I follow them automatically.

---

## When to Use These

### During Development (Days 3-5)

**ChatGPT building Research Portal:**
```python
# ChatGPT's code
from contracts.shared_models import PythonConcept, QualityReport
import requests

def generate_concept() -> PythonConcept:
    # ... generation logic ...
    concept = PythonConcept(
        concept_id="python-variables-01",
        title="Variables",
        problem="How do you store data?",
        system="Use variables like x = 5",
        win="Now you can store and reuse data",
        code_examples=["x = 5", "name = 'Alice'"],
        difficulty="beginner",
        prerequisites=[],
        tags=["basics"]
    )
    return concept

def validate_concept(concept: PythonConcept) -> QualityReport:
    import uuid
    response = requests.post(
        "http://localhost:8000/api/v1/content/validate",
        json=concept.model_dump(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {RESEARCH_PORTAL_API_KEY}",
            "Idempotency-Key": str(uuid.uuid4())
        }
    )
    data = response.json()['data']  # Extract from SuccessResponse
    return QualityReport(**data)
```

**My code (Quality Checker):**
```python
# Claude's code (Production v2.0)
from contracts.shared_models import PythonConcept, QualityReport, QualityGate, Telemetry, SuccessResponse
from fastapi import FastAPI

app = FastAPI()

@app.post("/api/v1/content/validate", response_model=SuccessResponse)
def validate_content(concept: PythonConcept):
    # ... validation logic with 10-criterion rubric ...

    # 10 criteria scoring
    groundedness_citation = 18  # /20
    technical_correctness = 14  # /15
    people_first_pedagogy = 13  # /15
    psw_actionability = 9       # /10
    mode_fidelity = 9           # /10
    self_paced_scaffolding = 9  # /10
    retrieval_quality = 9       # /10
    clarity = 4                 # /5
    bloom_alignment = 3         # /3
    people_first_language = 2   # /2

    overall_score = sum([...])  # = 90

    # 4 quality gates (must ALL pass)
    gates = [
        QualityGate(name="coverage_score", threshold=0.65, actual=0.75, passed=True),
        QualityGate(name="citation_density", threshold=1.0, actual=1.5, passed=True),
        QualityGate(name="exec_ok", threshold=True, actual=True, passed=True),
        QualityGate(name="scope_ok", threshold=True, actual=True, passed=True)
    ]

    # Pass logic: score ≥85 AND all gates passed
    passes_quality = (overall_score >= 85) and all([g.passed for g in gates])

    # Telemetry (14 metrics tracked)
    telemetry = Telemetry(
        run_id="run_abc123",
        model="gpt-4o-latest",
        provider="openai",
        prompt_version="v2.0",
        graph_version="1.0",
        coverage_score=0.75,
        citation_density=1.5,
        unique_sources=2,
        mode_ratio=0.8,
        scaffold_depth=3,
        exec_ok=True,
        latency_ms=2500,
        tokens=3200
    )

    quality_report = QualityReport(
        item_id=concept.concept_id,
        item_type="content",
        overall_score=overall_score,
        criterion_scores={
            "groundedness_citation": groundedness_citation,
            "technical_correctness": technical_correctness,
            "people_first_pedagogy": people_first_pedagogy,
            "psw_actionability": psw_actionability,
            "mode_fidelity": mode_fidelity,
            "self_paced_scaffolding": self_paced_scaffolding,
            "retrieval_quality": retrieval_quality,
            "clarity": clarity,
            "bloom_alignment": bloom_alignment,
            "people_first_language": people_first_language
        },
        gates=gates,
        telemetry=telemetry,
        issues=[],
        strengths=["Clear PSW structure", "Excellent code examples"],
        suggestions=["Add more real-world applications"],
        passes_quality=passes_quality,
        validated_at="2025-11-08T10:30:00Z"
    )

    return SuccessResponse(data=quality_report)
```

**Result**: They plug together perfectly! No integration errors.

---

### During Integration (Days 6-7)

You don't do anything special. Systems just work because they follow the same contracts.

**If something breaks:**
1. Check if both systems use `shared_models.py`
2. Check if endpoint URLs match
3. Ask me: "Claude, Research Portal is calling `/validate` but Quality Checker expects `/api/validate-content`. Fix?"
4. I fix it in 2 minutes

---

## Quality Framework v2.0 (Simple Explanation)

**What Changed**: Claude upgraded Quality Checker to production-grade standards.

**3 Key Things to Know:**

### 1. 10-Criterion Rubric (Total: 100 points)

Quality Checker evaluates content on 10 criteria:
- **Groundedness & Citation** (20 points) - Cited sources, accurate references
- **Technical Correctness** (15 points) - Code works, no errors
- **People-First Pedagogy** (15 points) - Learner-friendly, self-paced
- **PSW Actionability** (10 points) - Problem-System-Win framework
- **Mode Fidelity** (10 points) - Coach/Hybrid/Socratic alignment
- **Self-Paced Scaffolding** (10 points) - Progressive complexity
- **Retrieval Quality** (10 points) - RAG search effectiveness
- **Clarity** (5 points) - Easy to understand
- **Bloom Alignment** (3 points) - Cognitive level appropriate
- **People-First Language** (2 points) - Encouraging, inclusive

**Pass Threshold**: ≥85 points (raised from 70)

### 2. 4 Quality Gates (Must ALL Pass)

Even if content scores 90 points, it FAILS if any gate fails:
- **coverage_score ≥0.65** - RAG retrieval quality threshold
- **citation_density ≥1.0** - Minimum 1 citation per concept
- **exec_ok = true** - All code examples execute successfully
- **scope_ok = true** - Only approved libraries used (numpy, pandas, matplotlib, seaborn, scikit-learn)

**Example**: Content scores 90 but uses `import requests` (unapproved) → FAILS (scope_ok gate failed)

### 3. Telemetry (14 Metrics Tracked)

Every validation includes telemetry for observability:
- Run metadata (run_id, model, provider, prompt_version)
- Quality metrics (coverage_score, citation_density, unique_sources)
- Pedagogy metrics (mode_ratio, scaffold_depth, exec_ok)
- Performance metrics (latency_ms, tokens)

**You don't need to do anything** - Quality Checker handles this automatically.

### Code Sandbox Constraints

All code examples run in secure Pyodide sandbox:
- **Timeout**: 5 seconds max per example
- **Memory**: 50 MB limit
- **No network access** - No HTTP requests allowed
- **No file writes** - Read-only environment
- **Approved libraries only** - core-python, numpy, pandas, matplotlib, seaborn, scikit-learn

### Web Citation Allowlist

Pre-approved citation sources:
- docs.python.org, ocw.mit.edu, www.cmu.edu (academic/official)
- realpython.com, stackoverflow.com, github.com, medium.com (community)

Non-allowlisted sources flagged for manual review (1-3 day approval process).

**Bottom Line**: Quality Checker is now production-grade. Content must meet higher standards, but integration works the same way.

---

## FAQ

### Q: Can I modify `shared_models.py`?

**A**: NO. Tell me what you need, I'll update it and notify ChatGPT.

### Q: Can ChatGPT modify `shared_models.py`?

**A**: NO. ChatGPT must ask me (via you). I update, then notify everyone.

### Q: What if I forget to give ChatGPT the contracts?

**A**: ChatGPT will create their own data structures. Integration will break on Day 6. Give them the contracts tomorrow morning!

### Q: Do I need to understand all the code in these files?

**A**: NO. You just need to:
1. Copy `shared_models.py` to ChatGPT
2. Tell ChatGPT: "Use these exact models"
3. That's it!

---

## Quick Checklist

**Before starting any development:**
- [ ] contracts/ folder exists
- [ ] shared_models.py created
- [ ] ChatGPT has copy of shared_models.py
- [ ] ChatGPT confirmed they'll use it
- [ ] I (Claude) confirmed Quality Checker uses it

**If all checked**: ✅ You're ready to build!

---

## What Happens Next?

**Tonight (while you're in bootcamp):**
- I finish all 7 contract files
- I create system architecture diagram
- I create integration checklist

**Tomorrow morning (30 min):**
- You copy `shared_models.py` to ChatGPT
- You start building Research Portal (with ChatGPT)
- I start building Quality Checker

**Days 3-5:**
- Parallel development (no integration yet)
- Both systems built independently
- Both follow same contracts

**Days 6-7:**
- Integration (plug systems together)
- Should work on first try (because contracts)
- Fix any small bugs

**Nov 17:**
- Decision point: Success or fallback to 10-week plan

---

**Remember**: I'm the architect. You focus on bootcamp and building. I handle all coordination.

**Questions?** Just ask: "Claude, what do I do with [file]?" and I'll give you 1-2 sentence answer.
