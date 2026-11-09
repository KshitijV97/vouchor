# ADR-006: Portable deployment with OCI images, Helm, Kubernetes and OpenTofu

- **Status:** proposed
- **Date:** 2026-11-09
- **Decision owner:** Maintainer (STK-001)
- **Related:** `CON-001`, `CON-003`, `NFR-009`, [containers](../architecture/containers.md)

## Context and forces

The owner wants local execution and cloud deployment that is platform-agnostic, preferring FOSS infrastructure as code. Managed cloud services (RDS, ElastiCache, Cloud Run) would lock the system to one provider.

## Decision

Three layers, each portable:

1. **Images:** one multi-stage `Dockerfile` (uv, non-root, read-only rootfs) producing `vouchor` (api/worker/mcp entrypoints) and `vouchor-browser` (adds Chromium). Built for `linux/amd64` and `linux/arm64`, pushed to any OCI registry (GHCR by default), SBOM + Trivy scan, optional cosign signature.
2. **Runtime:**
   - Local: **Docker Compose** with profiles (`core`, `llm`, `observability`).
   - Anywhere else: **Kubernetes** via one **Helm chart** (`deploy/helm/vouchor`). In-cluster dependencies are FOSS operators/charts: **CloudNativePG** (Postgres + pgvector, backups to any S3-compatible store), Valkey, SearXNG, LiteLLM, optional Ollama. Ingress through the **Gateway API** (any conformant controller; Traefik ships with k3s). Secrets from **SOPS + age** or External Secrets Operator.
3. **Infrastructure:** **OpenTofu** (MPL-2.0).
   - `infra/modules/cluster-*`: thin provider modules that output a kubeconfig — `cluster-local-kind`, `cluster-hetzner-k3s`, `cluster-aws-eks`, more added on demand. This is the only provider-specific code.
   - `infra/modules/platform`: provider-agnostic; installs operators and the Vouchor chart through the Helm provider.
   - `infra/envs/{local,staging,prod}`: compose a cluster module with the platform module; state in any S3-compatible backend.
   - Single-VM option: `cluster-hetzner-k3s` (or any VM + k3s) keeps cost low while using the same chart.

CI deploys the chart to a **kind** cluster on every PR (`ct install`) so the cloud path is tested locally and continuously.

## Alternatives considered

- Terraform: BSL licence. Pulumi: FOSS engine but general-purpose code increases review surface. Nomad: BSL. Compose-on-VM only: simplest but no HA, no rolling upgrades, and a second deployment model to maintain. Crossplane: heavier control plane than needed.

## Consequences

- Positive: one chart for every environment; switching providers changes only the cluster module.
- Negative / risks: Kubernetes complexity for small installs — mitigated by k3s single-node and the documented Compose path for personal use.

## Supersedes / superseded by

None.
