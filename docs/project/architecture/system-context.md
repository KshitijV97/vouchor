# System context

**Status:** proposed
**Last reviewed:** 2026-11-09

```mermaid
C4Context
    title Vouchor system context
    Person(user, "User", "Requests work, approves batches")
    System(vouchor, "Vouchor", "Durable tiered execution engine")
    System_Ext(llm, "LLM endpoint", "Ollama locally, or any OpenAI-compatible API")
    System_Ext(google, "Google APIs", "Gmail, Calendar, Keep (Workspace)")
    System_Ext(mail, "SMTP / IMAP servers", "Any mail provider; Mailpit in dev")
    System_Ext(web, "Public websites", "Vendor pages, web forms")
    System_Ext(search, "Search engines", "Queried via self-hosted SearXNG")
    Rel(user, vouchor, "REST + SSE, approvals")
    Rel(vouchor, llm, "Intent parsing, drafting, distillation")
    Rel(vouchor, google, "Tier 1 connectors (OAuth)")
    Rel(vouchor, mail, "Tier 1 SMTP send, IMAP read-back")
    Rel(vouchor, web, "Tier 3 Playwright verification and forms")
    Rel(vouchor, search, "Discovery (untrusted)")
```

Everything inside the Vouchor boundary is self-hosted. External systems are reached only through MCP tool servers, so each can be faked in tests.
