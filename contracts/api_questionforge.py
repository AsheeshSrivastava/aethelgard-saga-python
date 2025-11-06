"""
API Contract: QuestionForge ↔ Quality Checker
==============================================

**System A:** QuestionForge (existing system)
**System B:** Quality Checker (Claude builds)

**Purpose:** QuestionForge generates practice questions, sends to Quality Checker for validation.

**Version:** 2.0
**Created:** 2025-11-06
**Updated:** 2025-11-06 (Production-grade upgrade)
"""

from shared_models import (
    Question,
    QuestionType,
    BloomsLevel,
    DifficultyLevel,
    QualityReport,
    create_success_response,
    create_error_response
)
from typing import Dict, Any
import requests
import uuid
import os

# ============================================================================
# ENDPOINT SPECIFICATION
# ============================================================================

ENDPOINT = "POST /api/v1/questions/validate"
BASE_URL = "http://localhost:8000"  # Quality Checker URL

# Authentication (set in environment)
QUESTIONFORGE_API_KEY = os.getenv("QUESTIONFORGE_API_KEY", "dev-key-questionforge")

# ============================================================================
# REQUEST FORMAT
# ============================================================================

def validate_question(question: Question, idempotency_key: str = None) -> Dict[str, Any]:
    """
    Send question to Quality Checker for validation.

    Args:
        question: Question to validate
        idempotency_key: Optional UUID for idempotent requests (generated if not provided)

    Returns:
        Dict with validation results

    Example:
        >>> question = Question(
        ...     question_id="q-variables-mc-01",
        ...     concept_id="python-variables-01",
        ...     question_text="What happens when you assign a value to a variable?",
        ...     question_type="multiple_choice",
        ...     options=[
        ...         "Python creates a labeled container",
        ...         "Python deletes the old value",
        ...         "Python converts to text",
        ...         "Python throws an error"
        ...     ],
        ...     correct_answer="Python creates a labeled container",
        ...     difficulty="beginner",
        ...     blooms_level="understand"
        ... )
        >>> result = validate_question(question)
        >>> print(result['data']['overall_score'])
        82
    """
    # Generate idempotency key if not provided
    if idempotency_key is None:
        idempotency_key = str(uuid.uuid4())

    response = requests.post(
        f"{BASE_URL}/api/v1/questions/validate",
        json=question.model_dump(),  # Pydantic v2: .model_dump() instead of .dict()
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {QUESTIONFORGE_API_KEY}",
            "Idempotency-Key": idempotency_key
        },
        timeout=10  # Prevent hanging connections
    )
    return response.json()


# ============================================================================
# RESPONSE FORMAT
# ============================================================================

# SUCCESS RESPONSE (Status 200)
"""
{
    "status": "success",
    "message": "Question validated successfully",
    "data": {
        "item_id": "q-variables-mc-01",
        "item_type": "question",
        "overall_score": 87,

        // 10-Criterion Rubric (100 points total)
        // NOTE: Questions use adapted criteria (not all criteria apply equally)
        "groundedness_citation_score": 15,     // 20 pts max - Less critical for questions
        "technical_correctness_score": 15,     // 15 pts max - Very important
        "people_first_pedagogy_score": 14,     // 15 pts max - Important for questions
        "psw_actionability_score": 8,          // 10 pts max - Less critical
        "mode_fidelity_score": 7,              // 10 pts max - Less critical
        "self_paced_scaffolding_score": 9,     // 10 pts max - Hints/explanation
        "retrieval_quality_score": 9,          // 10 pts max - Important
        "clarity_score": 5,                    // 5 pts max - Very important
        "bloom_alignment_score": 3,            // 3 pts max - Very important
        "people_first_language_score": 2,      // 2 pts max - Important

        // Quality Gates (adapted for questions)
        // NOTE: For questions, citation gate passes if (a) no explanation field OR (b) explanation has ≥1 allowlisted citation. citation_density is telemetry only.
        "gates": [
            {"name": "coverage_score", "passed": true, "details": "Question covers concept adequately"},
            {"name": "citation_density", "passed": true, "details": "Explanation cites concept (if applicable)"},
            {"name": "exec_ok", "passed": true, "details": "Code in question/answer executes (if applicable)"},
            {"name": "scope_ok", "passed": true, "details": "Question within curriculum scope"}
        ],

        // Telemetry
        "telemetry": {
            "run_id": "run_xyz789",
            "trace_url": "https://langsmith.com/trace/xyz789",
            "model": "gpt-4o-2024-11-20",
            "provider": "openai",
            "prompt_version": "v2.0",
            "graph_version": "v1.0",
            "coverage_score": 0.80,
            "citation_density": 0.5,  // Lower for questions (explanation may cite concept)
            "unique_sources": 1,
            "mode_ratio": 0.0,  // Not applicable to questions
            "scaffold_depth": 1,  // Hints count as scaffolding
            "exec_ok": true,
            "latency_ms": 890,
            "tokens": 345
        },

        "issues": [
            {
                "severity": "low",
                "category": "clarity",
                "message": "Consider rewording option 2 for clarity",
                "suggestion": "Change 'Python deletes the old value' to 'Python replaces the previous value'"
            }
        ],
        "strengths": [
            "Clear question text",
            "Appropriate Bloom's level (understand)",
            "Good distractors"
        ],
        "suggestions": [
            "Add explanation field for learning reinforcement"
        ],
        "passes_quality": true,
        "validated_at": "2025-11-08T11:00:00Z",
        "validator_version": "2.0"
    },
    "timestamp": "2025-11-08T11:00:00Z"
}
"""

