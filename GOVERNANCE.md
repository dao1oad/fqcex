# GOVERNANCE

## 1. Repository Model

- Repository: `dao1oad/fqcex`
- Visibility: `public`
- Default branch: `main`
- Governance model: single repository, phase-driven delivery

## 2. Project Roles

- `Product Owner`
  - owns scope, priorities, milestones, and acceptance
- `Architecture Owner`
  - owns architecture boundaries, ADRs, and freeze decisions
- `Runtime Owner`
  - owns venue runtimes and adapter integration
- `Risk and Ops Owner`
  - owns tradeability, runbooks, incident handling, and operator controls
- `Reviewer`
  - reviews changes before merge, especially around safety-critical behavior

Phase 1 may map multiple roles to the same person, but the responsibility split remains in force.

## 3. Decision Levels

- `Level 1: Product`
  - scope, phase boundaries, exchange expansion
- `Level 2: Architecture`
  - runtime choices, platform boundaries, state model, storage model
- `Level 3: Operating Policy`
  - thresholds, recovery rules, force-resume policy, incident handling
- `Level 4: Emergency Action`
  - `force_block`, `force_reduce_only`, `force_resume`, emergency recovery

## 4. Mandatory Documentation Rules

Changes must update the matching document set:

- architecture changes -> `docs/adr` and `docs/architecture`
- operating rule changes -> `docs/runbooks`
- scope or phase changes -> `docs/decisions/PHASE1_FREEZE.md` or roadmap docs
- roadmap changes -> `docs/roadmap/ROADMAP.md`

No change that affects tradeability, recovery, or risk should merge without documentation updates.

## 5. Branch and Pull Request Rules

- `main` is the only long-lived branch in Phase 1
- feature branches should use:
  - `feat/...`
  - `fix/...`
  - `docs/...`
  - `ops/...`
  - `adr/...`
- high-risk work should prefer `codex/...` or similarly isolated task branches
- direct pushes to `main` should be avoided except for repository bootstrap or emergency maintenance

Every PR that affects runtime, supervisor, recovery, data truth, or runbooks must include:

- purpose
- affected area
- risk
- verification
- documentation impact

## 6. Issue and Milestone Rules

- roadmap phases are managed through milestones:
  - `Phase 0` to `Phase 6`
- epics use normal GitHub issues with label `type/epic`
- tracking parent issues use label `type/tracking`
- child implementation issues use label `type/task`
- delivery issues must reference their parent epic in the body
- labels must identify both:
  - work type
  - area ownership
- work must follow the fixed hierarchy:
  - `Epic -> Tracking Parent Issue -> Child Implementation Issue`
- only `type/task` issues may be used as direct coding units
- `type/epic` and `type/tracking` issues are not direct coding entrypoints
- tracking parents close only after all child issues close
- epics close only after all tracking parents close
- the detailed issue tree and execution rules live in `docs/roadmap/ISSUE_HIERARCHY.md`

## 7. Subagent Execution Rules

- one subagent should own one `type/task` issue at a time
- if a task grows beyond its stated `Scope`, open a new sibling child issue instead of expanding the original issue
- PRs should reference the child issue they complete
- parent issue checklists must be updated as child issues close

## 8. Safety Rules

- public stream anomalies must be able to stop new opens
- private stream uncertainty must prevent returning to `LIVE`
- unexplained order, position, or balance truth must escalate to `BLOCKED` or remain `REDUCE_ONLY`
- `BLOCKED` requires explicit operator confirmation before resume
- manual actions must be auditable

## 9. Release Rules

- roadmap and governance docs may release independently from code
- before any small-size live dry run:
  - recovery runbooks must exist
  - tradeability rules must be documented
  - validation evidence must be recorded
- phase completion should be reflected with tags or milestone closure

## 10. Public Repository Rules

- never commit API keys, exchange secrets, account identifiers, or sensitive logs
- security-related disclosures should follow `SECURITY.md`
- issue reports that would leak sensitive trading details should use a private contact path instead of public issues
