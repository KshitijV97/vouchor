---
title: Vouchor — AI that does real work, and proves it
description: Self-hosted, open-source agent engine. Verified facts, one approval per batch, exactly-once actions, honest reports.
---

# Vouchor

## AI that does real work for you, and proves it.

Ask for something in plain words. Vouchor researches it, checks every fact at the source, and drafts every action. Then it waits for your **single approval**. It carries out the work by the most reliable route available and **proves each result** before calling it done.

!!! note "Project status"
    Vouchor is in the **design stage**. The architecture and plan are published. Features are marked *planned* until they ship.

---

## Built for the moments other agents get wrong

<div class="grid cards" markdown>

- **It doesn't trust stale search results**

    Search results are only hints. Vouchor reads the live page or API before using a fact, and keeps the evidence.

- **It asks once, at the right time**

    The research and drafting for a whole batch are done first. You review everything in one place, then approve, edit or reject each item.

- **It never sends twice**

    Every action carries a unique fingerprint. After a crash or timeout, Vouchor checks whether the action already happened before trying again.

- **"Done" means proven**

    A clicked button isn't proof. Vouchor confirms the result independently, for example by finding the email in your Sent folder or reading back the calendar event.

- **It always finds a way**

    Official API first, then a playbook, then a real browser. If all of those fail, you get a ready-to-use file. Every fallback is logged.

- **It remembers what matters**

    Your preferences and verified contacts are kept. Retry logs, drafts and page snapshots are not.

</div>

## What you'll use it for *(planned)*

| Ask Vouchor to… | It will… |
|---|---|
| "Email these seven vendors about part X" | Verify each vendor's real contact address, draft seven emails, ask you once, send, confirm every one was delivered |
| "What did the landlord say this week?" | Search and summarise your inbox. Reading doesn't need your approval. |
| "Book a call with Sam on Thursday at 3" | Create a Google Calendar event that can't be double-booked, even after a retry |
| "Add this recipe to my Keep" | Use Google's API where available, or a real browser if not, and check that the note exists |

Step-by-step walkthroughs are in the [Guide](guide/index.md).

## Self-hosted. Open source. Portable.

- **Runs on your laptop** with Docker, with no paid services required.
- **Uses local AI** through Ollama, or any OpenAI-compatible model you choose.
- **Deploys to any cloud** with the same Helm chart and open-source OpenTofu modules: a laptop cluster, a small VM or a large Kubernetes cluster.
- **AGPL-3.0 licensed:** free to use, study, change and self-host.

## Choose your path

| I want to… | Go to |
|---|---|
| Understand what Vouchor is | You're here |
| Set it up and use it | [Guide](guide/index.md) |
| Learn how it was built, from zero | [Build journal](build/index.md) |
| Read the requirements, architecture and decisions | [Engineering reference](project/README.md) |
