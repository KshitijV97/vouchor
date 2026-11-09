# Engineering principles

> Status: proposed. Inherited from CraftRail and extended for Vouchor.

1. **Human intent before generated code.** Approved requirements define intended behavior; agents may propose, not silently approve, changes.
2. **Specifications before implementation.** Resolve material ambiguity and agree on acceptance criteria before substantial implementation.
3. **Architecture before uncontrolled complexity.** Respect documented boundaries and record consequential decisions.
4. **Verification before completion.** Link evidence to acceptance criteria; report exact checks and limitations.
5. **Documentation evolves with code.** Converge specs, contracts, diagrams, and decisions when approved behavior changes.
6. **Replaceable tools.** Canonical engineering knowledge uses portable formats; provider integrations remain optional.

7. **Prove side effects.** No action is reported done without independent read-back evidence.
8. **Local first, portable always.** Everything runs and is tested on a laptop; deployment artefacts work on any conformant Kubernetes.

Document exceptions with rationale and an owner.
