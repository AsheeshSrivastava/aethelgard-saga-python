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
    response = requests.post(
        "http://localhost:8000/api/validate-content",
        json=concept.dict()
    )
    return QualityReport(**response.json())
```

**My code (Quality Checker):**
```python
# Claude's code
from contracts.shared_models import PythonConcept, QualityReport
from fastapi import FastAPI

app = FastAPI()

@app.post("/api/validate-content", response_model=QualityReport)
def validate_content(concept: PythonConcept):
    # ... validation logic ...
    return QualityReport(
        item_id=concept.concept_id,
        item_type="content",
        overall_score=85,
        psw_score=28,
        code_quality_score=27,
        clarity_score=14,
        adult_learning_score=12,
        people_first_score=9,
        rag_optimization_score=18,
        issues=[],
        strengths=["Clear PSW structure"],
        suggestions=["Add more examples"],
        passes_quality=True,
        validated_at="2025-11-08T10:30:00Z"
    )
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
