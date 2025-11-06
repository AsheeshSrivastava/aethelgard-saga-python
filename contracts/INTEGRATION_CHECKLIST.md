# Integration Checklist for Days 6-7
**The Zyric AI Ecosystem Integration**

**Purpose:** Step-by-step verification guide for integrating all 5 systems on Days 6-7.

**Version:** 1.0
**Created:** 2025-11-06

---

## 🎯 INTEGRATION OVERVIEW

**Timeline:**
- **Day 6:** Individual system testing + First integration attempts
- **Day 7:** Full flow testing + Bug fixes + Performance testing

**Integration Order:**
1. Research Portal → Quality Checker
2. QuestionForge → Quality Checker
3. Backend → Quality Checker (batch)
4. Backend → AXIS AI
5. Full end-to-end flows

**Success Criteria:**
- ✅ All 4 communication flows working
- ✅ Data formats 100% compatible
- ✅ No critical bugs
- ✅ Response times within targets
- ✅ Error handling graceful

---

## 📋 PRE-INTEGRATION CHECKLIST (Days 0-5)

### ChatGPT's Deliverables (Days 0-5)

**Research Portal:**
- [ ] Content generation service implemented
- [ ] PSW framework content creator working
- [ ] Code example generator working
- [ ] Metadata (tags, difficulty, prerequisites) assignment
- [ ] OpenAI API integration complete
- [ ] Environment variables configured (.env)
- [ ] Unit tests passing (>80% coverage)
- [ ] Deployment ready (localhost:PORT or deployed)

**QuestionForge:**
- [ ] Question generation service implemented
- [ ] All 5 question types supported (MCQ, True/False, Fill-in-blank, Code Output, Code Writing)
- [ ] Bloom's taxonomy assignment working
- [ ] Difficulty level assignment working
- [ ] Unit tests passing (>80% coverage)
- [ ] Deployment ready

**Aethelgard Backend:**
- [ ] FastAPI application running
- [ ] Database setup complete (SQLite or PostgreSQL)
- [ ] Vector database setup (LanceDB or similar)
- [ ] API routes defined (all GET/POST endpoints)
- [ ] Authentication middleware (API key validation)
- [ ] Storage service (save concepts/questions)
- [ ] Retrieval service (RAG search)
- [ ] Unit tests passing (>80% coverage)
- [ ] Deployment ready (localhost:9000 recommended)

**AXIS AI:**
- [ ] ChatGPT integration setup
- [ ] API client for Backend implemented
- [ ] RAG retrieval workflow implemented
- [ ] Question answering logic working
- [ ] Mode selector (Coach/Hybrid/Socratic) implemented
- [ ] Unit tests passing (>80% coverage)
- [ ] Deployment ready

### Claude's Deliverables (Days 0-5)

**Quality Checker:**
- [ ] FastAPI application running
- [ ] Content validation service (7 criteria)
- [ ] Question validation service (7 criteria)
- [ ] Batch validation service
- [ ] QualityReport generation working
- [ ] Gradio UI for manual testing
- [ ] OpenAI API integration (for advanced checks)
- [ ] Unit tests passing (>80% coverage)
- [ ] Deployment ready (localhost:8000 recommended)

### Shared Deliverables (All Developers)

**Critical:**
- [ ] All systems import from `shared_models.py` (no duplicate models!)
- [ ] All systems use SuccessResponse/ErrorResponse formats
- [ ] All systems use Pydantic for validation
- [ ] All systems have .env files with required keys
- [ ] All systems have requirements.txt with pinned versions
- [ ] All systems can run independently
- [ ] All systems have README with setup instructions

---

## 🧪 DAY 6: INDIVIDUAL SYSTEM TESTING & FIRST INTEGRATION

### Morning: Individual System Verification (2 hours)

**Goal:** Verify each system works independently before connecting.

#### Test 1: Quality Checker (Claude)

