# Roadmap

The delivery plan is the [implementation plan](docs/project/implementation-plan.md) (phases P0–P7). This file tracks items outside those phases.

## Later (not committed)

- Minimal web UI for approvals (decision pending; see plan "Open decisions").
- Additional cloud cluster modules (GKE, AKS, DigitalOcean, bare-metal k3s).
- Firecracker-based sandbox backend.
- Additional connectors: Outlook/Microsoft Graph, CalDAV, Notion, Slack.
- Optional CLA for dual licensing (see [ADR-009](docs/project/decisions/ADR-009-license-agpl-3-0-or-later.md)).

## Open technical debt

- [ ] **TD-001 — Documentation hosting.** The docs site configuration (`vercel.json`) is inherited from the CraftRail template. Decide where the Vouchor docs site is hosted (any static host works) and update `zensical.toml` `site_url`.

Out of scope for v1: payments or financial actions, multi-tenant SaaS hosting, mobile apps.
