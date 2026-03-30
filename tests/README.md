# Tests Documentation

This directory contains the test suite for the `python-sbb-polarion` package.

## Test Structure

```
tests/
├── README.md                           # This file
├── unit/                              # Unit tests
│   └── extensions/
│       └── test_*.py                  # Individual extension tests
├── verification/                       # API verification tests
│   ├── test_github.py                 # GitHub-based OpenAPI verification
│   └── test_polarion_live.py          # Live Polarion API verification
└── integration/                       # Integration tests (future)
```

---

## Extension API Verification Tests

### Overview

The `tests/verification/` module automatically verifies that Python extension clients correctly implement their corresponding upstream REST APIs by comparing against OpenAPI specifications.

**Purpose:**
- Ensure Python methods match upstream REST API endpoints
- Catch missing endpoint implementations
- Alert when upstream APIs change
- Document API coverage

### OpenAPI Spec Sources

The verification tests use a hybrid approach:

**1. GitHub** (PRIMARY - WORKING):
- URL: `https://raw.githubusercontent.com/SchweizerischeBundesbahnen/ch.sbb.polarion.extension.{name}/main/docs/openapi.json`
- Source: OpenAPI specs from **source code** repositories
- All extensions accessible
- Fast and reliable (0.89s per test)

**2. Polarion Deployed Extensions** (FUTURE - NOT YET IMPLEMENTED):
- URL: `https://polarion.example.com/polarion/{extension-name}/rest/api/openapi.json`
- Source: OpenAPI specs from **deployed** Polarion extensions (production reality)
- When available, will become primary source
- Requires: `POLARION_TOKEN` and `POLARION_URL` environment variables

### Authentication Setup

**Option 1 (Recommended): Use .env file**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your tokens
# POLARION_URL=https://polarion.example.com
# POLARION_TOKEN=your-polarion-token-here
# GITHUB_TOKEN=your-github-token-here

# Tokens are auto-loaded when tests run
uv run tox -e verify-openapi-mapping
```

**Option 2: Use GitHub CLI (auto-detected)**
```bash
# Authenticate with GitHub CLI (one-time setup)
gh auth login

# Token will be automatically detected via 'gh auth token'
uv run tox -e verify-openapi-mapping
```

**Option 3: Export environment variables**
```bash
# For Polarion (future - not yet implemented)
export POLARION_URL="https://polarion.example.com"
export POLARION_TOKEN="your-polarion-token"

# For GitHub (current working source)
export GITHUB_TOKEN="ghp_your_github_token"

uv run tox -e verify-openapi-mapping
```

**Token Setup:**

1. **GitHub Personal Access Token:**
   - Go to: https://github.com/settings/tokens
   - Generate new token with `repo` scope
   - Copy the token

2. **Polarion Token** (future):
   - When Polarion endpoints are implemented
   - Will use existing Jenkins credential: `POLARION-system-test-token`

**Security Note:** Never commit tokens to version control! The `.env` file is git-ignored.

### Running Tests

**Recommended: Use dedicated tox environment (local/manual only):**
```bash
# Option 1: With .env file (auto-loaded)
uv run tox -e verify-openapi-mapping

# Option 2: With GitHub CLI (auto-detected)
gh auth login
uv run tox -e verify-openapi-mapping