**Manual Test via Gradio UI:**
1. Start Quality Checker: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
2. Open Gradio UI: http://localhost:8000
3. Test content validation:
   ```python
   # Paste sample PythonConcept JSON
   {
     "concept_id": "test-001",
     "title": "Test Concept",
     "problem": "This is a test problem with at least 50 characters to meet minimum length.",
     "system": "This is a test system explanation with at least 100 characters to meet the minimum length requirement for validation.",
     "win": "This is a test win statement with at least 50 characters.",
     "code_examples": ["x = 5", "print(x)"],
     "difficulty": "beginner",
     "prerequisites": [],
     "tags": ["test"]
   }
   ```
4. Expected: QualityReport with scores, passes_quality=true/false
5. Test question validation similarly

**API Test via CURL:**
```bash
# Test content validation endpoint
curl -X POST http://localhost:8000/api/v1/content/validate \
  -H "Content-Type: application/json" \
  -d @test_concept.json

# Test question validation endpoint
curl -X POST http://localhost:8000/api/v1/questions/validate \
  -H "Content-Type: application/json" \
  -d @test_question.json
```

**Checklist:**
- [ ] Content validation returns QualityReport
- [ ] Question validation returns QualityReport
- [ ] Batch validation works (test with 3 items)
- [ ] Error responses use ErrorResponse format
- [ ] Success responses use SuccessResponse format
- [ ] Gradio UI working

---

#### Test 2: Research Portal (ChatGPT)

**Manual Test:**
1. Start Research Portal: `python -m app.main` or similar
2. Trigger content generation for test concept
3. Verify PythonConcept object created
4. Verify all required fields present
5. Verify data types match shared_models.py

**Unit Test:**
```bash
pytest tests/test_content_generation.py -v
```

**Checklist:**
- [ ] Content generation produces valid PythonConcept
- [ ] All required fields populated
- [ ] Code examples non-empty
- [ ] PSW fields meet minimum length
- [ ] Tags and metadata correct
- [ ] Unit tests passing

---

#### Test 3: QuestionForge (ChatGPT)

**Manual Test:**
1. Start QuestionForge
2. Generate test question for each type:
   - Multiple choice
   - True/False
   - Fill-in-blank
   - Code output
   - Code writing
3. Verify Question objects created
4. Verify all required fields present

**Checklist:**
- [ ] All 5 question types generate correctly
- [ ] Bloom's level assigned
- [ ] Difficulty level assigned
- [ ] Options present for MCQ/True-False
- [ ] Correct answer present
- [ ] Unit tests passing

---

#### Test 4: Aethelgard Backend (ChatGPT)

**API Test:**
```bash
# Test health check
curl http://localhost:9000/health

# Test concept storage (should fail - no data yet)
curl http://localhost:9000/api/v1/content/test-001
```

**Checklist:**
- [ ] Backend API running
- [ ] Database connected
- [ ] Vector database initialized
- [ ] All routes defined
- [ ] Authentication middleware working
- [ ] Storage service ready
- [ ] Retrieval service ready

---

#### Test 5: AXIS AI (ChatGPT)

**Manual Test:**
1. Start AXIS AI
2. Query Backend (should fail gracefully - no data yet)
3. Test mode selector
4. Test fallback behavior

**Checklist:**
- [ ] API client configured
- [ ] Authentication working
- [ ] RAG retrieval logic implemented
- [ ] Mode selector working
- [ ] Error handling graceful

---

### Afternoon: First Integration Tests (3 hours)

#### Integration 1: Research Portal → Quality Checker

**Goal:** Research Portal sends concept to Quality Checker and receives QualityReport.

**Test Steps:**
1. Start Quality Checker on localhost:8000
2. Start Research Portal
3. Generate test concept in Research Portal
4. Research Portal calls Quality Checker API:
   ```python
   response = requests.post(
       "http://localhost:8000/api/v1/content/validate",
       json=concept.dict()
   )
   ```
5. Verify response format matches SuccessResponse
6. Verify QualityReport extracted correctly

