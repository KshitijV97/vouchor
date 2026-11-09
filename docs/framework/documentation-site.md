# Documentation website

The website is a rendered view of the canonical Markdown in `docs/`. It is not a new source of engineering requirements, and it does not contain copied pages that can drift from repository policy.

## Why Zensical

We selected Zensical as a static documentation generator because it reads the repository's existing Markdown and TOML navigation configuration, renders Mermaid diagrams, includes search/theme behavior, and emits ordinary static files. That output can be served by a CDN without a runtime service, database, or server-side application. It keeps authoring in Markdown and the development tools in Python; no project JavaScript framework is required.

This is a deliberate tradeoff. Zensical 0.1.0 was released as a beta on 2026-11-05, so its configuration and build behavior are less mature than an established generator. Material for MkDocs, the mature alternative from the same team, is in maintenance mode and has an announced end-of-life date of 2027-05-05. We pin Zensical to 0.1.0 and keep content in standard Markdown so the project can migrate if the beta proves unsuitable. Re-evaluate the pin before release and periodically thereafter.

Official references, reviewed 2026-11-08: [Zensical installation](https://zensical.org/docs/), [configuration](https://zensical.org/docs/setup/basics/), [Mermaid support](https://zensical.org/docs/authoring/diagrams/), [build command](https://zensical.org/docs/usage/build/), and [Material for MkDocs lifecycle notice](https://squidfunk.github.io/mkdocs-material/changelog/).

## Why the site configuration is at repository root

`zensical.toml` and `vercel.json` live at the root because the docs site reads `docs/` and related source content across the repository. Setting Vercel's project root to a nested `website/` directory would prevent the build from reading those sibling Markdown files. This is a repository-root build, with `site/` as generated output.

The navigation is explicit. That adds a small maintenance cost when a page is added, but it gives developers a deliberate learning order and avoids exposing starter registers, internal decision notes, the implementation brief, or templates as primary website navigation. Pages can still be linked directly where useful.

## Local setup and preview

Python 3.11 or newer is required by the pinned Zensical package. Use an isolated virtual environment so documentation tooling does not alter the Python environment used by CraftRail's standard-library scripts:

```bash
python3 -m venv .venv-docs
source .venv-docs/bin/activate
python -m pip install -r requirements-docs.txt
zensical serve
```

Open the local address printed by Zensical (default `http://localhost:8000`). The server watches the Markdown source so edits appear as you work. To produce the deployable files locally:

```bash
zensical build --clean --strict
```

The generated `site/` directory is ignored by Git. Commit source Markdown, `zensical.toml`, the pinned requirements file, and Vercel configuration; do not commit generated HTML as a second source of truth.

## Vercel build design

`vercel.json` selects the static/Other preset (`framework: null`), installs the pinned Python documentation dependency as part of the build command, runs a strict clean build, and publishes only `site/` as the output directory. There are no functions, secrets, API calls, or per-request computation. Vercel documents `buildCommand`, `outputDirectory`, and the `null` framework preset for this type of custom static build in its [project configuration reference](https://vercel.com/docs/project-configuration/vercel-json).

The deployed project is named `craft-rail-docs` and builds from the repository root. Its generated site is published at [craft-rail-docs.vercel.app](https://craft-rail-docs.vercel.app). GitHub integration could not be connected to the owner's repository from the current Vercel account, so this deployment was created through the CLI. Vercel will not automatically rebuild on GitHub pushes until that integration is connected.

## How to update the site

The source of every page is committed under `docs/`. To change existing guidance, edit its Markdown file; to add a page, create a Markdown file and add it to the explicit `nav` list in `zensical.toml`. Images and CSS live in `docs/images/` and `docs/stylesheets/`. Do not edit `site/`: it is generated output and ignored by Git. The site is a rendered view of the canonical repository documentation, so those source files remain usable without Vercel.

For a local preview, install the pinned site tool in an isolated environment and run `zensical serve` as described above. Before publishing, run `zensical build --clean --strict`; this catches missing navigation pages and other build issues. GitHub Actions runs the Python tests and quality checks and builds the site on pushes and pull requests. It does **not deploy** the site to Vercel.

This Vercel project is currently CLI-driven. Since the repository is not connected to Vercel through GitHub, pushing a commit does not update the website. After reviewing a change, use the authenticated Vercel CLI from the repository root:

```bash
npx vercel link                 # once per local checkout; select craft-rail-docs
npx vercel deploy               # create a preview deployment
npx vercel deploy --prod        # publish to the production alias
```

Review the preview URL before deploying production. On a new machine, authenticate the CLI and link the checkout to the existing project; do not create a second project by accident. If the owner later connects the GitHub repository in Vercel, pushes can create automatic deployments. Verify production-branch and build settings in Vercel because those are account configuration, not controlled by this repository. See Vercel's [CLI deployment guide](https://vercel.com/docs/projects/deploy-from-cli). `zensical.toml` records the verified canonical URL so generated pages include correct metadata and canonical links.

Vercel's build uses a virtual environment because its Python installation is externally managed. This avoids modifying system packages and keeps the site generator isolated. Only the generated static `site/` directory is served; the site has no CraftRail runtime server, database, or request-time application logic. The Vercel CLI is needed only by maintainers who deploy, not by readers or projects adopting the framework.

## Current deployment status

The documentation site is deployed to production at [craft-rail-docs.vercel.app](https://craft-rail-docs.vercel.app). The `craft-rail-docs` Vercel project currently belongs to the `golden-tide-retreat` scope as a temporary arrangement. This creates an ownership and continuity dependency on an unrelated scope; it is tracked as `TD-001` in the repository-root `ROADMAP.md`. Vercel deployment protection is still enabled, so visitors may need to authenticate with Vercel to view it. The project owner must adjust Deployment Protection in Vercel settings to make the site readable to everyone. A GitHub automatic deployment connection remains unavailable, so subsequent Vercel deployments require the CLI unless the owner connects the repository in Vercel.
