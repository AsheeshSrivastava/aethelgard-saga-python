# Research Portal Service

**Built By:** 🔵 ChatGPT
**Status:** 🔨 Week 2-3 Implementation (Nov 20 - Dec 3, 2025)

---

## Overview

AI-powered service that generates educational content (concepts, questions) using RAG (Retrieval-Augmented Generation) and validates them through the Quality Checker.

**Tech Stack:**
- Python 3.11+
- OpenAI API (GPT-4o-latest)
- LlamaIndex 0.9.14 (RAG orchestration)
- LangChain 1.0.3 (agent framework)
- LanceDB (vector database)

---

## Features

### Content Generation
- ✅ PSW framework content (Problem-System-Win)
- ✅ Code examples with expected output
- ✅ Citation extraction from vector database
- ✅ Difficulty assessment
- ✅ Mode-specific content (Coach/Hybrid/Socratic)

### Question Generation
- ✅ 5 question types (Knowledge Check, Code Writing, Debugging, Code Reading, Mini-Project)
- ✅ Test case generation for code questions
- ✅ Multiple choice with distractors
- ✅ Bloom's taxonomy alignment

### Quality Integration
- ✅ Automatic validation via Quality Checker API
- ✅ Iterative refinement based on feedback
- ✅ Batch generation with validation

---

## Directory Structure (Coming Soon)

```
research-portal/
├── main.py                    # Entry point
├── services/
│   ├── content_generator.py   # Content generation logic
│   ├── question_generator.py  # Question generation logic
│   ├── rag_system.py          # RAG integration
│   └── quality_client.py      # Quality Checker API client
├── prompts/                   # LLM prompts
│   ├── content_prompts.py
│   └── question_prompts.py
├── data/
│   └── curriculum_context.json # Curriculum reference
├── tests/
└── README.md                  # This file
```

---

## Running Locally

```bash
cd research-portal
python main.py
```

---

## Implementation Timeline

**Week 2 (Nov 20-26, 2025):**
- Day 1-2: RAG system setup (LlamaIndex + LanceDB)
- Day 3-4: Content generation logic
- Day 5-6: Question generation logic
- Day 7: Quality Checker integration

**Week 3 (Nov 27 - Dec 3, 2025):**
- Day 1-2: Iterative refinement system
- Day 3-4: Batch generation pipeline
- Day 5-6: Testing + optimization
- Day 7: Documentation

---

## Integration with Quality Checker

```python
from services.quality_client import QualityClient

# Generate content
concept = generate_concept("Variables")

# Validate via Quality Checker
client = QualityClient(api_key=os.getenv("RESEARCH_PORTAL_API_KEY"))
report = client.validate_content(concept)

# Check if passed
if report.passes_quality:
    print(f"✅ Content passed with score {report.overall_score}")
else:
    print(f"❌ Content failed. Issues: {report.issues}")
    # Refine and retry
```

---

**Status:** 🔨 Awaiting implementation by ChatGPT
