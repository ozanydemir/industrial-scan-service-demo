# Security and Public-Data Policy

Only synthetic records are allowed. Do not add employer, customer, employee, project, product,
barcode, database, endpoint, credential, image, report, or proprietary process information.

Connection strings and production adapters are intentionally absent. A real integration would need
environment-based secret management, access control, audit logging, and generic error responses.

## Reference-screen rule

Static interface references are permitted only after review. They must not expose customer,
employer, project, location, operator, component, barcode, report, endpoint, or other traceable
operational information. A timestamp associated with a real activity must be removed or replaced.
Any field that could identify a real activity must be replaced with clearly fictional public-demo
content before publication.
