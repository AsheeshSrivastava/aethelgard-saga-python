"""
Shared Data Models for Aethelgard Ecosystem - PRODUCTION GRADE
================================================================

**Systems Using These Models:**
1. Research Portal (creates AethelgardConcepts)
2. QuestionForge (creates Questions)
3. Quality Checker (validates both, returns QualityReports)
4. Backend (stores validated content)
5. AXIS AI (retrieves validated content)

**Version:** 2.0 (Production-Grade with Gates, Telemetry, Citations)
**Created:** 2025-11-06
**Last Updated:** 2025-11-06
**Breaking Changes:** Yes (v1.0 → v2.0)
  - 10-criterion rubric (was 7)
  - Pass threshold 85+ (was 70+)
  - Code examples now structured (was List[str])
  - Citations system added
  - Gates system added
  - Telemetry object added
  - Pydantic v2 patterns (.model_dump())
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal
from enum import Enum
from datetime import datetime


# ============================================================================
# ENUMS
# ============================================================================

class DifficultyLevel(str, Enum):
    """Difficulty levels for content and questions"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Mode(str, Enum):
    """AXIS AI pedagogical modes"""
    COACH = "coach"        # 0.15-0.30 question ratio (mostly explains)
    HYBRID = "hybrid"      # 0.30-0.45 question ratio (balanced)
    SOCRATIC = "socratic"  # 0.50-0.70 question ratio (mostly asks)


class Library(str, Enum):
    """Approved Python libraries for curriculum scope"""
    CORE_PYTHON = "core-python"
    NUMPY = "numpy"
    PANDAS = "pandas"
    MATPLOTLIB = "matplotlib"
    SEABORN = "seaborn"
    SCIKIT_LEARN = "scikit-learn"


class BloomsLevel(str, Enum):
    """Bloom's Taxonomy cognitive levels"""
    REMEMBER = "remember"
    UNDERSTAND = "understand"
    APPLY = "apply"
    ANALYZE = "analyze"
    EVALUATE = "evaluate"
    CREATE = "create"


class QuestionType(str, Enum):
    """Practice question types"""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    FILL_BLANK = "fill_blank"
    CODE_OUTPUT = "code_output"
    CODE_WRITING = "code_writing"


class CitationSource(str, Enum):
    """Citation retrieval sources"""
    VECTOR = "vector"  # Retrieved from vector database
    WEB = "web"        # Retrieved from web search


# ============================================================================
# NEW MODELS (Production-Grade)
# ============================================================================

class Citation(BaseModel):
    """Provisional citation for groundedness checking"""
    source: CitationSource
    title: str
    locator: str  # e.g., "§2.3" or "line 42"
    url: Optional[str] = None
    license: Optional[str] = None

    model_config = {"frozen": True}


class CodeExample(BaseModel):
    """Structured code example with execution metadata"""
    code: str = Field(..., min_length=10)
    expected_output: Optional[str] = None
    runnable: bool = True

    model_config = {"frozen": True}


class GateStatus(BaseModel):
    """Quality gate check result"""
    name: str  # e.g., "coverage_score", "exec_ok", "scope_ok"
    passed: bool
    details: Optional[str] = None


class Telemetry(BaseModel):
    """Observability metrics for quality validation"""
    # Run metadata
    run_id: str
    trace_url: Optional[str] = None
    model: str
    provider: str
    prompt_version: str
    graph_version: str

    # Quality metrics
    coverage_score: float = Field(..., ge=0.0, le=1.0)
    citation_density: float = Field(..., ge=0.0)  # citations per claim
    unique_sources: int = Field(..., ge=0)

    # Pedagogy metrics
    mode_ratio: float = Field(..., ge=0.0, le=1.0)  # question/(question+statement)
    scaffold_depth: int = Field(..., ge=0)  # scaffolding layers
    exec_ok: bool  # code execution succeeded

    # Performance metrics
    latency_ms: int = Field(..., ge=0)
    tokens: int = Field(..., ge=0)


# ============================================================================
# CONTENT MODELS
# ============================================================================