# ERROR RESPONSE (Status 400)
"""
{
    "status": "error",
    "error": "Invalid question format",
    "details": "multiple_choice requires at least 2 options",
    "code": 400,
    "timestamp": "2025-11-08T11:00:00Z"
}
"""

# ============================================================================
# QUALITY CRITERIA FOR QUESTIONS (10-Criterion Adaptation)
# ============================================================================

"""
PRODUCTION-GRADE RUBRIC (100 points, pass threshold 85+)

Questions use the same 10-criterion framework as concepts, but with adapted interpretations:

1. GROUNDEDNESS & CITATION QUALITY (0-20 points)
   - Less critical for questions (weight reduced)
   - Applies if explanation cites concept
   - Correct answer must be grounded in curriculum

2. TECHNICAL CORRECTNESS (0-15 points)
   - Factually accurate
   - Correct Python syntax (if code)
   - No outdated information
   - Correct answer is truly correct

3. PEOPLE-FIRST PEDAGOGY (0-15 points)
   - Problem-oriented (real-world scenarios)
   - Experiential (learn by doing for code questions)
   - Immediately applicable
   - Self-directed

4. PSW ACTIONABILITY (0-10 points)
   - Less critical for questions (weight reduced)
   - Explanation may reference PSW framework

5. MODE FIDELITY (0-10 points)
   - Less critical for questions (weight reduced)
   - Question can be used in any mode

6. SELF-PACED SCAFFOLDING (0-10 points)
   - Hints provided (progressive scaffolding)
   - Explanation helps learner understand
   - Appropriate difficulty progression

7. RETRIEVAL QUALITY (0-10 points)
   - Keyword-rich for search
   - Context-independent (question makes sense alone)
   - LLM-parseable format
   - Semantic clarity

8. CLARITY (0-5 points)
   - Question text is beginner-friendly
   - No ambiguous wording
   - Proper grammar and spelling
   - Clear what is being asked

9. BLOOM ALIGNMENT (0-3 points)
   - Tests correct cognitive level
   - Remember: Recall facts
   - Understand: Explain concepts
   - Apply: Use in new situations
   - Analyze: Break down into parts
   - Evaluate: Make judgments
   - Create: Build something new

10. PEOPLE-FIRST LANGUAGE (0-2 points)
    - Inclusive language
    - Respectful tone
    - No ableist terms
    - Gender-neutral

TOTAL: 100 points
PASSING THRESHOLD: 85+ (raised from 70)
"""

# ============================================================================
# EXAMPLE USAGE (QuestionForge Side)
# ============================================================================

async def questionforge_workflow():
    """
    Example workflow in QuestionForge:
    1. Generate question
    2. Validate with Quality Checker
    3. Store if passes
    """
    # Step 1: Generate question (existing QuestionForge logic)
    question = Question(
        question_id="q-variables-mc-01",
        concept_id="python-variables-01",
        question_text="What happens when you assign a value to a variable in Python?",
        question_type=QuestionType.MULTIPLE_CHOICE,
        options=[
            "Python creates a labeled container to store the value",
            "Python deletes the old value",
            "Python converts the value to text",
            "Python throws an error"
        ],
        correct_answer="Python creates a labeled container to store the value",
        difficulty=DifficultyLevel.BEGINNER,
        blooms_level=BloomsLevel.UNDERSTAND,
        explanation="Variables in Python work like labeled containers that store values for later use.",
        hints=["Think about what a variable represents"]
    )

    # Step 2: Validate with Quality Checker
    try:
        result = validate_question(question)

        if result['status'] == 'success':
            quality_report = result['data']

            if quality_report['passes_quality']:
                print(f"✅ Question passed validation (Score: {quality_report['overall_score']}/100)")

                # Check gate status
                gates = quality_report.get('gates', [])
                gates_status = {gate['name']: gate['passed'] for gate in gates}
                print(f"Gates: {gates_status}")

                # Step 3: Store in question bank
                # await store_question(question, quality_report)
            else:
                print(f"⚠️ Question needs improvement (Score: {quality_report['overall_score']}/100)")
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
curl -X POST http://localhost:8000/api/v1/questions/validate \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer dev-key-questionforge" \\
  -H "Idempotency-Key: $(uuidgen)" \\
  -d '{
    "question_id": "q-variables-mc-01",
    "concept_id": "python-variables-01",
    "question_text": "What happens when you assign a value to a variable in Python?",
    "question_type": "multiple_choice",
    "options": [
      "Python creates a labeled container to store the value",
      "Python deletes the old value",
      "Python converts the value to text",
      "Python throws an error"
    ],
    "correct_answer": "Python creates a labeled container to store the value",
    "difficulty": "beginner",
    "blooms_level": "understand",
    "explanation": "Variables work like labeled containers.",
    "hints": ["Think about what a variable represents"]
  }'
