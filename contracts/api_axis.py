"""
API Contract: AXIS AI ↔ Aethelgard Backend
===========================================

**System A:** AXIS AI Chatbot (ChatGPT builds)
**System B:** Aethelgard Backend (ChatGPT builds)

**Purpose:** AXIS AI retrieves validated content from Backend to answer learner questions.

**Note:** Both systems built by ChatGPT, but still need clear API contract for separation of concerns.

**Version:** 2.0
**Created:** 2025-11-06
**Updated:** 2025-11-06 (Production-grade upgrade)
"""

from shared_models import (
    AethelgardConcept,  # Renamed from PythonConcept
    Question,
    DifficultyLevel
)
from typing import Dict, Any, List, Optional
import requests
import os

# ============================================================================
# ENDPOINT SPECIFICATIONS
# ============================================================================

BASE_URL = "http://localhost:9000"  # Aethelgard Backend URL

# Authentication (set in environment)
AXIS_API_KEY = os.getenv("AXIS_API_KEY", "dev-key-axis")

# Content retrieval
GET_CONCEPT_ENDPOINT = "GET /api/v1/content/{concept_id}"
LIST_CONCEPTS_ENDPOINT = "GET /api/v1/content/list"
SEARCH_CONCEPTS_ENDPOINT = "GET /api/v1/content/search"

# Question retrieval
GET_QUESTIONS_ENDPOINT = "GET /api/v1/questions/{concept_id}"
GET_RANDOM_QUESTION_ENDPOINT = "GET /api/v1/questions/random"

# Learning path
GET_PREREQUISITES_ENDPOINT = "GET /api/v1/content/{concept_id}/prerequisites"
GET_NEXT_CONCEPTS_ENDPOINT = "GET /api/v1/content/{concept_id}/next"

# Progress tracking (optional)
UPDATE_PROGRESS_ENDPOINT = "POST /api/v1/progress/update"

# ============================================================================
# CONTENT RETRIEVAL
# ============================================================================

def get_concept(concept_id: str) -> Dict[str, Any]:
    """
    Retrieve single concept by ID.

    Args:
        concept_id: Unique concept identifier

    Returns:
        Dict with concept data

    Example:
        >>> concept = get_concept("python-variables-01")
        >>> print(concept['title'])
        Variables
    """
    response = requests.get(
        f"{BASE_URL}/api/v1/content/{concept_id}",
        headers={"Authorization": f"Bearer {AXIS_API_KEY}"},
        timeout=10  # Prevent hanging connections
    )
    return response.json()


def list_concepts(
    difficulty: Optional[DifficultyLevel] = None,
    tags: Optional[List[str]] = None,
    min_quality_score: int = 85,  # Raised from 70 to 85
    min_citation_density: Optional[float] = None,  # NEW
    limit: int = 10,
    offset: int = 0
) -> Dict[str, Any]:
    """
    List concepts with filters.

    Args:
        difficulty: Filter by difficulty (beginner/intermediate/advanced)
        tags: Filter by tags
        min_quality_score: Minimum quality score (default 85, raised from 70)
        min_citation_density: Minimum citation density (e.g., 1.0)
        limit: Number of results (max 100)
        offset: Pagination offset

    Returns:
        Dict with list of concepts and total count

    Example:
        >>> result = list_concepts(difficulty="beginner", limit=5)
        >>> print(f"Found {result['total']} beginner concepts")
        Found 15 beginner concepts
    """
    params = {
        "min_quality_score": min_quality_score,
        "limit": limit,
        "offset": offset
    }
    if difficulty:
        params["difficulty"] = difficulty
    if tags:
        params["tags"] = ",".join(tags)
    if min_citation_density is not None:
        params["min_citation_density"] = min_citation_density

    response = requests.get(
        f"{BASE_URL}/api/v1/content/list",
        params=params,
        headers={"Authorization": f"Bearer {AXIS_API_KEY}"},
        timeout=10  # Prevent hanging connections
    )
    return response.json()