class AethelgardConcept(BaseModel):
    """
    Python learning concept with PSW Framework + Production Features

    **PSW Framework:**
    - Problem: What learning challenge does this address? (min 50 chars)
    - System: Structured approach to solve it (min 100 chars)
    - Win: Practical application/benefit (min 50 chars)

    **Production Features:**
    - Mode: Coach/Hybrid/Socratic pedagogy
    - Bloom: Optional cognitive level
    - Libraries: Scoped to approved curriculum
    - Code Examples: Structured with execution metadata
    - Citations: Provisional citations for groundedness
    """

    # Core identification
    concept_id: str = Field(..., pattern=r"^[a-z0-9-]+$")
    title: str = Field(..., min_length=5, max_length=100)

    # PSW Framework (Metacognitive Learning)
    problem: str = Field(..., min_length=50, max_length=500)
    system: str = Field(..., min_length=100, max_length=1000)
    win: str = Field(..., min_length=50, max_length=500)

    # Code & Resources
    code_examples: List[CodeExample] = Field(..., min_length=1, max_length=10)
    provisional_citations: List[Citation] = Field(default_factory=list)

    # Pedagogy
    mode: Mode = Mode.COACH
    bloom: Optional[BloomsLevel] = None
    difficulty: DifficultyLevel

    # Curriculum structure
    prerequisites: List[str] = Field(default_factory=list)
    libraries: List[Library] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)

    # Metadata
    created_at: Optional[str] = None

    @field_validator('created_at', mode='before')
    @classmethod
    def set_created_at(cls, v):
        if v is None:
            return datetime.utcnow().isoformat() + "Z"
        return v

    @field_validator('libraries')
    @classmethod
    def validate_libraries(cls, v):
        if not v:  # Empty list is valid (core Python only)
            return v
        # Check all are approved
        approved = {lib.value for lib in Library}
        invalid = [lib for lib in v if lib not in approved]
        if invalid:
            raise ValueError(f"Invalid libraries: {invalid}. Must be from: {approved}")
        return v


class Question(BaseModel):
    """
    Practice question for concept validation

    **Question Types:**
    - multiple_choice: Requires options (min 2, max 6)
    - true_false: Requires options=["True", "False"]
    - fill_blank: No options
    - code_output: No options
    - code_writing: No options
    """

    # Core identification
    question_id: str = Field(..., pattern=r"^[a-z0-9-]+$")
    concept_id: str = Field(..., pattern=r"^[a-z0-9-]+$")

    # Question content
    question_text: str = Field(..., min_length=10, max_length=500)
    question_type: QuestionType
    options: Optional[List[str]] = None
    correct_answer: str = Field(..., min_length=1)

    # Pedagogy
    difficulty: DifficultyLevel
    blooms_level: BloomsLevel

    # Learning support
    explanation: Optional[str] = None
    hints: Optional[List[str]] = None

    # Metadata
    created_at: Optional[str] = None

    @field_validator('created_at', mode='before')
    @classmethod
    def set_created_at(cls, v):
        if v is None:
            return datetime.utcnow().isoformat() + "Z"
        return v

    @field_validator('options')
    @classmethod
    def validate_options(cls, v, info):
        question_type = info.data.get('question_type')

        if question_type == QuestionType.MULTIPLE_CHOICE:
            if not v or len(v) < 2:
                raise ValueError("multiple_choice requires at least 2 options")
            if len(v) > 6:
                raise ValueError("multiple_choice allows maximum 6 options")

        if question_type == QuestionType.TRUE_FALSE:
            if v != ["True", "False"]:
                raise ValueError("true_false requires options=['True', 'False']")

        if question_type in [QuestionType.FILL_BLANK, QuestionType.CODE_OUTPUT, QuestionType.CODE_WRITING]:
            if v is not None:
                raise ValueError(f"{question_type.value} should not have options")

        return v


# ============================================================================
# QUALITY VALIDATION
# ============================================================================

