# ADR-008: Pluggable Tier 4 sandbox isolation backends

- **Status:** proposed
- **Date:** 2026-11-09
- **Decision owner:** Maintainer (STK-001)
- **Related:** `FR-025`, `NFR-007`, [ADR-001](ADR-001-adopt-craftrail-and-atep-blueprint-with-amendments.md) A9

## Context and forces

Tier 4 runs generated scripts. Docker-in-Docker requires privileged containers, which in Kubernetes is a node-level escape risk.

## Decision

A `SandboxBackend` protocol with three implementations:

- `subprocess` (tests only): restricted subprocess in a temp dir; never enabled in deployed configs.
- `docker` (local Compose): talks to a **docker-socket-proxy** allowing only container create/start/wait/logs/remove; containers run with `--network none`, non-root, read-only rootfs, `--pids-limit`, CPU/memory limits, timeout, tmpfs workdir, artifacts mounted at `/workspace/artifacts`.
- `kubernetes` (cloud): creates a `Job` in a dedicated namespace with the same restrictions via Pod Security `restricted`, a deny-all `NetworkPolicy`, `activeDeadlineSeconds`, and optional `runtimeClassName: gvisor`.

Artifacts are copied to S3-compatible storage (MinIO/Garage locally if enabled) or a volume.

## Alternatives considered

- Firecracker microVMs: strongest isolation, but needs KVM on hosts; revisit later. E2B / hosted sandboxes: paid SaaS (`CON-001`).

## Consequences

- Positive: same contract locally and in cloud; no privileged containers.
- Negative / risks: socket proxy is still sensitive — bound to an internal network and only enabled in the `sandbox` profile.

## Supersedes / superseded by

None.