def search_concepts(query: str, limit: int = 5) -> Dict[str, Any]:
    """
    Semantic search for concepts (RAG-powered).

    Args:
        query: Natural language search query
        limit: Number of results

    Returns:
        Dict with relevant concepts ranked by similarity

    Example:
        >>> result = search_concepts("how to store data in python", limit=3)
        >>> for concept in result['concepts']:
        ...     print(f"{concept['title']}: {concept['relevance_score']}")
        Variables: 0.92
        Data Types: 0.85
        Lists: 0.78
    """
    response = requests.get(
        f"{BASE_URL}/api/v1/content/search",
        params={"q": query, "limit": limit},
        headers={"Authorization": f"Bearer {AXIS_API_KEY}"},
        timeout=10  # Prevent hanging connections
    )
    return response.json()


# ============================================================================
# QUESTION RETRIEVAL
# ============================================================================

def get_questions_for_concept(concept_id: str) -> Dict[str, Any]:
    """
    Get all practice questions for a concept.

    Args:
        concept_id: Concept to get questions for

    Returns:
        Dict with list of questions

    Example:
        >>> result = get_questions_for_concept("python-variables-01")
        >>> print(f"Found {len(result['questions'])} practice questions")
        Found 5 practice questions
    """
    response = requests.get(
        f"{BASE_URL}/api/v1/questions/{concept_id}",
        headers={"Authorization": f"Bearer {AXIS_API_KEY}"},
        timeout=10  # Prevent hanging connections
    )
    return response.json()


