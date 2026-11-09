# Business rules and constraints

| ID | Type (`BR` or `CON`) | Rule / boundary | Source / rationale | Verification / owner | Status |
|---|---|---|---|---|---|
| BR-001 | BR | Any action that mutates external state, acts in the user's name, or may incur financial or reputational cost MUST be classified `CONSEQUENTIAL` and MUST NOT execute without explicit human approval. | Invariant 4 | Registry validation + gate tests / Owner | proposed |
| BR-002 | BR | An approved action MUST execute with exactly the payload the user approved; any change after approval requires a new approval. | Invariant 4 | Payload hash check in executor / Owner | proposed |
| BR-003 | BR | The system MUST NOT report an action as done unless read-back verified it. | Invariant 5 | Reporter tests / Owner | proposed |
| BR-004 | BR | Durable memory MUST NOT store drafts, DOM state, retry logs, credentials, or message bodies. | Invariant 6; privacy | Distiller tests / Owner | proposed |
| BR-005 | BR | Vouchor v1 MUST NOT perform payments, purchases, trades or fund transfers. | Risk boundary | Capability allow-list / Owner | proposed |
| BR-006 | BR | Reading user data (email, calendar, notes) is `READ_ONLY` but MUST be limited to the scopes the user granted and never forwarded to third parties without a consequential approval. | Privacy | OAuth scope tests / Owner | proposed |
| CON-001 | CON | All runtime and development dependencies MUST be free and open-source; no paid SaaS is required to run or test the system. | Original blueprint §1.2 (commit `ac5b91d`); owner preference | Dependency licence check in CI / Owner | proposed |
| CON-002 | CON | Python 3.12+, async-native code; no blocking I/O inside async nodes. | Original blueprint §3.2 (commit `ac5b91d`) | Ruff `ASYNC` rules + review | proposed |
| CON-003 | CON | Deployment artefacts MUST be platform-agnostic: OCI images, Helm chart, OpenTofu. Provider-specific code is limited to thin OpenTofu cluster modules. | Owner requirement | Review; [ADR-006](../decisions/ADR-006-portable-deployment-kubernetes-helm-opentofu.md) | proposed |
| CON-004 | CON | Default LLM endpoint is local (Ollama via LiteLLM); any OpenAI-compatible endpoint MAY be configured. | Original blueprint §3.2 (commit `ac5b91d`) | Config tests | proposed |
