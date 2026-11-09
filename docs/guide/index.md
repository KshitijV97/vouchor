# Guide: use Vouchor

> **Tier 2 documentation.** Practical walkthroughs for running Vouchor and using it for real tasks. Every walkthrough will be backed by an automated end-to-end test so it stays correct. Pages are added as the phases in the [implementation plan](../project/implementation-plan.md) ship.

## How a request flows

1. You describe the task (API, CLI, or later a web UI).
2. Vouchor finds candidates and **verifies facts at the source**.
3. It **drafts every action** in the batch.
4. If any action acts in your name, it **pauses once** for your decision.
5. It executes through the most reliable route and **proves each result**.
6. You get a **plain report**. Lasting facts are remembered for next time.

## Walkthroughs

| Walkthrough | What you'll learn | Status |
|---|---|---|
| Install and run locally | Docker + uv, start the stack, pick an AI model | planned (Phase 0) |
| Your first request | Create a request, review the batch, approve, read the report | planned (Phase 1) |
| Connect your Google account | Create your own OAuth client and grant minimal permissions | planned (Phase 5) |
| Send an email with Gmail | Draft, approve, send, and see the delivery proof | planned (Phase 5) |
| Read and search your email | Summarise your inbox. Read-only, so no approval needed. | planned (Phase 5) |
| Schedule a Google Calendar event | Book events that can't be duplicated | planned (Phase 5) |
| Add a note to Google Keep | API route vs. browser fallback | planned (Phase 5) |
| Vendor outreach batch | Seven vendors, verified contacts, one approval | planned (Phase 5) |
| Approvals in depth | Approve, edit, reject; what happens when something fails | planned (Phase 1) |
| Deploy to the cloud | OpenTofu + Helm on kind or a cloud provider | planned (Phase 7) |
| Troubleshooting | Reading the ledger and route history | planned |

The full page list and delivery schedule are in the [documentation strategy](../project/documentation-strategy.md).