**Common Issues & Fixes:**

**Issue 1: Connection Refused**
- **Symptom:** `requests.exceptions.ConnectionError`
- **Fix:** Verify Quality Checker is running on correct port
- **Verify:** `curl http://localhost:8000/health`

**Issue 2: 422 Unprocessable Entity**
- **Symptom:** Pydantic validation error
- **Cause:** Field name mismatch between Research Portal and shared_models.py
- **Fix:** Update Research Portal to match exact field names
- **Debug:** Check error response for field name

**Issue 3: 500 Internal Server Error**
- **Symptom:** Quality Checker crashes
- **Fix:** Check Quality Checker logs for stack trace
- **Common cause:** Missing import, incorrect function call

**Success Criteria:**
- [ ] Research Portal successfully sends concept
- [ ] Quality Checker returns QualityReport
- [ ] Overall_score calculated correctly
- [ ] passes_quality boolean correct
- [ ] Issues/strengths/suggestions populated
- [ ] No errors in logs

---

#### Integration 2: QuestionForge → Quality Checker

**Goal:** QuestionForge sends question to Quality Checker and receives QualityReport.

**Test Steps:**
1. Ensure Quality Checker running
2. Start QuestionForge
3. Generate test question
4. QuestionForge calls Quality Checker API:
   ```python
   response = requests.post(
       "http://localhost:8000/api/v1/questions/validate",
       json=question.dict()
   )
   ```
5. Verify QualityReport received

**Common Issues & Fixes:**

**Issue 1: Question Type Not Recognized**
- **Symptom:** Validation error on question_type field
- **Fix:** Use exact enum values from shared_models.py
- **Correct values:** "multiple_choice", "true_false", "fill_blank", "code_output", "code_writing"

**Issue 2: Options Missing for MCQ**
- **Symptom:** Validation error "options required for multiple_choice"
- **Fix:** Ensure options list present and non-empty

**Issue 3: Bloom's Level Invalid**
- **Symptom:** Validation error on blooms_level field
- **Fix:** Use exact enum values: "remember", "understand", "apply", "analyze", "evaluate", "create"

**Success Criteria:**
- [ ] QuestionForge successfully sends question
- [ ] Quality Checker returns QualityReport
- [ ] Question-specific scoring (7 criteria) working
- [ ] Bloom's alignment checked
- [ ] Technical correctness verified
- [ ] No errors in logs

---

#### Integration 3: Backend Batch Validation

**Goal:** Backend sends multiple items to Quality Checker in one request.

**Test Steps:**
1. Ensure Quality Checker running
2. Start Backend
3. Create test batch (3 concepts + 2 questions)
4. Backend calls batch validation:
   ```python
   batch_request = BatchValidationRequest(
       items=[concept1, concept2, concept3, question1, question2],
       validation_type="full"
   )
   response = requests.post(
       "http://localhost:8000/api/v1/content/batch-validate",
       json=batch_request.dict()
   )
   ```
5. Verify BatchValidationResponse received

**Common Issues & Fixes:**

**Issue 1: Batch Size Exceeded**
- **Symptom:** 400 Bad Request "Batch too large"
- **Fix:** Limit batch to 100 items max
- **Solution:** Split into multiple batches

**Issue 2: Mixed Item Types**
- **Symptom:** Validation error on item type
- **Fix:** Batch can contain both concepts and questions
- **Verify:** shared_models.py allows Union[PythonConcept, Question]

**Issue 3: Timeout**
- **Symptom:** Request times out after 30 seconds
- **Cause:** Batch too large or Quality Checker slow
- **Fix:** Reduce batch size or increase timeout

**Performance Test:**
- [ ] Batch of 10 items: < 10 seconds
- [ ] Batch of 50 items: < 30 seconds
- [ ] Batch of 100 items: < 60 seconds