"""

# ============================================================================
# QUALITY CHECKER IMPLEMENTATION (Reference)
# ============================================================================

"""
# Quality Checker side (FastAPI)

from fastapi import FastAPI, HTTPException, Header
from shared_models import Question, QualityReport, create_success_response, create_error_response

app = FastAPI()

@app.post("/api/v1/questions/validate")
async def validate_question(
    question: Question,
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

    try:
        # Validate question using Quality Checker logic
        report = await quality_checker.validate_question(question)

        response = create_success_response(
            message="Question validated successfully",
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
                error="Invalid question format",
                details=str(e),
                code=400
            ).model_dump()  # Pydantic v2
        )
"""

# ============================================================================
# ERROR SCENARIOS & HANDLING
# ============================================================================

"""
ERROR 1: Missing Options for Multiple Choice
Request: question_type="multiple_choice", options=None
Response: 400 Bad Request
{
    "status": "error",
    "error": "Invalid question format",
    "details": "multiple_choice requires at least 2 options",
    "code": 400
}

ERROR 2: Question Text Too Short
Request: question_text="What?"  (< 10 chars)
Response: 422 Unprocessable Entity
{
    "status": "error",
    "error": "Validation error",
    "details": "Field 'question_text' must be at least 10 characters",
    "code": 422
}

ERROR 3: Invalid Bloom's Level
Request: blooms_level="memorize"  (not in enum)
Response: 422 Unprocessable Entity
{
    "status": "error",
    "error": "Validation error",
    "details": "blooms_level must be one of: remember, understand, apply, analyze, evaluate, create",
    "code": 422
}

ERROR 4: Correct Answer Not in Options
Request: correct_answer="X", options=["A", "B", "C", "D"]
Response: 400 Bad Request
{
    "status": "error",
    "error": "Invalid question format",
    "details": "Correct answer must be one of the provided options",
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
Request: Valid question but fails gates
Response: 200 OK (not error, but passes_quality=false)
{
    "status": "success",
    "data": {
        "overall_score": 72,
        "gates": [
            {"name": "technical_correctness", "passed": false, "details": "Incorrect answer provided"}
        ],
        "passes_quality": false  // overall_score < 85 OR gate failed
    }
}

ERROR 7: Rate Limit Exceeded
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
# QUESTION TYPES SUPPORTED
# ============================================================================

"""
1. MULTIPLE_CHOICE
   - Requires: options (List[str]), correct_answer (str)
   - Example: "What is a variable?" with 4 options

2. TRUE_FALSE
   - Requires: options (["True", "False"]), correct_answer ("True" or "False")
   - Example: "Variables can store any data type. True or False?"

3. FILL_BLANK
   - Requires: correct_answer (str)
   - Example: "A _____ is used to store data in Python."

4. CODE_OUTPUT
   - Requires: correct_answer (str representing expected output)
   - Example: "What does print(5 + 3) output?"

5. CODE_WRITING
   - Requires: correct_answer (str representing code solution)
   - Example: "Write code to assign value 10 to variable x"
"""

# ============================================================================
# SUCCESS CRITERIA
# ============================================================================

"""
Integration is successful if:
✅ QuestionForge can send Question to Quality Checker
✅ Quality Checker returns QualityReport with all 10 scores
✅ Pass criteria: overall_score >= 85 AND all core gates passed (raised from 70)
✅ Gates checked: coverage, citation, exec_ok (for code questions), scope_ok
✅ Telemetry included: run_id, model, latency_ms, tokens, etc.
✅ Bloom's taxonomy validation works correctly
✅ Difficulty assessment accurate
✅ Technical correctness checked
✅ People-first language enforced
✅ No data format errors (Pydantic validation passes)
✅ Response time < 3 seconds per question
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
- POST /api/v1/questions/validate endpoint
- Question request format
- QualityReport response format (7 criteria)
- 5 question types supported

v2.0 (2025-11-06):
- Upgraded: QualityReport to 10-criterion rubric (was 7)
- Added: Quality gates (coverage, citation, exec_ok, scope_ok)
- Added: Telemetry object (9+ metrics)
- Added: Authentication (Bearer token)
- Added: Idempotency-Key header
- Changed: Pass threshold to 85 (was 70)
- Updated: 10-criterion interpretation for questions
- Migrated: Pydantic v1 → v2 (.dict() → .model_dump())
- Note: Question model itself unchanged (no new fields like AethelgardConcept)
"""
