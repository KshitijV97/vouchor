# ADR-009: License Vouchor under AGPL-3.0-or-later

- **Status:** proposed
- **Date:** 2026-11-09
- **Decision owner:** Maintainer (STK-001)
- **Related:** `CON-001`, `LICENSE`, `NOTICE`, `CONTRIBUTING.md`

## Context and forces

The owner wants a licence that protects their rights and is fair to users. Vouchor is a self-hostable network service. Under a permissive licence (MIT, Apache-2.0), a third party could take it, improve it privately, and sell it as a hosted service without giving anything back. Under source-available licences (BSL, SSPL, Elastic), it would stop being open source, which conflicts with the FOSS positioning (`CON-001`) and puts off contributors.

## Decision

- Code licence: **GNU Affero General Public License v3.0 or later** (SPDX `AGPL-3.0-or-later`).
  - Fair: anyone may use, study, modify and self-host it for any purpose, including commercially.
  - Protective: anyone who distributes a modified version, **or lets users interact with it over a network**, must offer the corresponding source under the same licence (section 13).
- Copyright and the trademark reservation for the "Vouchor" name are recorded in `NOTICE`.
- Contributions: inbound = outbound (AGPL), with a **Developer Certificate of Origin** sign-off (`git commit -s`). No CLA for now.
- Each source file gets the header `SPDX-License-Identifier: AGPL-3.0-or-later` (checked by a pre-commit hook added in P0).
- Dependency licences must be compatible with AGPL-3.0 (MIT, BSD, Apache-2.0, MPL-2.0, LGPL, GPL-3.0). The CI licence check from [ADR-002](ADR-002-python-toolchain-and-quality-gates.md) enforces this allow-list.

## Alternatives considered

- MIT / Apache-2.0: maximum adoption, but no protection against closed hosted forks.
- GPL-3.0: protects distributed copies but not network use (the "SaaS loophole").
- BSL / SSPL / Elastic License: not OSI open source; conflicts with `CON-001`.
- AGPL plus a CLA: would let the owner relicense later (for example, to sell commercial licences), but adds contributor friction. Can be adopted later for new contributions if the owner wants dual licensing.

## Consequences

- Positive: the owner's work cannot be turned into a closed competing service; the community gets improvements back.
- Negative / risks: some companies have policies against AGPL; without a CLA the owner cannot relicense code contributed by others. Not legal advice — the owner should get legal review before commercial use.

## Supersedes / superseded by

Supersedes the provisional MIT licence inherited from the CraftRail template.
