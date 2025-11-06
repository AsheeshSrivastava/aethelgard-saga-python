# Backend API Service

**Built By:** 🔵 ChatGPT
**Status:** 🔨 Week 4-7 Implementation (Dec 4-31, 2025)

---

## Overview

Main RESTful API that serves validated educational content to the frontend (Aethelgard_Saga React app) and integrates with AXIS AI for personalized learning experiences.

**Tech Stack:**
- FastAPI 0.120.4
- PostgreSQL/Supabase (database)
- Pydantic 2.x (data validation)
- OpenAI API (for AXIS AI integration)

---

## Features

### Content Management
- ✅ CRUD operations for concepts
- ✅ CRUD operations for questions
- ✅ Content search & filtering
- ✅ Prerequisite dependency graph

### User Progress
- ✅ Concept completion tracking
- ✅ XP & leveling system
- ✅ Achievement tracking
- ✅ Learning path recommendations

### AXIS AI Integration
- ✅ Context-aware chat
- ✅ Mode switching (Coach/Hybrid/Socratic)
- ✅ Exercise feedback & hints
- ✅ Personalized learning path

### Quality Assurance
- ✅ Only serves validated content (from Quality Checker)
- ✅ Content versioning
- ✅ A/B testing support

---

## Directory Structure (Coming Soon)

```
backend-api/
├── main.py                    # FastAPI app
├── api/
│   ├── concepts.py            # Concept endpoints
│   ├── questions.py           # Question endpoints
│   ├── progress.py            # User progress endpoints
│   └── axis.py                # AXIS AI endpoints
├── services/
│   ├── content_service.py
│   ├── progress_service.py
│   └── axis_service.py
├── database/
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   └── migrations/
├── tests/
└── README.md                  # This file
```

---

## API Endpoints (Planned)

### Content Endpoints
- `GET /api/concepts` - List all concepts
- `GET /api/concepts/{id}` - Get concept by ID
- `GET /api/concepts/{id}/questions` - Get questions for concept
- `GET /api/questions/{id}` - Get question by ID

### Progress Endpoints
- `POST /api/progress/complete-concept` - Mark concept complete
- `GET /api/progress/user/{user_id}` - Get user progress
- `GET /api/progress/learning-path` - Get recommended learning path

### AXIS AI Endpoints
- `POST /api/axis/chat` - Send message to AXIS AI
- `POST /api/axis/set-mode` - Change AXIS mode
- `POST /api/axis/get-hint` - Get exercise hint
- `POST /api/axis/explain-code` - Explain code snippet

---

## Running Locally

```bash
cd backend-api
uvicorn main:app --reload --port 8001
```

Access API docs: http://localhost:8001/docs

---

## Database Schema (Planned)

### concepts
- id, concept_id, title, problem, system, win
- code_examples (JSON), citations (JSON)
- difficulty, prerequisites, tags
- mode, libraries
- created_at, updated_at, validated_at

### questions
- id, question_id, concept_id, type
- question_text, options (JSON), test_cases (JSON)
- bloom_level, difficulty
- validated_at

### user_progress
- user_id, concept_id, completed
- completion_date, xp_earned
- reflections (JSON)

### achievements
- user_id, achievement_id, unlocked_at

---

## Implementation Timeline

**Week 4-5 (Dec 4-17, 2025):**
- Day 1-3: Database schema + migrations
- Day 4-7: Content CRUD endpoints
- Day 8-10: User progress tracking
- Day 11-14: Testing + optimization

**Week 6-7 (Dec 18-31, 2025):**
- Day 1-4: AXIS AI integration
- Day 5-7: Learning path recommendations
- Day 8-10: A/B testing support
- Day 11-14: Testing + documentation

---

## Integration with Quality Checker

Backend only serves content that has been validated:

```python
# When adding new content to database
if not concept.validated_at:
    raise ValueError("Content must be validated before adding to database")

# Check validation status
if quality_report.passes_quality and quality_report.overall_score >= 85:
    concept.validated_at = datetime.utcnow()
    db.add(concept)
```

---

**Status:** 🔨 Awaiting implementation by ChatGPT (after Research Portal complete)
