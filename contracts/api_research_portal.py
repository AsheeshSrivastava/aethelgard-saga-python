"""
API Contract: Research Portal ↔ Quality Checker
================================================

**System A:** Research Portal (ChatGPT builds)
**System B:** Quality Checker (Claude builds)

**Purpose:** Research Portal generates Python concepts, sends to Quality Checker for validation.

**Version:** 2.0
**Created:** 2025-11-06
**Updated:** 2025-11-06 (Production-grade upgrade)
"""

from shared_models import (
    AethelgardConcept,
    CodeExample,
    Citation,
    CitationSource,
    Mode,
    Library,
    QualityReport,
    create_success_response,
    create_error_response
)
from typing import Dict, Any
import requests
import asyncio
import uuid
import os

# ============================================================================
# ENDPOINT SPECIFICATION
# ============================================================================

ENDPOINT = "POST /api/v1/content/validate"
BASE_URL = "http://localhost:8000"  # Quality Checker URL

# Authentication (set in environment)
RESEARCH_PORTAL_API_KEY = os.getenv("RESEARCH_PORTAL_API_KEY", "dev-key-research-portal")

# ============================================================================
# REQUEST FORMAT
# ============================================================================

def validate_content(concept: AethelgardConcept, idempotency_key: str = None) -> Dict[str, Any]:
    """
    Send Aethelgard concept to Quality Checker for validation.

    Args:
        concept: AethelgardConcept to validate
        idempotency_key: Optional UUID for idempotent requests (generated if not provided)

    Returns:
        Dict with validation results

    Example:
        >>> concept = AethelgardConcept(
        ...     concept_id="python-variables-01",
        ...     title="Variables",
        ...     problem="How do you store data in Python?",
        ...     system="Use variables like x = 5",
        ...     win="Now you can store and reuse data",
        ...     code_examples=[
        ...         CodeExample(code="x = 5\\nprint(x)  # Output: 5", expected_output="5", runnable=True),
        ...         CodeExample(code="name = 'Alice'\\nprint(name)  # Output: Alice", expected_output="Alice", runnable=True)
        ...     ],
        ...     provisional_citations=[
        ...         Citation(source=CitationSource.VECTOR, title="Python Tutorial §2.1", locator="§2.1.1")
        ...     ],
        ...     difficulty="beginner",
        ...     prerequisites=[],
        ...     tags=["basics"],
        ...     mode=Mode.COACH,
        ...     libraries=[Library.CORE_PYTHON]
        ... )
        >>> result = validate_content(concept)
        >>> print(result['data']['overall_score'])
        87
    """
    # Generate idempotency key if not provided
    if idempotency_key is None:
        idempotency_key = str(uuid.uuid4())

    response = requests.post(
        f"{BASE_URL}/api/v1/content/validate",
        json=concept.model_dump(),  # Pydantic v2: .model_dump() instead of .dict()
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {RESEARCH_PORTAL_API_KEY}",
            "Idempotency-Key": idempotency_key
        }
    )
    return response.json()


# ============================================================================
# RESPONSE FORMAT
# ============================================================================

# SUCCESS RESPONSE (Status 200)
"""
{
    "status": "success",
    "message": "Content validated successfully",
    "data": {
        "item_id": "python-variables-01",
        "item_type": "content",
        "overall_score": 87,

        // 10-Criterion Rubric (100 points total)
        "groundedness_citation_score": 18,     // 20 pts max
        "technical_correctness_score": 14,     // 15 pts max
        "people_first_pedagogy_score": 13,     // 15 pts max
        "psw_actionability_score": 9,          // 10 pts max
        "mode_fidelity_score": 9,              // 10 pts max
        "self_paced_scaffolding_score": 8,     // 10 pts max
        "retrieval_quality_score": 9,          // 10 pts max
        "clarity_score": 4,                    // 5 pts max
        "bloom_alignment_score": 2,            // 3 pts max
        "people_first_language_score": 1,      // 2 pts max

        // Quality Gates
        "gates": [
            {"name": "coverage_score", "passed": true, "details": "0.72 >= 0.65"},
            {"name": "citation_density", "passed": true, "details": "1.2 >= 1.0"},
            {"name": "exec_ok", "passed": true, "details": "All code examples executed successfully"},
            {"name": "scope_ok", "passed": true, "details": "Only approved libraries used"}
        ],

        // Telemetry
        "telemetry": {
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
            "exec_ok": true,
            "latency_ms": 1234,
            "tokens": 567
        },

        "issues": [
            {
                "severity": "low",
                "category": "people_first_pedagogy",
                "message": "Could include more self-paced scaffolding prompts",
                "suggestion": "Add checkpoint questions like 'Try creating your own variable before continuing'"
            }
        ],
        "strengths": [
            "Strong groundedness with citations",
            "Clear PSW structure",
            "All code examples executable",
            "Beginner-friendly language"
        ],
        "suggestions": [
            "Add more scaffolding prompts for self-paced learning"
        ],
        "passes_quality": true,
        "validated_at": "2025-11-08T10:30:00Z",
        "validator_version": "2.0"
    },
    "timestamp": "2025-11-08T10:30:00Z"
}
"""

