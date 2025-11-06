"""
API Contract: Aethelgard Backend ↔ Quality Checker
===================================================

**System A:** Aethelgard Backend (ChatGPT builds)
**System B:** Quality Checker (Claude builds)

**Purpose:** Backend requests batch validation or re-validation of content/questions before serving to AXIS AI.

**Version:** 2.0
**Created:** 2025-11-06
**Updated:** 2025-11-06 (Production-grade upgrade)
"""

from shared_models import (
    AethelgardConcept,  # Was PythonConcept
    Question,
    QualityReport,
    BatchValidationRequest,
    BatchValidationResponse,
    create_success_response,
    create_error_response
)
from typing import Dict, Any, List
import requests
import uuid
import os

# ============================================================================
# ENDPOINT SPECIFICATIONS
# ============================================================================

# Single item validation (same as Research Portal/QuestionForge)
VALIDATE_CONTENT_ENDPOINT = "POST /api/v1/content/validate"
VALIDATE_QUESTION_ENDPOINT = "POST /api/v1/questions/validate"

# Batch validation (backend-specific)
BATCH_VALIDATE_ENDPOINT = "POST /api/v1/content/batch-validate"

# Get validated content (backend serves this to AXIS AI)
GET_VALIDATED_ENDPOINT = "GET /api/v1/content/{id}"
LIST_VALIDATED_ENDPOINT = "GET /api/v1/content/list"

BASE_URL = "http://localhost:8000"  # Quality Checker URL

# Authentication (set in environment)
BACKEND_API_KEY = os.getenv("BACKEND_API_KEY", "dev-key-backend")

# ============================================================================
# BATCH VALIDATION (Backend Optimization)
# ============================================================================

def batch_validate(items: List[AethelgardConcept | Question], idempotency_key: str = None) -> Dict[str, Any]:
    """
    Validate multiple items at once (more efficient for backend).

    Args:
        items: List of AethelgardConcept or Question objects (max 100)
        idempotency_key: Optional UUID for idempotent requests (generated if not provided)

    Returns:
        Dict with batch validation results

    Example:
        >>> concepts = [concept1, concept2, concept3]
        >>> result = batch_validate(concepts)
        >>> print(f"{result['data']['passed']}/{result['data']['total_items']} passed")
        2/3 passed
    """
    # Generate idempotency key if not provided
    if idempotency_key is None:
        idempotency_key = str(uuid.uuid4())

    batch_request = BatchValidationRequest(
        items=items,
        validation_type="full"  # or "quick" for faster basic checks
    )

    response = requests.post(
        f"{BASE_URL}/api/v1/content/batch-validate",
        json=batch_request.model_dump(),  # Pydantic v2: .model_dump() instead of .dict()
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {BACKEND_API_KEY}",
            "Idempotency-Key": idempotency_key
        },
        timeout=10  # Prevent hanging connections
    )
    return response.json()


# ============================================================================
# BATCH VALIDATION RESPONSE FORMAT
# ============================================================================

# SUCCESS RESPONSE (Status 200)
"""
{
    "status": "success",
    "message": "Batch validation completed",
    "data": {
        "total_items": 3,
        "passed": 2,
        "failed": 1,
        "reports": [
            {
                "item_id": "python-variables-01",
                "item_type": "content",
                "overall_score": 87,

                // 10-Criterion Rubric (100 points total)
                "groundedness_citation_score": 18,
                "technical_correctness_score": 14,
                "people_first_pedagogy_score": 13,
                "psw_actionability_score": 9,
                "mode_fidelity_score": 9,
                "self_paced_scaffolding_score": 8,
                "retrieval_quality_score": 9,
                "clarity_score": 4,
                "bloom_alignment_score": 2,
                "people_first_language_score": 1,

                // Quality Gates
                "gates": [
                    {"name": "coverage_score", "passed": true, "details": "0.72 >= 0.65"},
                    {"name": "citation_density", "passed": true, "details": "1.2 >= 1.0"},
                    {"name": "exec_ok", "passed": true, "details": "All code executed"},
                    {"name": "scope_ok", "passed": true, "details": "Libraries approved"}
                ],

                // Telemetry
                "telemetry": {
                    "run_id": "run_abc123",
                    "model": "gpt-4o-2024-11-20",
                    "coverage_score": 0.72,
                    "citation_density": 1.2,
                    "exec_ok": true,
                    ...
                },

                "passes_quality": true,
                "validator_version": "2.0"
            },
            {
                "item_id": "python-datatypes-01",
                "item_type": "content",
                "overall_score": 82,
                "passes_quality": false,  // overall_score < 85 OR gate failed
                ...
            },
            {
                "item_id": "q-variables-mc-01",
                "item_type": "question",
                "overall_score": 88,
                "passes_quality": true,
                ...
            }
        ],
        "timestamp": "2025-11-08T12:00:00Z"
    },
    "timestamp": "2025-11-08T12:00:00Z"
}
"""