**Success Criteria:**
- [ ] Batch validation returns correct total_items count
- [ ] Passed/failed counts match individual results
- [ ] All individual QualityReports present
- [ ] Performance within targets
- [ ] No memory leaks (test with large batches)

---

### Evening: Backend → AXIS AI Integration (2 hours)

#### Integration 4: AXIS AI Content Retrieval

**Goal:** AXIS AI retrieves content from Backend.

**Prerequisite:** Backend has at least 5 validated concepts stored.

**Test Steps:**

**Step 1: Store Test Data in Backend**
```python
# Via Backend API or direct database insertion
# Store 5 concepts with varying difficulty and tags
```

**Step 2: Test Single Concept Retrieval**
```bash
# AXIS AI calls Backend
curl -X GET http://localhost:9000/api/v1/content/test-001 \
  -H "Authorization: Bearer AXIS_API_KEY"
```

**Expected Response:**
```json
{
  "concept_id": "test-001",
  "title": "Test Concept",
  "problem": "...",
  "system": "...",
  "win": "...",
  "code_examples": ["...", "..."],
  "difficulty": "beginner",
  "quality_score": 85
}
```

**Step 3: Test List Concepts**
```bash
curl -X GET "http://localhost:9000/api/v1/content/list?difficulty=beginner&limit=5"
```

**Step 4: Test RAG Search**
```bash
curl -X GET "http://localhost:9000/api/v1/content/search?q=how%20to%20store%20data&limit=3"
```

**Expected:** Ranked list with relevance_score

**Common Issues & Fixes:**

**Issue 1: 401 Unauthorized**
- **Symptom:** Missing or invalid API key
- **Fix:** Ensure AXIS_API_KEY in AXIS AI .env
- **Fix:** Ensure Backend validates API key

**Issue 2: Empty Search Results**
- **Symptom:** RAG search returns []
- **Cause:** Vector embeddings not generated
- **Fix:** Verify Backend generates embeddings on concept storage
- **Debug:** Check Backend vector database has entries

**Issue 3: Slow Search (>1 second)**
- **Symptom:** RAG search takes too long
- **Fix:** Optimize vector database indexing
- **Fix:** Reduce similarity computation complexity

**Success Criteria:**
- [ ] Single concept retrieval works
- [ ] List concepts with filters works
- [ ] RAG search returns relevant results
- [ ] Relevance scores reasonable (0.0-1.0)
- [ ] Response times within targets (<500ms)
- [ ] Authentication working
- [ ] Rate limiting enforced (100 req/min)

---

## 🔬 DAY 7: FULL FLOW TESTING & BUG FIXES

### Morning: End-to-End Flow Testing (3 hours)

#### Flow 1: Content Creation & Retrieval

**Full Pipeline:**
```
Research Portal → Quality Checker → Backend → AXIS AI
```

**Test Steps:**

1. **Research Portal generates new concept**
   - Use realistic topic (e.g., "Python Variables")
   - Verify all PSW fields populated

2. **Research Portal sends to Quality Checker**
   - POST /api/v1/content/validate
   - Verify QualityReport received
   - Check overall_score >= 70

3. **Research Portal sends to Backend** (if passed)
   - POST to Backend storage endpoint
   - Verify concept stored in database
   - Verify vector embedding generated

4. **AXIS AI retrieves concept**
   - Scenario: User asks "How do I store data in Python?"
   - AXIS searches: GET /api/v1/content/search?q=store data python
   - AXIS should find the new concept
   - AXIS retrieves: GET /api/v1/content/{concept_id}
   - AXIS generates answer using retrieved context

**Success Criteria:**
- [ ] Concept flows through all 4 systems
- [ ] No data loss or corruption
- [ ] Quality validation working
- [ ] RAG retrieval finds correct concept
- [ ] End-to-end time < 10 seconds
- [ ] Logs show complete trace

**Metrics to Collect:**
- Total time (seconds)
- Quality Checker time
- Backend storage time
- RAG search time
- Errors encountered

---