# ERROR RESPONSE (Status 400)
"""
{
    "status": "error",
    "error": "Invalid concept format",
    "details": "Field 'problem' is too short (minimum 50 characters)",
    "code": 400,
    "timestamp": "2025-11-08T10:30:00Z"
}
"""

# ============================================================================
# EXAMPLE USAGE (Research Portal Side)
# ============================================================================

async def research_portal_workflow():
    """
    Example workflow in Research Portal:
    1. Generate concept
    2. Validate with Quality Checker
    3. Store if passes
    """
    # Step 1: Generate concept (using LangChain/LLM)
    concept = AethelgardConcept(
        concept_id="python-variables-01",
        title="Python Variables and Assignment",
        problem="You need to store data like a user's age or name so you can use it later in your program. How do you do this?",
        system="Variables in Python work like labeled boxes. You create a variable by giving it a name and assigning a value using the equals sign (=). Python remembers this value and lets you use it anywhere in your code by referencing the variable name.",
        win="Now you can store any data (numbers, text, lists) and reuse it throughout your program without typing it again. This makes your code cleaner and easier to change.",
        code_examples=[
            CodeExample(
                code="# Storing a number\nage = 25\nprint(age)  # Output: 25",
                expected_output="25",
                runnable=True
            ),
            CodeExample(
                code="# Storing text\nname = 'Alice'\nprint(name)  # Output: Alice",
                expected_output="Alice",
                runnable=True
            )
        ],
        provisional_citations=[
            Citation(
                source=CitationSource.VECTOR,
                title="Python Tutorial §2.1: Variables",
                locator="§2.1.1",
                url="https://docs.python.org/3/tutorial/introduction.html#using-python-as-a-calculator",
                license="PSF"
            )
        ],
        difficulty="beginner",
        prerequisites=[],
        tags=["variables", "basics", "data-storage"],
        mode=Mode.COACH,  # Coach mode: mostly explanations (15-30% questions)
        libraries=[Library.CORE_PYTHON]
    )

    # Step 2: Validate with Quality Checker
    try:
        result = validate_content(concept)

        if result['status'] == 'success':
            quality_report = result['data']

            if quality_report['passes_quality']:
                print(f"✅ Concept passed validation (Score: {quality_report['overall_score']}/100)")

                # Check gate status
                gates = quality_report.get('gates', [])
                gates_status = {gate['name']: gate['passed'] for gate in gates}
                print(f"Gates: {gates_status}")

                # Step 3: Store in database
                # await store_concept(concept, quality_report)
            else:
                print(f"⚠️ Concept needs improvement (Score: {quality_report['overall_score']}/100)")
                print(f"Issues: {quality_report['issues']}")
                print(f"Suggestions: {quality_report['suggestions']}")

                # Check which gates failed
                gates = quality_report.get('gates', [])
                failed_gates = [gate for gate in gates if not gate['passed']]
                if failed_gates:
                    print(f"Failed gates: {[gate['name'] for gate in failed_gates]}")

                # Regenerate or edit based on feedback
        else:
            print(f"❌ Validation error: {result['error']}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")


# ============================================================================
# CURL EXAMPLE (For Testing)
# ============================================================================