def get_random_question(
    difficulty: Optional[DifficultyLevel] = None,
    blooms_level: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get random practice question.

    Args:
        difficulty: Filter by difficulty
        blooms_level: Filter by Bloom's level

    Returns:
        Dict with single random question

    Example:
        >>> question = get_random_question(difficulty="beginner")
        >>> print(question['question_text'])
        What happens when you assign a value to a variable?
    """
    params = {}
    if difficulty:
        params["difficulty"] = difficulty
    if blooms_level:
        params["blooms_level"] = blooms_level

    response = requests.get(
        f"{BASE_URL}/api/v1/questions/random",
        params=params,
        headers={"Authorization": f"Bearer {AXIS_API_KEY}"},
        timeout=10  # Prevent hanging connections
    )
    return response.json()


# ============================================================================
# LEARNING PATH NAVIGATION
# ============================================================================

def get_prerequisites(concept_id: str) -> Dict[str, Any]:
    """
    Get concepts that should be learned before this one.

    Args:
        concept_id: Concept to get prerequisites for

    Returns:
        Dict with list of prerequisite concepts

    Example:
        >>> prereqs = get_prerequisites("python-lists-01")
        >>> for prereq in prereqs['concepts']:
        ...     print(f"Learn first: {prereq['title']}")
        Learn first: Variables
        Learn first: Data Types
    """
    response = requests.get(
        f"{BASE_URL}/api/v1/content/{concept_id}/prerequisites",
        headers={"Authorization": f"Bearer {AXIS_API_KEY}"},
        timeout=10  # Prevent hanging connections
    )
    return response.json()


def get_next_concepts(concept_id: str) -> Dict[str, Any]:
    """
    Get concepts that build on this one (what to learn next).

    Args:
        concept_id: Current concept

    Returns:
        Dict with list of next concepts

    Example:
        >>> next_concepts = get_next_concepts("python-variables-01")
        >>> for concept in next_concepts['concepts']:
        ...     print(f"Learn next: {concept['title']}")
        Learn next: Data Types
        Learn next: Operators
    """
    response = requests.get(
        f"{BASE_URL}/api/v1/content/{concept_id}/next",
        headers={"Authorization": f"Bearer {AXIS_API_KEY}"},
        timeout=10  # Prevent hanging connections
    )
    return response.json()


# ============================================================================
# EXAMPLE USAGE (AXIS AI Side)
# ============================================================================

async def axis_answer_question(user_query: str) -> str:
    """
    AXIS AI workflow to answer learner question.

    1. Search for relevant concepts
    2. Retrieve concept details
    3. Generate response using LLM + retrieved context
    """
    # Step 1: Search for relevant concepts
    search_result = search_concepts(user_query, limit=3)

    if not search_result['concepts']:
        return "I don't have information on that topic yet. Try asking about Python basics like variables, data types, or operators."

    # Step 2: Get most relevant concept
    top_concept = search_result['concepts'][0]
    concept = get_concept(top_concept['concept_id'])

    # Step 3: Generate response using LLM with context
    # (AXIS AI uses LangGraph for this)

    # Extract code from code_examples (now List[CodeExample])
    code_snippets = []
    for example in concept.get('code_examples', []):
        if isinstance(example, dict):
            code_snippets.append(example.get('code', ''))
        else:
            code_snippets.append(str(example))

    context = f"""
    Concept: {concept['title']}

    Problem: {concept['problem']}
    System: {concept['system']}
    Win: {concept['win']}

    Code Examples:
    {chr(10).join(code_snippets)}
    """

    # LLM generates answer using this context
    # answer = await llm.generate(user_query, context)

    return f"Based on the concept '{concept['title']}', here's what you need to know..."


async def axis_practice_mode(concept_id: str):
    """
    AXIS AI practice mode workflow.

    1. Get questions for concept
    2. Present random question
    3. Check answer
    4. Provide feedback
    """
    # Step 1: Get questions
    questions_result = get_questions_for_concept(concept_id)

    if not questions_result['questions']:
        return "No practice questions available for this concept yet."

    # Step 2: Present random question
    import random
    question = random.choice(questions_result['questions'])

    # AXIS AI presents question to learner
    # learner_answer = await get_user_input()

    # Step 3: Check answer
    # correct = (learner_answer == question['correct_answer'])

    # Step 4: Provide feedback
    # if correct:
    #     return f"✅ Correct! {question.get('explanation', '')}"
    # else:
    #     return f"❌ Not quite. {question.get('hints', ['Try again!'])[0]}"

    pass


# ============================================================================
# RESPONSE FORMATS
# ============================================================================

# GET /api/v1/content/{concept_id}
"""
{
    "concept_id": "python-variables-01",
    "title": "Variables",
    "problem": "...",
    "system": "...",
    "win": "...",

    // Code examples now use CodeExample model
    "code_examples": [
        {
            "code": "age = 25\\nprint(age)  # Output: 25",
            "expected_output": "25",
            "runnable": true
        },
        {
            "code": "name = 'Alice'\\nprint(name)  # Output: Alice",
            "expected_output": "Alice",
            "runnable": true
        }
    ],

    // Production-grade quality fields
    "mode": "coach",
    "libraries": ["core-python"],
    "difficulty": "beginner",
    "prerequisites": [],
    "tags": ["basics", "variables"],

    // Quality metadata (from v2.0 validation)
    "quality_score": 87,
    "citation_density": 1.2,
    "coverage_score": 0.72,
    "gates_passed": true,
    "validated_at": "2025-11-08T10:30:00Z",
    "validator_version": "2.0"
}
"""

# GET /api/v1/content/list
"""
{
    "total": 42,
    "limit": 10,
    "offset": 0,
    "concepts": [
        {
            "concept_id": "python-variables-01",
            "title": "Variables",
            "difficulty": "beginner",
            "quality_score": 87,  // Overall score from 10-criterion rubric
            "citation_density": 1.2,
            "gates_passed": true,
            "tags": ["basics"]
        },
        ...
    ]
}
"""

# GET /api/v1/content/search
"""
{
    "query": "how to store data",
    "total": 5,
    "concepts": [
        {
            "concept_id": "python-variables-01",
            "title": "Variables",
            "relevance_score": 0.92,
            "quality_score": 87,  // NEW: Include quality in search results
            "gates_passed": true,  // NEW: Quality gate status
            "excerpt": "Variables work like labeled boxes that store data..."
        },
        ...
    ]
}
"""

# GET /api/v1/questions/{concept_id}
"""
{
    "concept_id": "python-variables-01",
    "total": 5,
    "questions": [
        {
            "question_id": "q-variables-mc-01",
            "question_text": "What happens when you assign a value to a variable?",
            "question_type": "multiple_choice",
            "options": ["...", "...", "...", "..."],
            "difficulty": "beginner",
            "blooms_level": "understand",
            "quality_score": 82  // From 10-criterion rubric (adapted for questions)
        },
        ...
    ]
}
"""

# ============================================================================
# CURL EXAMPLES (For Testing)
# ============================================================================

"""
# Get concept
curl -X GET http://localhost:9000/api/v1/content/python-variables-01 \\
  -H "Authorization: Bearer YOUR_API_KEY"

# List concepts (with production-grade filters)
curl -X GET "http://localhost:9000/api/v1/content/list?difficulty=beginner&min_quality_score=85&min_citation_density=1.0&limit=5" \\
  -H "Authorization: Bearer YOUR_API_KEY"

# Search concepts
curl -X GET "http://localhost:9000/api/v1/content/search?q=how%20to%20store%20data&limit=3" \\
  -H "Authorization: Bearer YOUR_API_KEY"

# Get questions
curl -X GET http://localhost:9000/api/v1/questions/python-variables-01 \\
  -H "Authorization: Bearer YOUR_API_KEY"

# Get random question
curl -X GET "http://localhost:9000/api/v1/questions/random?difficulty=beginner" \\
  -H "Authorization: Bearer YOUR_API_KEY"

# Get prerequisites
curl -X GET http://localhost:9000/api/v1/content/python-lists-01/prerequisites \\
  -H "Authorization: Bearer YOUR_API_KEY"

# Get next concepts
curl -X GET http://localhost:9000/api/v1/content/python-variables-01/next \\
  -H "Authorization: Bearer YOUR_API_KEY"
"""

# ============================================================================
# AUTHENTICATION
# ============================================================================

"""
AXIS AI authenticates to Backend using API key.

Request Header:
Authorization: Bearer <AXIS_API_KEY>

Backend validates:
- API key is valid
- AXIS AI is authorized to access content
- Rate limiting (max 100 requests/minute)

Security:
- API key stored in environment variable (never committed)
- HTTPS only in production
- Rate limiting to prevent abuse
"""

# ============================================================================
# ERROR SCENARIOS & HANDLING
# ============================================================================

"""
ERROR 1: Concept Not Found
Request: GET /api/v1/content/invalid-id
Response: 404 Not Found
{
    "status": "error",
    "error": "Concept not found",
    "details": "concept_id 'invalid-id' does not exist",
    "code": 404
}

ERROR 2: Unauthorized
Request: GET /api/v1/content/python-variables-01
Response: 401 Unauthorized (missing or invalid API key)
{
    "status": "error",
    "error": "Unauthorized",
    "details": "Valid API key required",
    "code": 401
}

ERROR 3: Rate Limit Exceeded
Request: 101st request in 1 minute
Response: 429 Too Many Requests
{
    "status": "error",
    "error": "Rate limit exceeded",
    "details": "Maximum 100 requests per minute",
    "code": 429,
    "retry_after": 60
}
Headers:
    Retry-After: 60  // Seconds until rate limit resets

Note: Client should respect Retry-After header and implement exponential backoff.

ERROR 4: No Results for Search
Request: GET /api/v1/content/search?q=quantum physics
Response: 200 OK (empty results)
{
    "query": "quantum physics",
    "total": 0,
    "concepts": []
}

ERROR 5: Quality Threshold Not Met
Request: GET /api/v1/content/list?min_quality_score=90
Response: 200 OK (fewer results)
{
    "total": 5,  // Only 5 concepts meet 90+ threshold
    "concepts": [...]
}
"""

# ============================================================================
# PERFORMANCE OPTIMIZATION
# ============================================================================

"""
CACHING STRATEGY:
- Backend caches frequently accessed concepts (1 hour TTL)
- AXIS AI caches concept data locally (5 minutes TTL)
- Search results cached for same query (10 minutes TTL)

PAGINATION:
- Default limit: 10 items
- Max limit: 100 items
- Use offset for pagination (offset=0, 10, 20...)

COMPRESSION:
- All responses gzip compressed
- Reduces bandwidth by ~70%

RATE LIMITING:
- AXIS AI: 100 requests/minute
- Per-user: 20 requests/minute (if multi-user)

QUALITY FILTERING:
- Backend pre-filters to min_quality_score (default 85)
- Only validated content served to AXIS AI
- No re-validation needed on AXIS AI side
"""

# ============================================================================
# QUALITY ASSURANCE
# ============================================================================

"""
PRODUCTION-GRADE QUALITY STANDARDS (v2.0):

All content served to AXIS AI has been validated with:

10-CRITERION RUBRIC (100 points total):
1. Groundedness & Citation Quality (0-20 pts)
2. Technical Correctness (0-15 pts)
3. People-First Pedagogy (0-15 pts)
4. PSW Actionability (0-10 pts)
5. Mode Fidelity (0-10 pts)
6. Self-Paced Scaffolding (0-10 pts)
7. Retrieval Quality (0-10 pts)
8. Clarity (0-5 pts)
9. Bloom Alignment (0-3 pts)
10. People-First Language (0-2 pts)

QUALITY GATES (must all pass):
- coverage_score ≥ 0.65 (content adequacy)
- citation_density ≥ 1.0 (minimum citations)
- exec_ok = true (all code executes)
- scope_ok = true (approved libraries only)

PASS CRITERIA:
- Overall score ≥ 85 (raised from 70)
- All core gates passed

TELEMETRY TRACKED:
- run_id, trace_url (LangSmith)
- model, provider (e.g., gpt-4o-2024-11-20, openai)
- prompt_version, graph_version
- coverage_score, citation_density, unique_sources
- mode_ratio, scaffold_depth, exec_ok
- latency_ms, tokens

Backend guarantees all content meets these standards before serving to AXIS AI.
"""

# ============================================================================
# SUCCESS CRITERIA
# ============================================================================

"""
Integration is successful if:
✅ AXIS AI can retrieve concepts by ID
✅ AXIS AI can search concepts semantically
✅ AXIS AI can get practice questions
✅ AXIS AI can navigate learning path (prerequisites/next)
✅ Authentication works (API key validation)
✅ Rate limiting enforced
✅ Response time < 200ms for single concept
✅ Response time < 500ms for search (RAG)
✅ Error handling graceful
✅ All content meets production-grade quality standards (score ≥85, gates passed)
✅ Quality metadata available for AXIS AI decision-making
"""

# ============================================================================
# VERSION HISTORY
# ============================================================================

"""
v1.0 (2025-11-06):
- Initial API contract
- Content retrieval endpoints
- Question retrieval endpoints
- Learning path navigation
- Search/RAG integration
- Authentication specification

v2.0 (2025-11-06):
- Updated: PythonConcept → AethelgardConcept references
- Updated: min_quality_score default from 70 to 85
- Added: min_citation_density filter parameter
- Added: Quality metadata in all responses (quality_score, citation_density, gates_passed)
- Added: AXIS_API_KEY environment variable
- Added: Production-grade quality standards documentation
- Added: 10-criterion rubric reference
- Added: Quality gates documentation
- Added: Telemetry fields reference
- Updated: Response format examples to include v2.0 quality fields
- Updated: CURL examples with quality filters
- Updated: Code examples handling (CodeExample model support)
- Note: AXIS AI receives only validated content (no validation needed on AXIS side)
"""
