# FinTrack API Standards

## Stack and framework
- Python 3.12+
- FastAPI for HTTP APIs
- SQLAlchemy + SQLite for persistence in local development
- Pydantic v2 for request/response validation
- Pytest for automated tests
- Structured logging via structlog or logging with JSON fields; never use print()

## Architecture conventions
- Follow a layered architecture: model -> repository -> service -> controller
- Keep each module focused on one responsibility and one domain
- Repositories handle persistence and data access only
- Services contain business rules and validation
- Controllers expose the API contract and delegate logic to services
- Do not mix persistence code into controllers or business services

## Code standards
- Use clear English names; prefer descriptive nouns and verbs
- Type hint every function argument and return value
- Prefer dataclasses or typed models for domain objects
- Keep functions short and single-purpose
- Add docstrings for public models, services, and controllers
- Use dependency injection for repositories and services where useful
- Use Pydantic schemas for all API IO boundaries
- Format with Ruff/Black-compatible style and 88-character lines

## Security rules
- Never use raw SQL strings for data access in app code
- Never hardcode secrets, API keys, tokens, or credentials
- Validate all user input at the boundary and verify business constraints inside services
- Enforce authorization checks on every action involving user-owned data
- Reject invalid amounts, blank descriptions, missing users, and malformed payloads early
- Treat all external input as untrusted; sanitize and normalize before persistence

## Testing expectations
- Use pytest and keep tests close to the module under test
- Prefer behavior-driven tests covering validation, success paths, and edge conditions
- Name tests with clear intent such as test_create_transaction_rejects_negative_amount
- Maintain minimum coverage for service logic and controller endpoints
- Add regression tests for any bugfix and for security/validation issues

## Logging standards
- Use structured logging only; include operation, user id, amount, and outcome when relevant
- Log validation failures and security denials with context, not stack traces only
- Never use print(), console.log(), or bare logger.debug without structured context

## Forbidden patterns
- Do not use raw SQL for primary business data access
- Do not bypass validation or trust client-supplied values blindly
- Do not commit secrets or local environment files
- Do not use mutable default arguments or broad exceptions for control flow
- Do not write "AI-generated without review" code into production without remediation
- Never leave TODOs or placeholder business logic in shipped code

## Review expectations
- Every generated module must be reviewed for validation, DB safety, and business correctness
- Prefer smaller, verifiable changes over large refactors with no test coverage
- If a model or service is AI-generated, confirm logic before it ships to development