"""
curl -X POST http://localhost:8000/api/v1/content/validate \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer dev-key-research-portal" \\
  -H "Idempotency-Key: $(uuidgen)" \\
  -d '{
    "concept_id": "python-variables-01",
    "title": "Variables",
    "problem": "How do you store data like a user age or name so you can use it later in your program?",
    "system": "Variables in Python work like labeled boxes. You create a variable by giving it a name and assigning a value using the equals sign (=).",
    "win": "Now you can store any data (numbers, text, lists) and reuse it throughout your program.",
    "code_examples": [
      {
        "code": "age = 25\\nprint(age)",
        "expected_output": "25",
        "runnable": true
      },
      {
        "code": "name = '\'Alice\\'\\nprint(name)",
        "expected_output": "Alice",
        "runnable": true
      }
    ],
    "provisional_citations": [
      {
        "source": "vector",
        "title": "Python Tutorial §2.1",
        "locator": "§2.1.1",
        "url": "https://docs.python.org/3/tutorial/introduction.html"
      }
    ],
    "difficulty": "beginner",
    "prerequisites": [],
    "tags": ["basics"],
    "mode": "coach",
    "libraries": ["core-python"]
  }'
"""

# ============================================================================
# QUALITY CHECKER IMPLEMENTATION (Reference)
# ============================================================================

"""
# Quality Checker side (FastAPI)

from fastapi import FastAPI, HTTPException, Header
from shared_models import AethelgardConcept, QualityReport, create_success_response, create_error_response

app = FastAPI()

@app.post("/api/v1/content/validate")
async def validate_content(
    concept: AethelgardConcept,
    authorization: str = Header(...),
    idempotency_key: str = Header(None)
):
    # Verify API key
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    api_key = authorization.split("Bearer ")[1]
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Check idempotency (if key provided, check if already processed)
    if idempotency_key:
        cached_result = check_idempotency_cache(idempotency_key)
        if cached_result:
            return cached_result

    try:
        # Validate concept using Quality Checker logic
        report = await quality_checker.validate_content(concept)

        response = create_success_response(
            message="Content validated successfully",
            data=report.model_dump()  # Pydantic v2: .model_dump() instead of .dict()
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
"""

# ============================================================================
# ERROR SCENARIOS & HANDLING
# ============================================================================

"""
ERROR 1: Field Validation Error
Request: concept.problem = "Too short"  (< 50 chars)
Response: 400 Bad Request
{
    "status": "error",
    "error": "Invalid concept format",
    "details": "Field 'problem' is too short (minimum 50 characters)",
    "code": 400
}

ERROR 2: Missing Required Field
Request: concept without 'title' field
Response: 422 Unprocessable Entity (Pydantic validation)
{
    "status": "error",
    "error": "Validation error",
    "details": "field required: title",
    "code": 422
}

ERROR 3: Quality Checker Offline
Request: Valid concept
Response: Connection error (handle in try/except)

ERROR 4: Empty Code Examples
Request: concept.code_examples = [CodeExample(code="", runnable=False)]
Response: 400 Bad Request
{
    "status": "error",
    "error": "Invalid concept format",
    "details": "Code examples must have at least 10 characters",
    "code": 400
}

ERROR 5: Unauthorized
Request: Missing or invalid Authorization header
Response: 401 Unauthorized
{
    "status": "error",
    "error": "Unauthorized",
    "details": "Invalid or missing API key",
    "code": 401
}

ERROR 6: Failed Quality Gates
Request: Valid concept but fails gates
Response: 200 OK (not error, but passes_quality=false)
{
    "status": "success",
    "data": {
        "overall_score": 72,
        "gates": [
            {"name": "citation_density", "passed": false, "details": "0.8 < 1.0"}
        ],
        "passes_quality": false  // overall_score < 85 OR gate failed
    }
}
"""

# ============================================================================
# SUCCESS CRITERIA
# ============================================================================

"""
Integration is successful if:
✅ Research Portal can send AethelgardConcept to Quality Checker
✅ Quality Checker returns QualityReport with all 10 scores
✅ Pass criteria: overall_score >= 85 AND all core gates passed
✅ Gates checked: coverage_score ≥0.65, citation_density ≥1.0, exec_ok=true, scope_ok=true
✅ Telemetry included: run_id, model, latency_ms, tokens, etc.
✅ Issues and suggestions help improve content
✅ No data format errors (Pydantic validation passes)
✅ Response time < 5 seconds per concept
✅ Error handling works for all edge cases
✅ Authentication required (Bearer token)
✅ Idempotency supported (same request = same response)
"""

# ============================================================================
# VERSION HISTORY
# ============================================================================

"""
v1.0 (2025-11-06):
- Initial API contract
- POST /api/v1/content/validate endpoint
- PythonConcept request format
- QualityReport response format (7 criteria)
- Error handling specification

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
- Migrated: Pydantic v1 → v2 (.dict() → .model_dump())
"""
