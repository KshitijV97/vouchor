# Agent compatibility

CraftRail separates its engineering process from the product used to assist with it. Requirements, plans, decisions, contracts, verification, and workflow prompts are files or ordinary instructions. Tool-specific files only tell an agent where to find shared context.

> **Compatibility is documented from official product guidance. Direct interactive testing is a separate claim.**

No direct end-to-end instruction-loading test has been run in Codex, Claude Code, or OpenCode as part of this repository draft. The matrix below describes supported/documented file discovery and labels verification honestly.

## Compatibility matrix

| Agent | Canonical shared instruction | Adapter/config in this repository | Documented behavior | Directly tested here |
|---|---|---|---|---|
| Codex | Root `AGENTS.md` | None required | Codex reads project `AGENTS.md`; nested guidance can narrow rules for a directory. | No |
| Claude Code | Root `AGENTS.md` | Root `CLAUDE.md` imports `@AGENTS.md` | Claude Code supports `@path` imports in `CLAUDE.md`; its current docs also describe when it reads `AGENTS.md` directly. | No |
| OpenCode | Root `AGENTS.md` | None required | OpenCode instruction discovery reads `AGENTS.md`; current docs explicitly say it does not use `CLAUDE.md` as fallback. | No |

| Shared behavior | State |
|---|---|
| Markdown specifications and neutral prompts can be read by each product | Documented compatibility; exact model adherence is not guaranteed |
| Optional skills, slash commands, hooks, MCP, or provider runtime | Not included or required; future adapters may add optional convenience |
| Directly tested instruction loading and cross-agent task outcome | Pending portability acceptance test |

Official sources, reviewed 2026-11-08: [Codex project instructions](https://developers.openai.com/codex/guides/agents-md/), [Claude Code memory and imports](https://docs.anthropic.com/en/docs/claude-code/memory), [OpenCode instructions](https://opencode.ai/docs/instructions/). These sources establish documented support; they do not prove this particular checkout was opened in each product.

## Why the file setup is intentionally asymmetric

`AGENTS.md` is the only shared policy file because maintaining three copies would create instruction drift. Codex and OpenCode consume this shared filename directly. Claude Code has its own project memory conventions, so `CLAUDE.md` contains an import pointer rather than another policy. OpenCode's docs explicitly distinguish its current instruction discovery from `CLAUDE.md`; creating a Claude file must not be mistaken for OpenCode compatibility.

If a future agent needs another filename or config, add a minimal adapter that refers to canonical docs. Document what that adapter can and cannot load. Do not store requirements in an agent-specific command file.

## Automatic use in Claude Code

The GitHub template already contains a root `CLAUDE.md` with `@AGENTS.md`. Claude Code automatically loads project `CLAUDE.md` files when a session starts in the project or one of its subdirectories. It expands `@AGENTS.md` into the same session context. The shared instructions state that CraftRail is the default for this repository, so the user does not need to paste a setup prompt, run `/init`, install a plugin, or invoke a slash command. Open the cloned/generated repository in Claude Code and describe the task normally.

Only the short shared instructions are loaded as always-on project context. Guides, requirements, feature specifications, plans, and ADRs are read when relevant, keeping token use lower than loading the entire documentation tree. This is documented behavior of Claude Code's project memory and import syntax; CraftRail's matrix still marks direct interactive testing as pending. This arrangement supplies context but cannot guarantee a model follows it.

The same no-extra-prompt principle applies to Codex and OpenCode: open the repository and let each product discover root `AGENTS.md` according to its documented behavior. For a meaningful task, the agent should select relevant project artifacts from the instructions. No setup ceremony is required after using the template.

## Use the same repository across agents

To verify compatibility, open the repository root in each product and ask the agent to:

1. Read `AGENTS.md` and summarize its relevant instructions.
2. Read the specific feature spec and the project's applicable requirements/accepted ADRs.
3. State the spec status and identify ambiguities before proposing implementation.
4. Work in approved scope, update ordinary repository files, run relevant checks, and report exact outcomes.

The user prompt can use ordinary language. The supplied [workflow prompts](workflow-prompts.md) are examples; none depend on a proprietary command, skill name, or tool invocation. Project knowledge remains in Git when switching agents.

## Portability acceptance test

Run this before claiming direct cross-agent verification:

1. Use the same commit or working tree in Codex, Claude Code, and OpenCode. Open each at the repository root.
2. Ask each to identify the same `AGENTS.md` policy, one requirement, one approved feature spec, and one applicable ADR. Do not ask it to edit yet.
3. Ask each to draft the same small documentation change with no code mutation. Compare whether they cite the same source and preserve the same intent.
4. After human approval, ask each to make the same small edit and run the same local validator. Review diffs and exact commands.
5. Record tool/version/date, instruction files actually loaded, observed differences, and failures. Do not convert a single successful session into a guarantee about future model behavior.

The test is intentionally about shared project knowledge and conventions, not identical prose or model output. If a product cannot load an adapter, update the adapter and record the limitation. Keep this result table honest:

| Agent | Version/date | Shared source loaded? | Same requirement/spec found? | Check outcome | Notes |
|---|---|---|---|---|---|
| Codex | pending | pending | pending | pending | Not run in this draft |
| Claude Code | pending | pending | pending | pending | Not run in this draft |
| OpenCode | pending | pending | pending | pending | Not run in this draft |

## Known limitations

- File discovery only supplies context; it cannot guarantee instruction adherence.
- Global user rules or nested project files can add instructions. Review the effective instruction chain when behavior differs.
- Large instruction files can be truncated or consume context. Keep root guidance concise and link to relevant docs.
- This project does not provide model-provider integrations, agents, skills, command files, or hooks.
- The portfolio test has not yet been run directly in the three products.
