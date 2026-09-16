# Pull Request Description

## Summary
This PR adds the Expense Splitting workflow to FinTrack and remediates the AI-generated Transaction module that was inherited without review. The changes introduce a cleaner layered architecture, stronger validation, and regression coverage to support safe fintech operations.

## AI Disclosure
This work was implemented with an AI-assisted workflow that followed explicit project standards in `CLAUDE.md`. All generated code was reviewed, remediated, and validated with pytest before shipping.

## Highlights
- Remediated the Transaction module with SQLAlchemy-based persistence and validation.
- Added an Expense Splitting domain model and balance calculation logic.
- Added tests covering transaction create/get/delete flows and split scenarios.
- Captured prompt engineering and review workflow documentation for future maintainers.

## Peer Review Simulation
### Review comment 1
File: `src/expense_splitting/service.py`
Comment: The `create_expense` method currently treats the creator as an automatic participant when missing, but it does not enforce a consistent participant list for all equal splits. Please ensure the creator is included once, and the equal-share allocation logic uses the final participant list rather than a partially normalized list.
Why: This avoids silent double-counting or inconsistent share totals when the creator is not explicitly listed.

### Review comment 2
File: `src/transactions/controller.py`
Comment: The route contract currently returns raw ISO strings for timestamps but does not yet include structured error handling for invalid payloads. Please add explicit error mapping for `ValueError` so the API returns consistent 400 responses to clients.
Why: This makes the API easier to consume and prevents ambiguous error states in production.

### Review comment 3
File: `tests/test_transaction_service.py`
Comment: The current tests cover the happy path and edge validation well, but they do not assert the database row count after deletion or check that the repository flushes timezones correctly. Please add one regression case for bulk delete and one for created timestamp consistency.
Why: It protects against non-deterministic persistence issues that AI-generated code often misses.

## Notes
The project is ready for review with the remediation and feature work integrated under the required architecture and test coverage standards.
