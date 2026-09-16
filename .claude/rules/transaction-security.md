# Transaction security rules

- Validate every amount as a positive decimal number.
- Reject blank user IDs and descriptions.
- Use service-layer validation before CRUD operations.
- Log suspicious bulk delete operations for audit review.
- Do not accept untrusted values from API clients without schema checks.
