# Prompt Engineering Documentation

## Prompt Chain

### 1. Project standards and architecture setup
Prompt text:
"Create a production-ready Python FastAPI project for a fintech API. Add CLAUDE.md with the stack, architecture layers, coding standards, security rules, logging requirements, and testing expectations. Also add a README.md and a lightweight requirements.txt, plus .claude/rules/transaction-security.md for transaction-specific controls."

Claude Code feature used: Interactive terminal prompt with project-root context and file creation
Prompting techniques: role-based, specificity, constraints
Rationale: I first set guardrails for all future generations so the code would align with the architecture and security requirements before implementing business logic.

### 2. Generate the unreviewed Transaction module (as instructed)
Prompt text:
"Generate a Transaction model and a Transaction service with create, get-by-user, and delete-all functions. Use a database."

Claude Code feature used: Direct file generation in the working directory
Prompting techniques: low specificity, direct generation, minimal constraints
Rationale: This reproduces the unreviewed AI-generated code scenario described by the assignment so the later review and remediation step is realistic.

### 3. Refactor the Transaction module for production readiness
Prompt text:
"Review the generated transaction module and rewrite it to production standards. Use a layered architecture: model -> repository -> service -> controller. Add validation, SQLAlchemy persistence, and clean naming. Keep the API contract explicit and do not add raw SQL."

Claude Code feature used: @ file references for the existing model/service files
Prompting techniques: decomposition, constraint, role-based
Rationale: The task was broken into domain layers so the generated code would be fixed in the right shape instead of patched ad hoc.

### 4. Build the expense-splitting feature
Prompt text:
"Create a SharedExpense model and a BalanceCalculationService that supports equal and custom splits. Include validation for total amount matching, participant counts, and balances owed/owed-by. Keep the business logic separate from API controllers and add a clean controller contract."

Claude Code feature used: /plan mode for architecture review and implementation planning
Prompting techniques: decomposition, few-shot structure, constraints
Rationale: The feature involved multiple domain rules and edge cases; planning first reduced the chance of incorrect or incomplete logic.

### 5. Add and verify tests
Prompt text:
"Write pytest tests for the transaction service and expense-splitting business logic. Cover positive and negative paths, validation errors, equal splits, custom splits, and net balance calculations. Run the tests and fix any failing cases."

Claude Code feature used: Terminal-driven verification + iterative refinement
Prompting techniques: iterative refinement, specificity, validation-first
Rationale: The best way to reduce AI drift is to put the logic under test and fix only the cases the tests reveal.

## Context Window Management
- I used /compact after the initial scaffolding to reduce token load after the project standards and transaction rewrite were in place.
- I used /clear when switching from transaction remediation to expense-splitting implementation so new prompts would not inherit stale model state.
- I kept prompts focused and explicit to avoid large unexplained code generation in one turn.

## Post-Generation Corrections
- Issue: The first generated Transaction module used a raw SQLite connection in the service layer. Fix: replaced it with `TransactionRepository` and SQLAlchemy-backed model objects.
- Issue: Invalid amounts and blank user IDs were accepted. Fix: added explicit guards in `TransactionService.create_transaction` and tests to lock the behavior in.
- Issue: The first expense-splitting logic incorrectly accepted mismatched custom split totals and did not separate allocation logic cleanly. Fix: tightened `_validate_custom_amounts` and restructured the service to keep validation and balance calculation explicit.
- Issue: The generated controller exposure was too static and did not follow a layered contract. Fix: reworked the controller to rely on service methods and typed request/response models.
- Issue: The environment initially used Python 3.14 with pinned dependencies that were incompatible with Pydantic. Fix: verified the project under Python 3.12 and installed the project in a compatible virtual environment before running pytest.

## Implementation Note
This prompt chain was intentionally designed to follow the project standards in `CLAUDE.md`, using plan mode and constrained generation to keep the code review and remediation aligned with the fintech architecture and security requirements.