# ============================================================================
# EXAMPLE USAGE (Backend Side)
# ============================================================================

async def backend_validation_workflow():
    """
    Example workflow in Aethelgard Backend:
    1. Receive content from Research Portal
    2. Batch validate before storing
    3. Store only validated content
    4. Serve validated content to AXIS AI
    """
    # Step 1: Receive concepts from Research Portal
    from shared_models import CodeExample, Citation, CitationSource, Mode, Library

    concepts = [
        AethelgardConcept(
            concept_id="python-variables-01",
            title="Variables",
            problem="You need to store data like a user's age...",
            system="Variables in Python work like labeled boxes...",
            win="Now you can store any data...",
            code_examples=[
                CodeExample(
                    code="age = 25\nprint(age)",
                    expected_output="25",
                    runnable=True
                )
            ],
            provisional_citations=[
                Citation(
                    source=CitationSource.VECTOR,
                    title="Python Tutorial §2.1",
                    locator="§2.1.1"
                )
            ],
            difficulty="beginner",
            mode=Mode.COACH,
            libraries=[Library.CORE_PYTHON]
        ),
        AethelgardConcept(
            concept_id="python-datatypes-01",
            title="Data Types",
            problem="How do you represent different kinds of data?",
            system="Python has built-in data types...",
            win="You can choose the right type for your data",
            code_examples=[
                CodeExample(
                    code="x = 42\nprint(type(x))",
                    expected_output="<class 'int'>",
                    runnable=True
                )
            ],
            provisional_citations=[],
            difficulty="beginner",
            mode=Mode.COACH,
            libraries=[Library.CORE_PYTHON]
        )
    ]

    # Step 2: Batch validate
    try:
        result = batch_validate(concepts)

        if result['status'] == 'success':
            data = result['data']

            print(f"✅ Validated {data['total_items']} items")
            print(f"   Passed: {data['passed']}")
            print(f"   Failed: {data['failed']}")

            # Step 3: Store only passed items
            for report in data['reports']:
                if report['passes_quality']:
                    concept_id = report['item_id']
                    # await store_validated_content(concept_id, report)
                    print(f"   ✓ Stored {concept_id} (Score: {report['overall_score']})")

                    # Check gates
                    gates = report.get('gates', [])
                    failed_gates = [g for g in gates if not g['passed']]
                    if failed_gates:
                        print(f"     ⚠️ Failed gates: {[g['name'] for g in failed_gates]}")
                else:
                    print(f"   ✗ Rejected {report['item_id']} (Score: {report['overall_score']})")

        else:
            print(f"❌ Batch validation error: {result['error']}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")


# ============================================================================
# RE-VALIDATION WORKFLOW
# ============================================================================

async def revalidate_existing_content():
    """
    Backend can request re-validation of existing content.

    Use cases:
    - Quality standards updated (e.g., threshold raised to 85)
    - Bug fix in validation logic
    - Periodic quality audits
    - New gates added (e.g., citation_density ≥1.0)
    """
    # Get all stored content
    # existing_concepts = await get_all_concepts_from_db()

    # Re-validate with current standards
    # result = batch_validate(existing_concepts)

    # Update quality scores in database
    # for report in result['data']['reports']:
    #     await update_quality_score(report['item_id'], report)
    #
    #     # Flag content that no longer passes
    #     if not report['passes_quality']:
    #         await mark_for_revision(report['item_id'], report['issues'])

    pass


