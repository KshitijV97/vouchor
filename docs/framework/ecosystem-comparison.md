# Ecosystem comparison

**Last reviewed: 2026-11-08.** This is a practical comparison of published project documentation, not a ranking. Links point to canonical project sources; capabilities may change.

| Approach | Purpose/workflow | Agent compatibility | Artifacts and adoption | What it adds / tradeoff |
|---|---|---|---|---|
| CraftRail | Repository conventions spanning project intent and feature lifecycle; docs + small validator | Neutral files and ordinary prompts; no interactive agent test claimed | Markdown/Mermaid/YAML/JSON; template or incremental copy | Supplies a coherent baseline teams would otherwise assemble. Deliberately little automation. |
| [GitHub Spec Kit](https://github.com/github/spec-kit) | Toolkit for spec-driven development; documented flow includes specify, clarify, plan, tasks, analyze, implement, converge | Many agent integrations and optional generated commands; see current project docs | CLI initialization, templates, commands/skills, Markdown artifacts | Choose when you want an installed, more automated feature workflow and generated agent-specific commands. More setup/configuration. |
| [OpenSpec](https://openspec.dev/) / [repository](https://github.com/Fission-AI/OpenSpec) | Spec-driven changes with explore/propose/apply/archive style workflow | Project documents many coding-assistant integrations; use its current docs for exact setup | CLI/configuration and Markdown change/spec artifacts | Choose when a purpose-built change lifecycle and CLI are desired. Introduces its own workflow/tooling. |
| Plain Markdown + `AGENTS.md` | Ad hoc repository documentation and local agent guidance | Depends on each agent's instruction-file support; shared Markdown is broadly portable | No prescribed layout or validation | Maximum freedom and minimum framework opinion; teams assemble conventions and checks themselves. |

## Interoperability answers

CraftRail contributes templates, stable IDs, architecture/ADR practices, a verified example, and offline checks. It does not attempt to replace Spec Kit or OpenSpec's command-driven feature orchestration. It can coexist with either if owners are explicit: for example, keep project requirements and ADRs canonical in CraftRail and link a feature proposal to the orchestration tool's working artifacts, then converge approved outcomes back to one canonical record. Do not keep duplicated competing requirements.

Canonical records are reviewed Markdown, Mermaid source, YAML/JSON contracts, and decisions in the project's chosen location. Agent-specific commands/configuration and rendered diagrams are adapters or generated artifacts. CraftRail intentionally does not automate approvals, semantic analysis, code generation, or diagram rendering.

Sources: [Spec Kit repository](https://github.com/github/spec-kit), [Spec Kit docs](https://github.com/github/spec-kit/tree/main/docs), [OpenSpec site](https://openspec.dev/), [OpenSpec repository](https://github.com/Fission-AI/OpenSpec). Capabilities were reviewed against official docs on the date above; no claim is made about their internal agent execution being tested by CraftRail.