#### Flow 2: Question Creation & Retrieval

**Full Pipeline:**
```
QuestionForge → Quality Checker → Backend → AXIS AI
```

**Test Steps:**

1. **QuestionForge generates question**
   - Type: Multiple choice
   - Topic: Python variables
   - 4 options, 1 correct answer

2. **QuestionForge sends to Quality Checker**
   - POST /api/v1/questions/validate
   - Verify QualityReport (question-specific criteria)

3. **QuestionForge sends to Backend** (if passed)
   - POST to Backend question storage
   - Associate with concept_id

4. **AXIS AI retrieves questions**
   - GET /api/v1/questions/{concept_id}
   - GET /api/v1/questions/random?difficulty=beginner
   - Present question to learner
   - Validate learner answer

**Success Criteria:**
- [ ] Question flows through all systems
- [ ] Bloom's level validated
- [ ] Technical correctness checked
- [ ] AXIS can retrieve questions
- [ ] Random question selection works
- [ ] Answer validation working

---

#### Flow 3: Batch Processing

**Test Scenario:** Backend receives 20 concepts from Research Portal at once.

**Test Steps:**

1. Research Portal generates 20 concepts
2. Backend batch validates:
   ```python
   batch_request = BatchValidationRequest(
       items=concepts,
       validation_type="full"
   )
   ```
3. Quality Checker validates all 20
4. Backend stores passed concepts
5. AXIS AI can search across all concepts

**Success Criteria:**
- [ ] All 20 validated in < 30 seconds
- [ ] Passed/failed correctly identified
- [ ] Only passed concepts stored
- [ ] No memory issues
- [ ] RAG search finds all concepts

---

### Afternoon: Bug Fixes & Edge Cases (3 hours)

#### Common Integration Bugs

**Bug 1: Field Name Mismatch**
```python
# Research Portal sends:
{"conceptId": "test-001"}  # camelCase

# shared_models.py expects:
concept_id: str  # snake_case
```
**Fix:** Ensure all systems use exact field names from shared_models.py

---

**Bug 2: Missing Required Fields**
```python
# QuestionForge sends question without explanation
question = Question(
    question_id="q-001",
    # ... but missing 'explanation' if it's required
)
```
**Fix:** Check Pydantic Field() definitions for required vs optional

---

**Bug 3: Enum Value Mismatch**
```python
# System sends:
"difficulty": "easy"  # Wrong

# shared_models.py expects:
difficulty: Literal["beginner", "intermediate", "advanced"]
```
**Fix:** Use exact enum values from shared_models.py

---

**Bug 4: API Response Not Parsed**
```python
# System receives response but doesn't extract data
response = requests.post(...)
# Forgot to do: response.json()['data']
```
**Fix:** Always extract 'data' field from SuccessResponse

---

**Bug 5: Timeout Issues**
```python
# No timeout specified, hangs indefinitely
response = requests.post(url, json=data)

# Fix: Always use timeout
response = requests.post(url, json=data, timeout=30)
```

---

#### Edge Case Testing

**Edge Case 1: Empty Code Examples**
```python
concept = PythonConcept(
    # ...
    code_examples=[]  # Empty list
)
```
**Expected:** Validation error (min_items=2)
**Verify:** Quality Checker rejects

---

**Edge Case 2: Very Long Content**
```python
concept = PythonConcept(
    problem="x" * 10000  # 10,000 characters
)
```
**Expected:** Should handle gracefully (may have max length)
**Verify:** No crashes, reasonable validation time

---

**Edge Case 3: Special Characters**
```python
concept = PythonConcept(
    title="Variables & \"Special\" Chars'",
    code_examples=["x = 'It\\'s working'"]
)
```
**Expected:** Proper escaping, no parsing errors
**Verify:** Stored and retrieved correctly

---

**Edge Case 4: Concurrent Requests**
```python
# 10 concepts sent simultaneously to Quality Checker
import concurrent.futures
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(validate, concept) for concept in concepts]
```
**Expected:** All validated correctly, no race conditions
**Verify:** All responses correct, no errors