# ============================================================================
# SERVING VALIDATED CONTENT TO AXIS AI
# ============================================================================

async def get_validated_content_for_axis(concept_id: str) -> Dict[str, Any]:
    """
    Backend serves validated content to AXIS AI.

    Only content with passes_quality=True AND overall_score ≥ 85 is served.
    """
    # Get from database (backend's own database)
    # concept = await db.get_concept(concept_id)

    # Check if validated
    # if not concept.quality_report.passes_quality:
    #     raise HTTPException(404, "Content not validated")

    # Check minimum score
    # if concept.quality_report.overall_score < 85:
    #     raise HTTPException(404, "Content below quality threshold")

    # Return to AXIS AI
    # return concept.model_dump()  # Pydantic v2

    pass


async def list_validated_content(
    difficulty: str = None,
    tags: List[str] = None,
    min_score: int = 85,  # Raised from 70 to 85
    min_citation_density: float = None
) -> List[Dict[str, Any]]:
    """
    Backend provides list of validated content to AXIS AI.

    Filters:
    - difficulty: beginner/intermediate/advanced
    - tags: filter by tags
    - min_score: minimum quality score (default 85, raised from 70)
    - min_citation_density: minimum citation density (e.g., 1.0)
    """
    # Query database
    # concepts = await db.query_concepts(
    #     difficulty=difficulty,
    #     tags=tags,
    #     min_quality_score=min_score,
    #     min_citation_density=min_citation_density
    # )

    # Return list
    # return [c.model_dump() for c in concepts]  # Pydantic v2

    pass


# ============================================================================
# CURL EXAMPLES (For Testing)
# ============================================================================

"""
# Batch Validation
curl -X POST http://localhost:8000/api/v1/content/batch-validate \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer dev-key-backend" \\
  -H "Idempotency-Key: $(uuidgen)" \\
  -d '{
    "items": [
      {
        "concept_id": "python-variables-01",
        "title": "Variables",
        "problem": "You need to store data like a user age...",
        "system": "Variables in Python work like labeled boxes...",
        "win": "Now you can store any data...",
        "code_examples": [
          {
            "code": "age = 25\\nprint(age)",
            "expected_output": "25",
            "runnable": true
          }
        ],
        "provisional_citations": [
          {
            "source": "vector",
            "title": "Python Tutorial §2.1",
            "locator": "§2.1.1"
          }
        ],
        "difficulty": "beginner",
        "mode": "coach",
        "libraries": ["core-python"],
        "prerequisites": [],
        "tags": ["basics"]
      },
      {
        "concept_id": "python-datatypes-01",
        "title": "Data Types",
        "problem": "How do you represent different kinds of data?",
        "system": "Python has built-in data types...",
        "win": "You can choose the right type for your data",
        "code_examples": [
          {
            "code": "x = 42\\nprint(type(x))",
            "expected_output": "<class 'int'>",
            "runnable": true
          }
        ],
        "provisional_citations": [],
        "difficulty": "beginner",
        "mode": "coach",
        "libraries": ["core-python"],
        "prerequisites": ["python-variables-01"],
        "tags": ["basics"]
      }
    ],
    "validation_type": "full"
  }'

# Get Validated Content (from Backend to AXIS AI)
curl -X GET http://localhost:9000/api/v1/content/python-variables-01

# List Validated Content
curl -X GET "http://localhost:9000/api/v1/content/list?difficulty=beginner&min_score=85&min_citation_density=1.0"
"""

# ============================================================================
# QUALITY CHECKER IMPLEMENTATION (Reference)
# ============================================================================