# Option 3: With manual environment variables
export GITHUB_TOKEN="ghp_..."
uv run tox -e verify-openapi-mapping
```

**Direct execution:**
```bash
uv run python -m tests.verification
```

**Note:** The API verification tests are:
- Located in `tests/verification/` (separate from unit tests)
- Included in standard `uv run tox` test suite
- Can also run separately via `uv run tox -e verify-openapi-mapping`

**Run single extension verification:**
```bash
uv run python -m tests.verification.ExtensionAPIVerificationTest.test_pdf_exporter_completeness
```

**Disable parameter validation (method names only):**
```bash
VALIDATE_PARAMETERS=false uv run tox -e verify-openapi-mapping
```

### What the Tests Validate

The verification tests perform **annotation-based API compatibility checking**:

**Method Matching (via `@restapi_endpoint` annotations):**
- ✅ Uses explicit `@restapi_endpoint` decorator annotations for matching
- ✅ No heuristic name guessing - exact `method + path` matching
- ✅ Validates annotated methods against OpenAPI specification
- ✅ Reports missing annotations for endpoints not yet implemented
- ✅ Reports annotation issues (path/parameter mismatches)
- ✅ Detects orphan annotations (method annotated but endpoint not in OpenAPI)
- ✅ Detects duplicate annotations (multiple methods for same endpoint)

**Parameter Validation (Automatic via annotations):**
- ✅ Validates path parameters match OpenAPI spec
- ✅ Validates query parameters match OpenAPI spec
- ✅ Validates request body parameters
- ✅ Reports mismatched parameter names or missing params

**Implementation Validation:**
- ✅ Validates `api_request_*` call matches annotated HTTP method (e.g., `@restapi_endpoint(method="GET")` must use `api_request_get()`)

**Method Naming Validation:**
- ✅ Methods must start with a verb (get, create, save, delete, etc.)
- ✅ HTTP method correspondence (GET → get_, POST → create_/save_, etc.)
- ✅ Plural/singular consistency (list endpoints → plural method names)
- ✅ Path keywords should appear in method name
- ✅ No double underscores or mixed camelCase/snake_case
- ✅ Use `naming_ok=True` in decorator to suppress suggestions for intentionally non-standard names

**Annotation Example:**
```python
from python_sbb_polarion.core.annotations import restapi_endpoint

@restapi_endpoint(
    method="GET",
    path="/api/projects/{projectId}/documents/{documentId}",
    path_params={"projectId": "project_id", "documentId": "document_id"},
    query_params={"revision": "revision"},
)
def get_document(self, project_id: str, document_id: str, revision: str | None = None) -> Response:
    ...
```

**Benefits of annotation-based matching:**
- Explicit mapping - no ambiguity in method-to-endpoint correspondence
- Self-documenting code - annotations show API contract
- Precise validation - catches real issues, no false positives

### Understanding Test Results

**✅ Test Passed:**
```
test_pdf_exporter_completeness ... ok

====================================================================================================
OpenAPI Verification Report: pdf_exporter
====================================================================================================

{
  "extension": "pdf_exporter",
  "repository": "ch.sbb.polarion.extension.pdf-exporter",
  "openapi_spec_url": "https://github.com/...",
  "summary": {
    "total_openapi_endpoints": 41,
    "missing_annotations": 0,
    "annotation_issues": 0,
    "implemented_methods": 41,
    "annotated_methods": 41
  },
  "missing_annotations": [],
  "annotation_issues": [],
  "implemented_methods": ["convert_to_pdf", "get_context", "get_version", ...]
}

====================================================================================================

OpenAPI verification passed for pdf_exporter (41 endpoints verified via annotations)
```
All REST API endpoints have corresponding Python methods with `@restapi_endpoint` annotations.

**❌ Test Failed (Missing Annotations):**
```
{
  "summary": {
    "total_openapi_endpoints": 41,
    "missing_annotations": 3,
    "annotation_issues": 0,
    "implemented_methods": 38,
    "annotated_methods": 38
  },
  "missing_annotations": [
    {
      "http_method": "POST",
      "path": "/api/convert/html",
      "operation_id": "convertHtmlToPdf",
      "openapi_params": {
        "path_params": [],
        "query_params": ["orientation", "paperSize"],
        "required_params": []
      }
    }
  ]
}