---

**Edge Case 5: Backend Restart**
```python
# AXIS AI has active connection
# Backend restarts
# AXIS AI retries request
```
**Expected:** Graceful failure, automatic retry
**Verify:** Error handling and recovery

---

### Evening: Performance Testing (2 hours)

#### Performance Targets

**Quality Checker:**
- Single validation: < 5 seconds
- Batch (50 items): < 30 seconds
- Throughput: 100 validations/minute

**Backend:**
- Single concept retrieval: < 200ms
- RAG search: < 500ms
- List concepts: < 300ms
- Throughput: 1000 requests/minute

**AXIS AI:**
- Full answer generation: < 3 seconds

#### Load Testing

**Test 1: Quality Checker Throughput**
```python
import time
import requests

concepts = [generate_test_concept() for _ in range(100)]
start = time.time()

for concept in concepts:
    response = requests.post(
        "http://localhost:8000/api/v1/content/validate",
        json=concept.dict()
    )

end = time.time()
print(f"100 validations in {end-start:.2f} seconds")
```

**Expected:** < 60 seconds (100/minute throughput)

---

**Test 2: Backend RAG Search Performance**
```python
queries = [
    "how to store data",
    "what are variables",
    "python data types",
    # ... 50 queries
]

start = time.time()
for query in queries:
    response = requests.get(
        f"http://localhost:9000/api/v1/content/search?q={query}"
    )
end = time.time()

print(f"50 searches in {end-start:.2f} seconds")
```

**Expected:** < 25 seconds (500ms per search)

---

**Test 3: Concurrent Users (AXIS AI)**
```python
import concurrent.futures

def simulate_user():
    # User asks question
    # AXIS searches Backend
    # AXIS retrieves concept
    # AXIS generates answer
    pass

with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    futures = [executor.submit(simulate_user) for _ in range(50)]
    results = [f.result() for f in futures]

print(f"{len(results)} concurrent users handled successfully")
```

**Expected:** All 50 users served, no crashes

---

## ✅ FINAL INTEGRATION VERIFICATION

### Pre-Launch Checklist

**All Systems:**
- [ ] All unit tests passing (>80% coverage)
- [ ] All integration tests passing
- [ ] All edge cases handled
- [ ] Performance targets met
- [ ] Error handling graceful
- [ ] Logs informative
- [ ] Documentation complete
- [ ] README setup instructions verified
- [ ] Environment variables documented
- [ ] Deployment tested (not just localhost)

**Data Quality:**
- [ ] No data loss through pipeline
- [ ] No data corruption
- [ ] Field names consistent
- [ ] Data types correct
- [ ] Enum values valid

**Security:**
- [ ] API keys not hardcoded
- [ ] Authentication working
- [ ] Rate limiting enforced
- [ ] Input validation present
- [ ] Error messages don't expose secrets

**Communication Flows:**
- [ ] Flow 1: Research Portal → Quality Checker → Backend ✓
- [ ] Flow 2: QuestionForge → Quality Checker → Backend ✓
- [ ] Flow 3: Backend → Quality Checker (batch) ✓
- [ ] Flow 4: AXIS AI → Backend (RAG) ✓

---

## 🐛 TROUBLESHOOTING GUIDE

### Debug Checklist

When integration fails:

1. **Check Logs**
   - Quality Checker logs
   - Backend logs
   - Research Portal logs
   - AXIS AI logs

2. **Verify Running**
   ```bash
   curl http://localhost:8000/health  # Quality Checker
   curl http://localhost:9000/health  # Backend
   ```

3. **Test in Isolation**
   - Can Quality Checker validate manually (Gradio)?
   - Can Backend store manually (direct DB)?
   - Can AXIS retrieve manually (CURL)?

