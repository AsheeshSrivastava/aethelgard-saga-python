# Quality Checker Service

**Built By:** 🟢 Claude Code
**Status:** 🔨 Week 1 Implementation (Nov 13-19, 2025)

---

## Overview

FastAPI service that validates educational content and questions against production-grade quality standards.

**Tech Stack:**
- FastAPI 0.120.4
- Gradio 4.44.1 (UI)
- Pydantic 2.x
- LangSmith (telemetry)
- Pyodide (code execution sandbox)

---

## Features

### Content Validation
- ✅ 10-criterion rubric (100 points total)
- ✅ 4 quality gates (coverage, citation, exec_ok, scope_ok)
- ✅ Pass threshold: 85
- ✅ Telemetry: 14 metrics tracked

### Question Validation
- ✅ 7-8 criteria (type-dependent)
- ✅ Test case validation for code questions
- ✅ Multiple choice validation
- ✅ Bloom's taxonomy alignment

### API Endpoints
- `POST /api/v1/content/validate` - Single content
- `POST /api/v1/content/batch-validate` - Batch (max 100)
- `POST /api/v1/questions/validate` - Single question
- `POST /api/v1/questions/batch-validate` - Batch (max 100)

### Security
- ✅ Bearer token authentication
- ✅ 4 API keys (Research Portal, QuestionForge, Backend, AXIS)
- ✅ Rate limiting
- ✅ Idempotency support (24-hour cache)

---

## Directory Structure (Coming Soon)

```
quality-checker/
├── main.py              # FastAPI app
├── api/                 # API routes
│   ├── content.py       # Content validation endpoints
│   └── questions.py     # Question validation endpoints
├── services/            # Business logic
│   ├── content_validator.py
│   ├── question_validator.py
│   └── telemetry.py
├── models/              # Pydantic models (import from contracts)
├── ui/                  # Gradio interface
│   └── app.py
├── tests/               # Test suite
└── README.md            # This file
```

---

## Running Locally

```bash
cd quality-checker
uvicorn main:app --reload --port 8000
```

Access Gradio UI: http://localhost:8000/ui

---

## Implementation Timeline

**Week 1 (Nov 13-19, 2025):**
- Day 1-2: Core validation logic
- Day 3-4: API endpoints + authentication
- Day 5: Gradio UI
- Day 6: Telemetry integration
- Day 7: Testing + documentation

---

**Status:** 🔨 Awaiting implementation by Claude Code