FAIL: pdf_exporter: Found 3 issues (3 missing annotations, 0 annotation issues)
```

**❌ Test Failed (Annotation Issues):**
```
{
  "annotation_issues": [
    {
      "method_name": "get_document",
      "http_method": "GET",
      "path": "/api/projects/{projectId}/documents/{documentId}",
      "issues": ["Missing path parameter mapping: documentId"]
    }
  ]
}
```

**Action Required:**
1. **Missing annotations** - Add `@restapi_endpoint` decorator to method
2. **Annotation issues** - Fix parameter mappings in decorator
3. Update Python extension client with correct annotations

**JSON Format Benefits:**
- Machine-readable for automation
- Complete parameter information from OpenAPI spec
- Can be fed directly to AI models for implementation assistance

**⏭ Test Skipped:**
```
test_admin_utility_completeness ... skipped 'No OpenAPI spec found'
```

**Common skip reasons:**
- No OpenAPI spec in repository (`docs/openapi.json` missing)
- Network error (GitHub unreachable)
- Missing authentication token

### Configuration

**Skip specific extensions:**

Edit `tests/verification/test_github.py`:
```python
SKIP_EXTENSIONS = ["test_data", "requirements_inspector"]  # Extensions to skip
```

**Adjust timeouts:**
```python
REQUEST_TIMEOUT = 10  # seconds for HTTP requests
```

### Interpreting Results

**"Missing Annotations" Can Be Legitimate:**

1. **Base class methods** - Already handled by `PolarionGenericExtensionApi`:
   - `get_context()`, `get_version()` - inherited with annotations

2. **Intentionally not implemented** - Endpoint not needed in Python client:
   - Some admin/internal endpoints
   - Deprecated endpoints

**When to Act:**
- Core functionality endpoints missing annotation
- Newly added endpoints in upstream API
- Annotation issues reported (parameter mismatches)

**When Not to Act:**
- Base class methods (already annotated in parent class)
- Documented intentional omissions

### Annotation Validation

The `@restapi_endpoint` decorator provides explicit mapping between Python methods and OpenAPI endpoints:

**Decorator Parameters:**
```python
@restapi_endpoint(
    method="POST",                                    # HTTP method
    path="/api/projects/{projectId}/export",          # API path with placeholders
    path_params={"projectId": "project_id"},          # OpenAPI → Python mapping
    query_params={"format": "format", "scope": "scope"},
    body_param="export_params",                       # Request body parameter
    helper_params=["file_path"],                      # Python-only params (not in API)
    required_params=["projectId"],                    # Required OpenAPI params
    response_type="binary",                           # Expected response type
    naming_ok=True,                                   # Suppress naming suggestions
)
```

**Suppressing Naming Suggestions:**

When a method name intentionally doesn't follow naming conventions (e.g., matching external API terminology), use `naming_ok=True`:

```python
@restapi_endpoint(
    method="GET",
    path="/api/opentext/api/v1/nodes/{nodeId}/output",
    path_params={"nodeId": "nodeId"},
    naming_ok=True,  # Method name matches external API terminology
)
def run_web_report(self, node_id: str) -> Response:
    """Run a WebReport - name intentionally matches OpenText API."""
    ...
```

**Common Annotation Issues:**

1. **Missing path parameter mapping:**
   ```
   issues: ["Missing path parameter mapping: documentId"]
   ```
   **Fix:** Add to `path_params`: `path_params={"documentId": "document_id"}`

2. **Missing query parameter mapping:**
   ```
   issues: ["Missing query parameter mapping: revision"]
   ```
   **Fix:** Add to `query_params`: `query_params={"revision": "revision"}`

3. **Path mismatch:**
   ```
   issues: ["Path mismatch: expected /api/jobs/{id}, got /api/jobs/{jobId}"]
   ```
   **Fix:** Update path to match OpenAPI spec exactly

4. **HTTP method implementation mismatch:**
   ```
   issues: ["HTTP method implementation mismatch: annotation declares GET, but method body calls api_request_post()"]
   ```
   **Fix:** Ensure the `api_request_*` call matches the annotated HTTP method

### Using JSON Output for AI-Assisted Development

The verification tests output structured JSON reports that can be used with AI models to automatically implement missing endpoints.

**Extract JSON report:**
```bash
# Run test and capture output
uv run python -m unittest tests.verification.test_github.ExtensionAPIVerificationTest.test_pdf_exporter_completeness -v 2>&1 > report.txt

# Extract JSON (between the separator lines)
grep -A 1000 "OpenAPI Verification Report" report.txt > pdf_exporter_report.json
```

**Feed to AI model (Claude, ChatGPT, etc.):**
```
Prompt: "Based on this OpenAPI verification report, implement the missing methods for the pdf_exporter extension. Use the parameter information to create correct method signatures."

[Paste JSON report]
```

**JSON includes everything needed for implementation:**
- HTTP method (GET, POST, PUT, DELETE)
- Endpoint path with parameters
- Suggested Python method name (snake_case converted)
- Operation ID from OpenAPI spec
- Complete parameter list (path, query, body)
- Required vs optional parameters
- Body schema structure

**Example AI prompt:**
```
I have an OpenAPI verification report showing 16 missing methods in my pdf_exporter.py Python client.
Please implement these methods based on the JSON specification below. Follow the existing code style
in the file and ensure proper error handling.