class ValidationIssue(BaseModel):
    """Single validation issue found during quality check"""
    severity: Literal["critical", "high", "medium", "low"]
    category: str  # e.g., "clarity", "technical", "pedagogy"
    message: str
    suggestion: Optional[str] = None
    location: Optional[str] = None  # e.g., "code_examples[0]", "problem field"


class QualityReport(BaseModel):
    """
    Production-Grade Quality Validation Report

    **10-Criterion Rubric (Sum = 100):**
    1. Groundedness & Citation Quality (20 pts)
    2. Technical Correctness (15 pts)
    3. People-First Pedagogy (15 pts)
    4. PSW Actionability (10 pts)
    5. Mode Fidelity (10 pts)
    6. Self-Paced Scaffolding (10 pts)
    7. Retrieval Quality (10 pts)
    8. Clarity (5 pts)
    9. Bloom Alignment (3 pts)
    10. People-First Language (2 pts)

    **Quality Gates (All Must Pass):**
    - coverage_score ≥ 0.65
    - citation_density ≥ 1.0
    - exec_ok = true
    - scope_ok = true

    **Pass Threshold:**
    - overall_score ≥ 85 AND all core gates passed
    """

    # Item identification
    item_id: str
    item_type: Literal["content", "question"]
    overall_score: int = Field(..., ge=0, le=100)

    # 10-Criterion Scores (Production Rubric)
    groundedness_citation_score: int = Field(..., ge=0, le=20)
    technical_correctness_score: int = Field(..., ge=0, le=15)
    people_first_pedagogy_score: int = Field(..., ge=0, le=15)
    psw_actionability_score: int = Field(..., ge=0, le=10)
    mode_fidelity_score: int = Field(..., ge=0, le=10)
    self_paced_scaffolding_score: int = Field(..., ge=0, le=10)
    retrieval_quality_score: int = Field(..., ge=0, le=10)
    clarity_score: int = Field(..., ge=0, le=5)
    bloom_alignment_score: int = Field(..., ge=0, le=3)
    people_first_language_score: int = Field(..., ge=0, le=2)

    # Quality gates
    gates: List[GateStatus]

    # Telemetry (observability)
    telemetry: Telemetry

    # Feedback
    issues: List[ValidationIssue]
    strengths: List[str]
    suggestions: List[str]

    # Pass/Fail determination
    passes_quality: bool

    # Metadata
    validated_at: str
    validator_version: str = "2.0"

    @field_validator('validated_at', mode='before')
    @classmethod
    def set_validated_at(cls, v):
        if v is None:
            return datetime.utcnow().isoformat() + "Z"
        return v

    @field_validator('overall_score')
    @classmethod
    def validate_overall_score(cls, v, info):
        """Verify overall score matches sum of criteria"""
        scores = [
            info.data.get('groundedness_citation_score', 0),
            info.data.get('technical_correctness_score', 0),
            info.data.get('people_first_pedagogy_score', 0),
            info.data.get('psw_actionability_score', 0),
            info.data.get('mode_fidelity_score', 0),
            info.data.get('self_paced_scaffolding_score', 0),
            info.data.get('retrieval_quality_score', 0),
            info.data.get('clarity_score', 0),
            info.data.get('bloom_alignment_score', 0),
            info.data.get('people_first_language_score', 0),
        ]
        total = sum(scores)
        if v != total:
            raise ValueError(f"overall_score ({v}) must equal sum of criteria scores ({total})")
        return v

    @field_validator('passes_quality')
    @classmethod
    def validate_passes_quality(cls, v, info):
        """
        Production pass criteria:
        - overall_score ≥ 85
        - All core gates passed
        """
        overall_score = info.data.get('overall_score', 0)
        gates = info.data.get('gates', [])

        # Check score threshold
        score_pass = overall_score >= 85

        # Check core gates
        core_gates = {'coverage_score', 'citation_density', 'exec_ok', 'scope_ok'}
        gates_pass = all(
            gate.passed
            for gate in gates
            if gate.name in core_gates
        )

        expected_pass = score_pass and gates_pass

        if v != expected_pass:
            raise ValueError(
                f"passes_quality mismatch: expected {expected_pass} "
                f"(score≥85: {score_pass}, gates: {gates_pass}), got {v}"
            )

        return v


