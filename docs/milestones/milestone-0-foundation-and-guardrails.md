# Milestone 0: Foundation and Guardrails

- Status: Complete
- Roadmap source: [docs/roadmap.md](../roadmap.md)
- Primary architecture reference: [docs/PAG-mini-v0.6.md](../PAG-mini-v0.6.md)

## Milestone Intent

Milestone 0 establishes the project operating system: architecture constraints, development standards, and reproducible setup rules. The output of this milestone is not gameplay functionality. The output is a stable foundation that prevents rework in later milestones.

## What Will Be Accomplished

By the end of Milestone 0, the project will have:
- A documented architecture contract that defines layer boundaries and ownership.
- A documented dependency direction policy that prevents cross-layer leakage.
- A locked baseline for Python version, dependency pinning, and local development workflow.
- A documented quality gate policy for formatting, linting, type checks, and tests.
- A practical, reproducible setup/run/test section in [README.md](../../README.md).
- A milestone acceptance checklist that must be passed before Milestone 1 begins.

## In Scope

- Clarify and document architecture constraints from PAG.
- Define import and dependency rules for domain, controller, and GUI layers.
- Define initial standards for code quality and test expectations.
- Define repository conventions for folder naming and module ownership.
- Define how external dependencies are introduced and pinned.
- Document setup and verification commands in README.

## Out of Scope

- Implementing game logic.
- Building UI functionality.
- Implementing session persistence.
- Writing production feature code beyond lightweight project scaffolding needed for validation.

## Detailed Work Packages

## WP0.1: Architecture Contract

Goal:
- Convert architecture statements in PAG into explicit development constraints.

Tasks:
- Define the authoritative rule: game rules live in crapssim only.
- Define layer contract:
  - GUI renders state and forwards user intent.
  - SessionController bridges Qt to session model.
  - GameSession owns session state and orchestration.
  - crapssim owns game rules and bet resolution.
- Define prohibited behaviors:
  - No Qt imports in domain/session modules.
  - No game-rule duplication in controller or GUI.
- Define source of truth precedence:
  - PAG architecture constraints override convenience implementation shortcuts.

Deliverable:
- Written architecture contract section in repository docs.

## WP0.2: Dependency Direction and Boundaries

Goal:
- Prevent architecture drift before code growth begins.

Tasks:
- Define allowed dependencies:
  - GUI -> controller
  - controller -> session
  - session -> crapssim
- Define forbidden dependencies:
  - GUI -> session direct mutation paths.
  - session -> GUI or Qt dependencies.
- Define module ownership guidance:
  - Domain dataclasses and state models under session.
  - Qt signal and slot wiring under controller.
  - Visual components and interaction under gui.

Deliverable:
- Boundary policy documented with examples of allowed and forbidden imports.

## WP0.3: Toolchain and Environment Baseline

Goal:
- Ensure every contributor can produce the same local behavior.

Tasks:
- Select required Python version for the project.
- Define virtual environment workflow.
- Define dependency install workflow for runtime and dev dependencies.
- Define pinning strategy for PySide6 and crapssim.
- Define command set for setup, lint, type-check, and tests.

Deliverable:
- Setup and command conventions written in README.

## WP0.4: Quality Gates

Goal:
- Establish minimum quality standards before feature implementation starts.

Tasks:
- Define formatting standard and command.
- Define lint policy and failure thresholds.
- Define type-check policy scope.
- Define test policy for milestone progression:
  - New domain behavior requires tests.
  - Regressions must be covered before merge.
- Define CI intent for later automation.

Deliverable:
- Written quality gate policy and pass criteria.

## WP0.5: Milestone Handoff Preparation

Goal:
- Ensure Milestone 1 starts with zero ambiguity.

Tasks:
- Publish a concise list of required packages/modules for Milestone 1 skeleton.
- Confirm naming conventions for files and packages.
- Confirm acceptance checklist for Milestone 0 completion.

Deliverable:
- Milestone 0 signoff checklist with explicit pass conditions.

## Deliverables Summary

Milestone 0 is complete only when all items exist and are reviewable:
- Architecture contract document section.
- Dependency boundary policy with allowed/forbidden examples.
- Toolchain baseline and reproducible local setup documentation.
- Quality gate policy and expected commands.
- Milestone 1 readiness handoff checklist.

## Acceptance Criteria

All criteria must be true:
- Architecture constraints are documented and reflect PAG.
- Dependency direction is explicit and unambiguous.
- Development setup instructions are reproducible on a clean machine.
- Quality gate commands are defined and produce expected results.
- Team can state what is out of scope for Milestone 0 without ambiguity.

## Verification Checklist

Reviewer checklist:
- [x] Architecture sections align with [docs/PAG-mini-v0.6.md](../PAG-mini-v0.6.md).
- [x] No milestone content introduces gameplay implementation requirements.
- [x] README contains setup and validation commands for local workflow.
- [x] Boundary rules explicitly prevent Qt usage in domain modules.
- [x] Quality gate definitions are practical and enforceable.

## Risks and Mitigations

Risk: Architecture policy is too abstract.
- Mitigation: Add concrete allowed/forbidden dependency examples.

Risk: Tooling policy is too strict too early.
- Mitigation: Keep minimum viable gates now, tighten in later milestones.

Risk: Setup drift across machines.
- Mitigation: Require explicit versions and deterministic install steps.

## Milestone 0 Exit Decision

**Decision: Pass.** All acceptance criteria are satisfied; work may proceed to Milestone 1.

## Signoff Evidence

- Signoff date: 2026-07-29.
- Environment: macOS with Python 3.14.6 in a fresh project virtual environment.
- Clean setup evidence: a separate temporary virtual environment installed `requirements-dev.txt`
  from scratch and passed `python tools/check.py`.
- Engine source: local sibling checkout at commit
  `56e26a8794a63bb5ec4a4e7efcca727b0febf7d2`.
- Engine source lifecycle: the sibling checkout remains in use while Bubble Craps v0.1.0 is
  completed; the release candidate will switch to published crapssim v0.5.0 before Bubble Craps
  v0.1.0 is released.
- Architecture and dependency policy: [docs/architecture-contract.md](../architecture-contract.md).
- Toolchain, quality, and handoff policy: [docs/development.md](../development.md).
- Milestone 1 handoff: package layout and module ownership are reconciled with the accepted
  architecture contract.
- Setup and command workflow: [README.md](../../README.md).
- Automated evidence: architecture direction, documentation links, check-runner behavior, engine
  revision cleanliness, and Crapless API tests.
- Gate result: Ruff format passed, Ruff lint passed, strict first-party mypy passed, 11 pytest tests
  passed, and `pip check` reported no broken requirements.
