# Stakeholders and personas

| ID / role | Goals | Constraints / needs | Decision or consultation role |
|---|---|---|---|
| STK-001 Owner / maintainer | Ship a trustworthy, self-hostable agent platform | Limited time; wants agent-assisted development with strong guardrails | Approves specs, ADRs, releases |
| STK-002 Self-hosting end user | Delegate email, calendar, notes and outreach chores | Must stay in control of anything sent in their name; no paid SaaS | Approves every consequential batch |
| STK-003 Integrator / capability author | Add new connectors, skills and playbooks | Needs stable contracts and a test harness | Consulted on registry and MCP contracts |
| STK-004 Operator | Run Vouchor on a VM or Kubernetes cluster | Needs reproducible IaC, backups, observability | Consulted on deployment design |
| STK-005 Learning engineer | Understand how such a system is built from zero | Needs the build journal (Tier 3 docs) | Reader; feedback via issues |

## Personas / user groups

- **Priya, freelance consultant (STK-002):** wants "email these seven vendors and put the calls on my calendar" done in one go, reviewed once.
- **Sam, platform engineer (STK-004):** wants `tofu apply` to produce a working deployment on their provider of choice.

Personas are illustrative and not yet validated with real users.
