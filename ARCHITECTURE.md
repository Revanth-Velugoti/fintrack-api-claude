# Architecture Overview

The Transaction and Expense Splitting modules work together as two linked domains in the same fintech API: transactions record user-level financial movements, while shared expenses produce settlement obligations between participants. 
The application uses a layered pattern: model -> repository -> service -> controller, which keeps domain logic separate from persistence and HTTP concerns. 
Requests enter the controller, which validates input through schema models and delegates to the service layer. 
The service calls repository methods for database access, preserving a clean boundary between business rules and data persistence. 
This structure is appropriate for fintech because it reduces the chance of invalid financial data reaching the database and makes auditing easier. 
The expense splitter calculates net balances and supports both equal and custom share models, making settlement logic explicit and reviewable. 
Key design decisions include typed domain models, strict validation for amount and participant data, and pytest-driven regression protection. 
The transaction layer is intentionally simple and reusable so it can be used by other downstream services without duplication. 
This approach keeps the codebase easier to review, safer to extend, and better aligned with production engineering standards.
