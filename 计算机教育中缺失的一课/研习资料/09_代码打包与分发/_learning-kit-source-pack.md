# 09 代码打包与分发 - source pack

## Source Snapshot

- Course root: `30_研究/计算机教育中缺失的一课/研习资料/`
- Unit page: `09_代码打包与分发/学习页.html`
- Local course index snapshot: 2026-06-21
- Existing unit draft snapshot: 2026-06-09

## Source Boundary

This unit is grounded in:

1. The course index entry for `09_代码打包与分发`.
   - Unit role: stage 4, delivery and collaboration.
   - Adjacent units: 08 establishes Git history and recovery; 10-12 continue into agent programming, engineering collaboration, and automated quality checks.
   - Learner promise: hand code to other people or systems as a reproducible runnable artifact, not as an unexplained folder.

2. The existing old study page for this unit.
   - Core terms: dependency, transitive dependency, runtime, artifact, lockfile, image/container.
   - Main flow: source code -> dependency declaration -> resolution/locking -> build artifact -> clean installation -> runtime verification.
   - Existing examples: `pyproject.toml`, optional development dependencies, CLI entry point, Dockerfile, wheel build, clean environment install.
   - Existing failure modes: `ModuleNotFoundError`, version conflict, hidden global install, missing data files, missing entry command, secret baked into image.

3. The broader public topic of code packaging and distribution, expressed in ecosystem-neutral terms.
   - Python packaging examples use `pyproject.toml`, wheel artifacts, CLI entry points, virtual environments, and `uv` commands because this workspace uses `uv`.
   - Container examples stay at the image/container/runtime-configuration boundary and avoid provider-specific deployment claims.

## Source To Unit Notes

- The lesson should start from the concrete failure "it runs on my machine but not elsewhere" and turn hidden local assumptions into explicit project metadata.
- Keep the anchor example as a small Python CLI package named `hello-tool`.
- Show the same package moving through metadata, dependency declaration, build artifact, clean install, entry command, and container boundary.
- Use a trace table or state ledger for the central handoff: what each file or command reads, writes, and what symptom appears when it is wrong.
- Practice should test conceptual distinctions, command/config reading, failure diagnosis, and transfer to a README/release checklist.

## Required Teaching Boundaries

- This page covers packaging and distribution concepts at the project level: dependencies, environments, artifacts, lockfiles, entry points, and container boundaries.
- It does not teach full package publishing, CI/CD, supply-chain signing, private registries, SBOM generation, or production orchestration. Those can be follow-up topics after the learner can produce and verify a local artifact.
- Do not imply containers solve secrets, external databases, CPU architecture, networking, data volumes, or host kernel compatibility.

## Acceptance Notes

- The finished page should use the shared `study-page-v2` runtime assets.
- It should include a working practice export, objective checks, open-question rubrics, at least one state/data-flow tracer, a terminal-style failure lab, and several exportable review contexts.
- Learner-facing Chinese should stay concrete and technical; protect commands, file names, package names, and error messages during prose cleanup.