# ============================================================================
# BATCH OPERATIONS
# ============================================================================

class BatchValidationRequest(BaseModel):
    """Request for batch validation of multiple items"""
    items: List[AethelgardConcept | Question] = Field(..., min_length=1, max_length=100)
    validation_type: Literal["quick", "full"] = "full"
    strict: bool = True  # If True, fail entire batch on first failure


class BatchValidationResponse(BaseModel):
    """Response for batch validation"""
    total_items: int
    passed: int
    failed: int
    reports: List[QualityReport]
    timestamp: str

    @field_validator('timestamp', mode='before')
    @classmethod
    def set_timestamp(cls, v):
        if v is None:
            return datetime.utcnow().isoformat() + "Z"
        return v


# ============================================================================
# API RESPONSE WRAPPERS
# ============================================================================

class SuccessResponse(BaseModel):
    """Standard success response wrapper"""
    status: Literal["success"] = "success"
    message: str
    data: dict
    timestamp: str

    @field_validator('timestamp', mode='before')
    @classmethod
    def set_timestamp(cls, v):
        if v is None:
            return datetime.utcnow().isoformat() + "Z"
        return v


class ErrorResponse(BaseModel):
    """Standard error response wrapper"""
    status: Literal["error"] = "error"
    error: str
    details: Optional[str] = None
    code: int
    timestamp: str

    @field_validator('timestamp', mode='before')
    @classmethod
    def set_timestamp(cls, v):
        if v is None:
            return datetime.utcnow().isoformat() + "Z"
        return v


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_success_response(message: str, data: dict) -> dict:
    """Create standard success response"""
    response = SuccessResponse(message=message, data=data, timestamp=None)
    return response.model_dump()


def create_error_response(error: str, code: int, details: Optional[str] = None) -> dict:
    """Create standard error response"""
    response = ErrorResponse(error=error, code=code, details=details, timestamp=None)
    return response.model_dump()


# ============================================================================
# EXAMPLES (Production-Grade)
# ============================================================================

def example_aethelgard_concept() -> AethelgardConcept:
    """Example concept with production features"""
    return AethelgardConcept(
        concept_id="python-variables-01",
        title="Variables in Python",
        problem=(
            "Learners struggle to understand how data is stored and referenced "
            "in Python programs, often treating variables as 'boxes' rather than "
            "name-value bindings."
        ),
        system=(
            "Variables in Python are names that reference objects in memory. "
            "When you write x = 10, Python creates an integer object with value 10 "
            "and binds the name 'x' to it. Multiple names can reference the same object. "
            "Understanding this reference model prevents confusion about mutability, "
            "copying, and parameter passing."
        ),
        win=(
            "Master variable assignment and reference semantics to write predictable, "
            "bug-free code. Understand why x = y doesn't copy in all cases, and when "
            "mutable objects can cause unexpected behavior."
        ),
        code_examples=[
            CodeExample(
                code="x = 10\ny = x\nprint(f'x={x}, y={y}')",
                expected_output="x=10, y=10",
                runnable=True
            ),
            CodeExample(
                code="numbers = [1, 2, 3]\nalias = numbers\nalias.append(4)\nprint(numbers)",
                expected_output="[1, 2, 3, 4]",
                runnable=True
            )
        ],
        provisional_citations=[
            Citation(
                source=CitationSource.VECTOR,
                title="Python Data Model",
                locator="§3.1",
                url="https://docs.python.org/3/reference/datamodel.html",
                license="PSF-2.0"
            )
        ],
        mode=Mode.COACH,
        bloom=BloomsLevel.UNDERSTAND,
        difficulty=DifficultyLevel.BEGINNER,
        prerequisites=[],
        libraries=[Library.CORE_PYTHON],
        tags=["basics", "variables", "references"]
    )