"""
# Quality Checker side (FastAPI)

from fastapi import FastAPI, Header, HTTPException
from shared_models import (
    BatchValidationRequest,
    BatchValidationResponse,
    QualityReport
)

app = FastAPI()

@app.post("/api/v1/content/batch-validate")
async def batch_validate(
    request: BatchValidationRequest,
    authorization: str = Header(...),
    idempotency_key: str = Header(None)
):
    # Verify API key
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    api_key = authorization.split("Bearer ")[1]
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Check idempotency
    if idempotency_key:
        cached_result = check_idempotency_cache(idempotency_key)
        if cached_result:
            return cached_result

    reports = []
    passed = 0
    failed = 0

    for item in request.items:
        if isinstance(item, AethelgardConcept):  # Was PythonConcept
            report = await quality_checker.validate_content(item)
        elif isinstance(item, Question):
            report = await quality_checker.validate_question(item)

        reports.append(report)
        if report.passes_quality:
            passed += 1
        else:
            failed += 1

    response = BatchValidationResponse(
        total_items=len(request.items),
        passed=passed,
        failed=failed,
        reports=reports,
        timestamp=get_current_timestamp()
    )

    result = create_success_response(
        message="Batch validation completed",
        data=response.model_dump()  # Pydantic v2: was .dict()
    )

    # Store in idempotency cache
    if idempotency_key:
        store_idempotency_cache(idempotency_key, result)

    return result
"""

# ============================================================================
# BACKEND IMPLEMENTATION (Reference)
# ============================================================================

"""
# Backend side (FastAPI)

from fastapi import FastAPI, HTTPException
from shared_models import AethelgardConcept, QualityReport  # Was PythonConcept

app = FastAPI()

# Backend's own database
validated_content_db = {}

@app.post("/api/v1/content/store")
async def store_content(concept: AethelgardConcept, quality_report: QualityReport):
    '''Store validated content from Research Portal.'''
    if not quality_report.passes_quality:
        raise HTTPException(400, "Content did not pass quality check")

    if quality_report.overall_score < 85:
        raise HTTPException(400, "Content below quality threshold (need 85+)")

    validated_content_db[concept.concept_id] = {
        "concept": concept,
        "quality_report": quality_report
    }

    return {"status": "stored", "concept_id": concept.concept_id}


@app.get("/api/v1/content/{concept_id}")
async def get_content(concept_id: str):
    '''Serve validated content to AXIS AI.'''
    if concept_id not in validated_content_db:
        raise HTTPException(404, "Content not found")

    return validated_content_db[concept_id]["concept"]


@app.get("/api/v1/content/list")
async def list_content(
    difficulty: str = None,
    min_score: int = 85,  # Raised from 70 to 85
    min_citation_density: float = None
):
    '''List validated content for AXIS AI.'''
    results = []
    for item in validated_content_db.values():
        concept = item["concept"]
        report = item["quality_report"]

        # Filter by difficulty
        if difficulty and concept.difficulty != difficulty:
            continue

        # Filter by quality score
        if report.overall_score < min_score:
            continue

        # Filter by citation density (if specified)
        if min_citation_density is not None:
            telemetry = report.telemetry
            if telemetry.citation_density < min_citation_density:
                continue

        results.append(concept)

    return {"total": len(results), "content": results}
"""

# ============================================================================
# ERROR SCENARIOS & HANDLING
# ============================================================================

"""
ERROR 1: Too Many Items in Batch
Request: items=[...] (> 100 items)
Response: 400 Bad Request
{
    "status": "error",
    "error": "Batch too large",
    "details": "Maximum 100 items per batch",
    "code": 400
}

ERROR 2: Empty Batch
Request: items=[]
Response: 400 Bad Request
{
    "status": "error",
    "error": "Invalid batch",
    "details": "Batch must contain at least 1 item",
    "code": 400
}

ERROR 3: Mixed Invalid Items
Request: items=[valid_concept, invalid_concept, valid_question]
Response: 207 Multi-Status (partial success)
{
    "status": "partial_success",
    "message": "Batch validation completed with errors",
    "data": {
        "total_items": 3,
        "validated": 2,
        "errors": 1,
        "reports": [...],
        "errors_detail": [
            {
                "index": 1,
                "item_id": "invalid-concept",
                "error": "Field 'problem' too short"
            }
        ]
    }
}

ERROR 4: Unauthorized
Request: Missing or invalid Authorization header
Response: 401 Unauthorized
{
    "status": "error",
    "error": "Unauthorized",
    "details": "Invalid or missing API key",
    "code": 401
}

ERROR 5: Failed Quality Gates (Not Error - Valid Response)
Request: Valid concepts but fail gates
Response: 200 OK (not error, but passes_quality=false)
{
    "status": "success",
    "data": {
        "reports": [
            {
                "overall_score": 82,
                "gates": [
                    {"name": "citation_density", "passed": false, "details": "0.8 < 1.0"}
                ],
                "passes_quality": false  // overall_score < 85 OR gate failed
            }
        ]
    }
}

ERROR 6: Rate Limit Exceeded
Request: Too many requests from client
Response: 429 Too Many Requests
{
    "status": "error",
    "error": "Rate limit exceeded",
    "details": "Maximum 100 requests per hour exceeded",
    "code": 429
}
Headers:
    Retry-After: 3600  // Seconds until rate limit resets

Note: Client should respect Retry-After header and implement exponential backoff.
"""