4. **Check Data Format**
   ```python
   # Print exact JSON being sent
   import json
   print(json.dumps(concept.dict(), indent=2))

   # Compare with shared_models.py
   ```

5. **Verify Dependencies**
   ```bash
   pip list | grep pydantic  # Should be 2.x
   pip list | grep fastapi   # Should be 0.120.4
   ```

6. **Check Network**
   ```bash
   # Are systems reachable?
   ping localhost
   telnet localhost 8000
   telnet localhost 9000
   ```

---

## 📊 SUCCESS METRICS

### Integration Success = All of These

**Functional:**
- ✅ All 4 communication flows working
- ✅ Data formats 100% compatible
- ✅ Zero critical bugs
- ✅ Error handling graceful

**Performance:**
- ✅ Quality Checker: < 5s single, < 30s batch (50 items)
- ✅ Backend retrieval: < 200ms
- ✅ RAG search: < 500ms
- ✅ AXIS full answer: < 3s

**Quality:**
- ✅ Validation accuracy: 95%+ (matches human expert)
- ✅ False positives: < 5%
- ✅ False negatives: < 2%
- ✅ RAG relevance: Top 3 results contain answer 90%+ of time

**Reliability:**
- ✅ No crashes during load testing
- ✅ No data loss
- ✅ No race conditions
- ✅ Automatic recovery from transient failures

---

## 🎉 INTEGRATION COMPLETE

**When you can check all boxes above, integration is COMPLETE and The Zyric AI Ecosystem is ready for Phase 2: Building real features!**

**Estimated Time:**
- Day 6: 7 hours (2h individual + 3h first integration + 2h AXIS)
- Day 7: 8 hours (3h end-to-end + 3h bugs + 2h performance)
- **Total: 15 hours over 2 days**

**Contingency:** If integration takes longer, Day 7 can extend to Day 8. The critical milestone is "Integration working," not "Integration done by Day 7."

---

## 📚 APPENDIX: TESTING TEMPLATES

### Template 1: Manual Test Log

```markdown
## Test: [Test Name]
**Date:** YYYY-MM-DD
**System:** [System Name]
**Tester:** [Your Name]

### Test Steps:
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Expected Result:
[What should happen]

### Actual Result:
[What actually happened]

### Status:
[ ] PASS [ ] FAIL

### Notes:
[Any observations, issues, suggestions]
```

---

### Template 2: Integration Bug Report

```markdown
## Bug: [Short Description]
**Date:** YYYY-MM-DD
**Severity:** Critical / High / Medium / Low
**Systems Involved:** [System A] ↔ [System B]
**Status:** Open / In Progress / Fixed / Closed

### Description:
[Detailed description of the bug]

### Steps to Reproduce:
1. [Step 1]
2. [Step 2]
3. [Error occurs]

### Expected Behavior:
[What should happen]

### Actual Behavior:
[What actually happens]

### Error Message:
```
[Paste full error message and stack trace]
```

### Environment:
- OS: [Windows/Mac/Linux]
- Python: [Version]
- FastAPI: [Version]
- Pydantic: [Version]

### Proposed Fix:
[How to fix this]

### Fixed By:
[Name, Date]
```

---

### Template 3: Performance Test Result

```markdown
## Performance Test: [Test Name]
**Date:** YYYY-MM-DD
**System:** [System Name]

### Test Configuration:
- Requests: [Number]
- Concurrency: [Number]
- Data Size: [Size]

### Results:
| Metric | Target | Actual | Pass/Fail |
|--------|--------|--------|-----------|
| Avg Response Time | < Xs | Ys | ✅/❌ |
| P95 Response Time | < Xs | Ys | ✅/❌ |
| Throughput | > N req/s | M req/s | ✅/❌ |
| Error Rate | < X% | Y% | ✅/❌ |

### Bottlenecks:
[What's slowing things down]

### Recommendations:
[How to optimize]
```

---

**Document Version:** 1.0
**Last Updated:** 2025-11-06
**Status:** Ready for Days 6-7