def example_question() -> Question:
    """Example question"""
    return Question(
        question_id="q-variables-mc-01",
        concept_id="python-variables-01",
        question_text="What happens when you assign a value to a variable in Python?",
        question_type=QuestionType.MULTIPLE_CHOICE,
        options=[
            "Python creates a labeled container to store the value",
            "Python creates a name that references an object in memory",
            "Python copies the value into a new memory location",
            "Python converts the value to a string"
        ],
        correct_answer="Python creates a name that references an object in memory",
        difficulty=DifficultyLevel.BEGINNER,
        blooms_level=BloomsLevel.UNDERSTAND,
        explanation="Variables in Python are names that reference objects, not containers.",
        hints=["Think about the reference model, not the box model"]
    )


def example_quality_report() -> QualityReport:
    """Example quality report with gates and telemetry"""
    return QualityReport(
        item_id="python-variables-01",
        item_type="content",
        overall_score=88,

        # 10 criterion scores (sum = 88)
        groundedness_citation_score=18,  # /20
        technical_correctness_score=14,  # /15
        people_first_pedagogy_score=13,  # /15
        psw_actionability_score=9,       # /10
        mode_fidelity_score=9,           # /10
        self_paced_scaffolding_score=9,  # /10
        retrieval_quality_score=9,       # /10
        clarity_score=4,                 # /5
        bloom_alignment_score=2,         # /3
        people_first_language_score=1,   # /2

        # Gates (all passed)
        gates=[
            GateStatus(name="coverage_score", passed=True, details="0.78 ≥ 0.65"),
            GateStatus(name="citation_density", passed=True, details="1.2 ≥ 1.0"),
            GateStatus(name="exec_ok", passed=True, details="All code executed successfully"),
            GateStatus(name="scope_ok", passed=True, details="All content in approved scope")
        ],

        # Telemetry
        telemetry=Telemetry(
            run_id="run_abc123",
            trace_url="https://langsmith.example.com/runs/abc123",
            model="gpt-4o-latest",
            provider="openai",
            prompt_version="v2.3",
            graph_version="v1.0",
            coverage_score=0.78,
            citation_density=1.2,
            unique_sources=3,
            mode_ratio=0.22,
            scaffold_depth=2,
            exec_ok=True,
            latency_ms=1200,
            tokens=1500
        ),

        # Feedback
        issues=[
            ValidationIssue(
                severity="low",
                category="people_first_language",
                message="Consider using 'learner' instead of 'user' for consistency",
                suggestion="Replace 'user' with 'learner' in problem statement"
            )
        ],
        strengths=[
            "Clear PSW structure with concrete examples",
            "Accurate reference model explanation",
            "Code examples are runnable and well-chosen",
            "Citations properly formatted"
        ],
        suggestions=[
            "Add example showing mutable vs immutable behavior",
            "Include common pitfall: list aliasing"
        ],

        # Passes (88 ≥ 85 AND all gates passed)
        passes_quality=True,

        validated_at=None  # Auto-set
    )


# ============================================================================
# VERSION HISTORY
# ============================================================================

"""
v2.0 (2025-11-06) - Production-Grade Upgrade:
- BREAKING: Changed from 7 to 10 quality criteria
- BREAKING: Pass threshold 85 (was 70)
- BREAKING: Code examples now structured (CodeExample model)
- BREAKING: All Pydantic v2 patterns (.model_dump())
- NEW: Mode enum (coach/hybrid/socratic)
- NEW: Library enum (approved curriculum scope)
- NEW: Citation model (groundedness)
- NEW: CodeExample model (structured with execution metadata)
- NEW: GateStatus model (quality gates)
- NEW: Telemetry model (observability metrics)
- RENAMED: PythonConcept → AethelgardConcept
- ADDED: AethelgardConcept.mode, .bloom, .libraries, .provisional_citations
- UPGRADED: QualityReport with 10 criteria, gates, telemetry
- UPGRADED: All validators to Pydantic v2
- UPGRADED: Examples to production-grade patterns

v1.0 (2025-11-06) - Initial shared models:
- PythonConcept with PSW framework
- Question with 5 types
- QualityReport with 7 criteria
- Batch validation support
- Standard response wrappers
"""
