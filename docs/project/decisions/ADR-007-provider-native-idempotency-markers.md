# ADR-007: Provider-native idempotency markers for exact read-back

- **Status:** proposed
- **Date:** 2026-11-09
- **Decision owner:** Maintainer (STK-001)
- **Related:** `FR-014`–`FR-016`, [ADR-001](ADR-001-adopt-craftrail-and-atep-blueprint-with-amendments.md) A2–A3

## Context and forces

Read-back must answer "did *this* action happen?", not "did something similar happen?". Matching on recipient + subject breaks when a user sends similar messages, and generic SMTP does not populate a Sent folder.

## Decision

Each connector embeds a marker derived from the idempotency key (`ik` = first 32 hex chars) and reads back by that marker:

| Capability | Marker | Read-back |
|---|---|---|
| SMTP send | `Message-ID: <ik@vouchor.local>` header | Mailpit API search (dev); IMAP `SEARCH HEADER Message-ID` on Sent after `APPEND` (generic providers) |
| Gmail send | Same `Message-ID` header in raw MIME | `users.messages.list q="rfc822msgid:<…>"` |
| Calendar event | Client-supplied event `id` (base32hex of `ik`) | `events.get(id)`; insert returns 409 on duplicate — itself idempotent |
| Keep note (API) | Label/metadata containing `ik` | `notes.list` filter |
| Keep note (browser) | `ik` suffix in note body footer (user-visible, configurable) | Tier 3 DOM search |
| Web form | Hidden field if available, else unique reference in message | Post-submit DOM / confirmation email |

Read-back polls with exponential backoff (1, 2, 4 s …) up to a per-capability grace window (default 30 s, Gmail 60 s) before returning "absent".

## Alternatives considered

- Subject/recipient match: not unique. Trusting the tool's response: violates invariant 5.

## Consequences

- Positive: exact matching, provider-side deduplication where supported (Calendar).
- Negative / risks: browser-tier markers may be visible to recipients — documented and configurable.

## Supersedes / superseded by

None.
