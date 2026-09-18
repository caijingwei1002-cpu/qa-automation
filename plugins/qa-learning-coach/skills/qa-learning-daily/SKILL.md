---
name: qa-learning-daily
description: Plan and review long-term QA automation learning work with one concrete daily output, using the local qa-automation-learning curriculum, progress.json, daily-log files, and project stages. Use when the user asks for today's testing-learning task, wants a daily automation script plan, needs a review of a completed study day, or wants to decide what to learn next across UI, API, performance, CI/CD, reliability, and security testing.
---

# QA Learning Daily

## Core rule

The learner requires the same seven-stage process every day. Stage IDs, titles, and ordering come from `config/learning-workflow.json`; teaching behavior and acceptance rules come from `docs/INTERACTIVE-LEARNING.md`. This skill applies to teaching, not requests to maintain or optimize the repository. Never advance learning progress during engineering maintenance.

Convert each study session into one small, verifiable learning output. The lesson contract declares whether that output is analysis, coding, debugging, or assessment; only coding lessons may require executable implementation. From Day 56 use flexible 120–150 minute sessions (baseline: discussion 30, learner practice 40, verification/debugging 25, review/revision 25, reflection 15). Split or extend sessions when needed. Read `ROADMAP.md`, `docs/INTERACTIVE-LEARNING.md`, and `docs/TEST-CODING-STANDARD.md` before teaching the revised curriculum. This is a rolling project curriculum: `core_days` is the detailed horizon, not the total program length. Do not fall back to archived lessons or ongoing tracks beyond it; perform the next project's deployment discovery and refine the plan first.

Do not give a large list of unrelated tutorials. Give one primary task, one optional stretch task, and a concrete definition of done.

## Workflow

1. Locate the repository. Prefer the path supplied by the user; otherwise use `qa-automation-learning` in the current workspace.
2. Before welcoming the learner, asking a diagnostic question, creating a log, modifying files, or running tests, perform a read-only progress preflight:
   - Read `progress.json` and identify `current_day`, `completed_days`, and the latest `history` entry.
   - If the learner names Day N, run `python tools/plan_day.py check-day N`. Treat `progress.json` as canonical; never accept the prompt's day number without this check.
   - If Day N differs from `current_day`, explain the mismatch and the requested day's status, then stop that day's teaching flow. Continue only with the canonical current day, or after the learner explicitly says this is a review/relearning session.
   - If no day is named, use `python tools/plan_day.py status` and read the current entry in `daily-plan.json`.
3. Cross-check the current plan against the latest `daily-log/day-*.md` and the relevant directory under `test-projects/`. If the target output already exists or the latest history says the day is complete, resolve the inconsistency before teaching.
   - Run `python tools/plan_day.py session N` to read the first unfinished stage and its next action. Resume there; do not restart a continued lesson. An existing output may be unfinished practice, not proof of completion.
4. Obtain the canonical task from the successful `check-day` output or `python tools/plan_day.py show N` (read-only). `today` and `plan N` create logs; use them only after preflight. Process logs may be updated during learning; knowledge writeback and progress advancement require explicit completion confirmation.
   - When `plan_day.py` emits a source-preparation reminder, tell the learner which project is next and inspect its disk, dependency, port, and version requirements. Obtain agreement before cloning; do not batch-download future projects.
5. Before implementation, ask two or three short pre-experiment questions tied to the day's learning focus, and wait for the learner's answers. Record the questions and the learner's answers or a clearly labeled retrospective reference answer; do not present a retrospective answer as an original conversation record.
   - Use the planned business scenario for role-play: requirements clarification, learner test design, learner coding, debugging, review and revision, then an unfamiliar transfer task.
   - Give progressively stronger hints (question, reasoning, partial example) and wait for actual learner responses. Do not write the learner's entire solution unless explicitly requested.
   - Record explained, practiced, independently completed, and accepted separately. Reference answers and assistant-written code do not demonstrate independence.
   - Use `templates/code-review.md`. Give file/line, impact, and a revision direction, then let the learner revise and re-review. Verify cleanup, xfail scope, and assertion quality as well as formatting.
   - Follow preflight → discussion → design → practice → verification → review → reflection. Save each actual result with `plan_day.py checkpoint N STAGE`. Use `--status in_progress` for unfinished work. From Day 77 record artifact type, learner/coach contributions, verification scope, and mastery level as required by the interactive protocol. The coach maintains checkpoints; do not burden the learner with JSON entry.
   - Record the learner's actual response and assistance level. A pasted reference implementation or coach fix is assisted work. In review, give a new transfer prompt and wait for a response without supplying the answer; record transfer assistance honestly. Do not fabricate missing historical checkpoints.
6. State the stage, project, objective, learning focus, today's single output, target file, expected command, evidence location, completion criteria, and optional stretch task.
7. Keep the task within the current test asset boundary. The external system under test is configured separately and must not be modified as part of a normal learning task. Advance from UI basics to UI framework design, API automation, performance, engineering, reliability, and security only when the earlier stage has evidence.
8. After the user reports results, classify learning progress, mastery, execution, environment, and product contract separately. A failed test with a documented root cause can be a valid learning output; a blind retry is not. Never treat `git diff --check`, a design matrix, or a Mock result as evidence for a different layer.
9. After explicit completion confirmation, record it in the reflection checkpoint, write the knowledge chapter with navigation/index and the daily log, then call `python tools/plan_day.py complete N --result "..." --next-step "..."`. From Day 67 the command requires all seven steps and structured execution evidence. Failures do not authorize editing progress directly. Run repository validation before staging only the day's files and creating a local commit. Do not push unless requested.
10. Every seventh learning day, include a short review of script count, failure patterns, concepts understood, and one skill to revisit. Every 28-day cycle, propose a harder constraint such as more data, parallelism, failure injection, observability, or CI quality gates.

## Preflight invariant

The first teaching response must be based on repository state, not on the day number written in the learner's prompt. A mismatch is a workflow result, not a minor warning: do not ask the requested day's diagnostic question until it is resolved. Preflight commands must be read-only so that checking progress cannot itself start or alter a learning day.

## Stage guidance

- TodoMVC: require a real UI assertion and a failure artifact before adding abstractions.
- SauceDemo: move repeated selectors and flows into Page Objects; keep business assertions in tests.
- Restful Booker: prefer API clients, fixtures, data isolation, authentication, schema checks, and cleanup over one-off requests.
- Swagger Petstore: use a local or explicitly authorized instance for load, stress, spike, and soak tests. Never load-test a public demo service.
- Engineering and advanced tracks: require reproducibility, logs, reports, CI evidence, and an explanation of tradeoffs.

## Output format

When planning a day, respond with:

```text
学习日：Day N
阶段/项目：...
实验前问答：...
今天要交付：...
建议步骤：...
运行命令：...
完成标准：...
证据目录：artifacts/day-NNN/
```

When reviewing a day, summarize the actual script, command, result, root cause if failed, evidence path, and the first action for the next day.

## Safety and scope

Keep performance work local or authorized. Avoid destructive data operations unless the project already has a deliberate test-data cleanup path. Do not treat screenshots or a green command with no assertions as sufficient evidence.

For the detailed project and extension map, read `qa-automation-learning/PLUGIN-AND-MCP.md` when a promotion or integration decision is needed.