# ============================================================================
# OPTIMIZATION NOTES
# ============================================================================

"""
BATCH VALIDATION BENEFITS:
✅ Network efficiency: 1 request instead of N requests
✅ Quality Checker can optimize: Process multiple items in parallel
✅ Reduced overhead: Less connection setup/teardown
✅ Atomic operations: All-or-nothing validation possible
✅ Idempotency: Duplicate requests return cached results

RECOMMENDED BATCH SIZES:
- Small: 1-10 items (immediate feedback)
- Medium: 10-50 items (balanced)
- Large: 50-100 items (bulk import)
- DO NOT exceed 100 items (split into multiple batches)

VALIDATION TYPES:
- "quick": Basic checks only (faster, 80% accuracy)
  • Skip telemetry collection
  • Skip code execution
  • Basic score estimation
- "full": Comprehensive checks (slower, 99% accuracy)
  • Full 10-criterion evaluation
  • Code execution validation
  • Complete telemetry
  • LangSmith tracing

WHEN TO USE QUICK VS FULL:
- Quick: Real-time user input, preview mode, draft concepts
- Full: Production content, final validation, serving to learners

AUTHENTICATION:
- Backend → Quality Checker: Bearer token (BACKEND_API_KEY)
- Stored in environment variable (not committed to git)
- Validated on each request
- Rate limited: 1000 requests/hour per API key

IDEMPOTENCY:
- Optional Idempotency-Key header (UUID)
- Duplicate requests (same key) return cached results
- Cache TTL: 24 hours
- Use for retry logic to prevent duplicate processing
"""

# ============================================================================
# SUCCESS CRITERIA
# ============================================================================

"""
Integration is successful if:
✅ Backend can batch validate content efficiently
✅ Backend stores only validated content (passes_quality=True AND overall_score ≥85)
✅ Backend serves validated content to AXIS AI
✅ Re-validation workflow works for quality audits
✅ Filters work correctly (difficulty, tags, min_score, min_citation_density)
✅ Performance: Batch of 50 items validates in < 30 seconds
✅ Error handling graceful (partial success supported via 207 Multi-Status)
✅ Authentication required (Bearer token)
✅ Idempotency supported (same request = same response)
✅ Gates enforced: coverage_score ≥0.65, citation_density ≥1.0, exec_ok=true, scope_ok=true
✅ Telemetry included: run_id, model, latency_ms, tokens, etc.
"""

# ============================================================================
# VERSION HISTORY
# ============================================================================

"""
v1.0 (2025-11-06):
- Initial API contract
- Batch validation endpoint
- Single item validation (reuse from other contracts)
- Content serving endpoints (GET)
- Filter support
- Re-validation workflow

v2.0 (2025-11-06):
- Renamed: PythonConcept → AethelgardConcept
- Upgraded: QualityReport to 10-criterion rubric (was 7)
- Added: Quality gates (coverage_score, citation_density, exec_ok, scope_ok)
- Added: Telemetry object (9+ metrics)
- Added: Authentication (Bearer token)
- Added: Idempotency-Key header
- Changed: Pass threshold to 85 (was 70)
- Changed: code_examples from List[str] to List[CodeExample]
- Changed: provisional_citations added (List[Citation])
- Added: mode field (Coach/Hybrid/Socratic)
- Added: libraries field (explicit scope enforcement)
- Added: min_citation_density filter parameter
- Migrated: Pydantic v1 → v2 (.dict() → .model_dump())
- Updated: All examples to use CodeExample model
- Updated: CURL examples with auth and idempotency headers
- Updated: Default min_score filter from 70 to 85
"""
