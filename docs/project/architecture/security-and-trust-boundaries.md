# Security and trust boundaries

**Status:** proposed
**Last reviewed:** 2026-11-09

| Boundary | Threat | Control | Requirement |
|---|---|---|---|
| Web content → LLM | Prompt injection from pages, emails, search results | Content treated as data; never changes capability selection or consequence level; consequential actions always gated | `BR-001`, `FR-005` |
| LLM → tools | Model proposes unapproved side effect | Tools classified in registry, not by the model; executor refuses actions without an `APPROVED` ledger row whose payload hash matches | `BR-002` |
| Tier 4 sandbox | Escape, exfiltration, crypto-mining | No network by default, non-root, read-only rootfs, seccomp, CPU/memory/time limits, optional gVisor | `FR-025`, [ADR-008](../decisions/ADR-008-tier4-sandbox-isolation-backends.md) |
| Credentials | Token theft | Only the `mcp-connectors` container holds provider tokens; encrypted at rest; least-privilege OAuth scopes | `BR-006`, `NFR-007` |
| API clients | Unauthorized approval | Authenticated API; approvals bound to thread owner | `FR-026` |
| Supply chain | Malicious dependency/image | Lockfile, pinned image digests, Trivy, SBOM (Syft), gitleaks, Dependabot/Renovate | `NFR-007`, `NFR-012` |
| Memory store | Sensitive data retained | Distiller allow-list of categories; no bodies/credentials | `BR-004` |