[Paste the JSON "missing_methods" array]
```

### CI/CD Integration

The API verification tests are included in the standard `tox` test suite and run automatically as part of CI/CD pipelines.

```yaml
- name: Run All Tests (including API verification)
  run: |
    export GITHUB_TOKEN=${{ secrets.GITHUB_TOKEN }}
    uv run tox
```

### Troubleshooting

**Problem:** Tests fail with "Could not fetch OpenAPI spec"

**Solutions:**
- Check network connectivity to GitHub/Bitbucket
- Verify authentication tokens are set correctly
- Check token has required permissions
- Try accessing the URL manually in a browser

**Problem:** Test reports many missing methods

**Solution:**
- Review the OpenAPI spec in the repository
- Determine which methods are legitimately missing
- Add missing methods or document why they're omitted
- Consider adding to `SKIP_EXTENSIONS` if extension is incomplete

### Development Workflow

**When adding a new extension:**

1. Add extension to `EXTENSION_MAPPING` in test file
2. Run verification test to see current status
4. Implement missing critical methods
5. Document any intentional omissions

**When upstream API changes:**

1. Tests will fail showing new/removed endpoints
2. Review changes in upstream repository
3. Update Python client accordingly
4. Update tests if endpoint mapping changes

### Implemented Features

- [x] **Annotation-based matching** - Explicit `@restapi_endpoint` decorators for method-endpoint mapping
- [x] **Parameter validation** - Validates annotations against OpenAPI specifications
- [x] **Implementation validation** - Validates `api_request_*` calls match annotated HTTP method
- [x] **Method naming validation** - Verbs, HTTP correspondence, plural consistency
- [x] **Orphan annotation detection** - Methods annotated but not in OpenAPI spec
- [x] **Duplicate annotation detection** - Multiple methods for same endpoint
- [x] **JSON report generation** - Structured JSON output for AI-assisted development
- [x] **100% API coverage** - 252 annotated methods across all extensions
- [x] **100% test coverage** - All extension methods covered by unit tests

### Planned Improvements

- [ ] Type annotation validation (validate Python type hints against OpenAPI schemas)
- [ ] Return type validation (verify return types match OpenAPI responses)
- [ ] Generate test stubs from OpenAPI specs
- [ ] Auto-generate missing method implementations via AI integration
- [ ] GitHub Actions workflow for scheduled checks
- [ ] Pre-commit hook for extension changes
- [ ] Monitoring for upstream API changes with notifications

---

## Writing New Tests

### Unit Test Guidelines

**Location:** `tests/unit/<module_name>/test_<feature>.py`

**Structure:**
```python
import unittest
from python_sbb_polarion.module import Class

class TestFeature(unittest.TestCase):
    """Test feature X"""

    def setUp(self):
        """Set up test fixtures"""
        pass

    def test_specific_behavior(self):
        """Test that specific behavior works correctly"""
        # Arrange
        input_data = ...

        # Act
        result = some_function(input_data)

        # Assert
        self.assertEqual(result, expected)
```

**Naming:**
- Test classes: `TestFeatureName`
- Test methods: `test_specific_behavior`
- Use descriptive names that explain what is being tested

**Best Practices:**
- One assertion per test (when possible)
- Test one behavior per test method
- Use setUp/tearDown for common setup
- Mock external dependencies
- Test both success and failure cases

### Running Tests

**All tests:**
```bash
uv run pytest
```

**Specific test file:**
```bash
uv run pytest tests/unit/extensions/test_pdf_exporter.py
```

**Specific test method:**
```bash
uv run pytest tests/unit/extensions/test_pdf_exporter.py::TestPdfExporter::test_convert
```

**With coverage:**
```bash
uv run coverage run --source=python_sbb_polarion --branch -m pytest .
uv run coverage report -m
```

---

## Test Coverage

**Current Target:** 95% code coverage (actual: 100%)

**Check coverage:**
```bash
uv run coverage run --source=python_sbb_polarion --branch -m pytest .
uv run coverage report -m
uv run coverage html  # Generate HTML report
```

**Coverage report location:** `htmlcov/index.html`

---

## Questions or Issues?

- Review test output for detailed error messages
- Consult the OpenAPI specs in upstream repositories
- Contact the team for access to private repositories
