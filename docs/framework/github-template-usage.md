# Use CraftRail as a GitHub template

GitHub template mode is enabled for [`kshitijv97/craft-rail`](https://github.com/kshitijv97/craft-rail). Open the repository and choose **Use this template** → **Create a new repository**. This copies the starter files into a new repository without retaining the upstream repository's commit history. A clone or fork is a different choice: use those when you want history or a continuing relationship with the upstream project.

In the new repository, update project brief, principles, stakeholders, glossary, requirements, architecture, and contract examples. Remove irrelevant starter content, keep or revise the shared `AGENTS.md`, and review the license and brand decisions. Create a first feature with `python3 scripts/new_feature.py "Feature title"`. Run the validator and unit tests, then commit the customized baseline. See [quickstart](quickstart.md).

## Start using CraftRail with Claude Code

No setup prompt is required after creating the repository from this template. Root `CLAUDE.md` imports the concise shared `AGENTS.md`; Claude Code reads project instructions when you open the project. The shared instructions tell Claude to use CraftRail by default, select only the relevant project requirements and feature records, scale the workflow to the task, and verify its changes. Start Claude Code in the project directory (or open that directory in its editor integration) and describe the work normally.

This keeps the always-loaded context small: the shared instructions are brief, while guides and specifications are read only when relevant. You do not need to paste the same framework prompt into each conversation, run Claude's `/init`, install a CraftRail plugin, or maintain a second copy of the policy. As documented in the [compatibility guide](agent-compatibility.md), automatic instruction discovery is based on Claude Code's documented behavior; CraftRail has not yet recorded a direct interactive compatibility test.

The GitHub template setting belongs to the upstream repository's GitHub settings, not this source tree. A local checkout cannot make the **Use this template** button appear by adding a file. An owner or maintainer with repository administration rights must enable the setting and then verify it on the repository page. The CraftRail repository was checked through GitHub's API after enabling the setting. For another repository, do not claim template status until that state is verified.
