---
name: qa-learning-daily
description: Plan and review long-term QA automation learning work with one concrete daily output, using the local qa-automation-learning curriculum, progress.json, daily-log files, and project stages. Use when the user asks for today's testing-learning task, wants a daily automation script plan, needs a review of a completed study day, or wants to decide what to learn next across UI, API, performance, CI/CD, reliability, and security testing.
---

# QA Learning Daily

## Core rule

Convert each study session into one small, verifiable engineering change. The default session is 90 minutes: 10 minutes to understand the task, 50 minutes to implement one script or framework improvement, 20 minutes to run and capture evidence, and 10 minutes to record the result and next step.

Do not give a large list of unrelated tutorials. Give one primary task, one optional stretch task, and a concrete definition of done.

## Workflow

1. Locate the repository. Prefer the path supplied by the user; otherwise use `qa-automation-learning` in the current workspace.
2. Read `progress.json`, `daily-plan.json`, the latest `daily-log/day-*.md`, and the relevant project directory before proposing work. Use `curriculum.json` for stage-level context.
3. Use `python tools/plan_day.py today` or `python tools/plan_day.py plan N` to obtain the canonical task. The detailed plan is also readable in `DAILY-PLAN.md`. Do not invent a different stage unless the current task is blocked.
4. State the stage, project, objective, learning focus, today's single output, target file, expected command, evidence location, completion criteria, and optional stretch task.
5. Keep the task within the current project boundary. Advance from UI basics to UI framework design, API automation, performance, engineering, reliability, and security only when the earlier stage has evidence.
6. After the user reports results, classify the outcome as passed, failed-but-understood, or blocked. A failed test with a documented root cause is valid learning output; a blind retry is not.
7. Record the result with `python tools/plan_day.py complete N --result "..." --next-step "..."` only after confirming what actually happened.
8. Every seventh learning day, include a short review of script count, failure patterns, concepts understood, and one skill to revisit. Every 28-day cycle, propose a harder constraint such as more data, parallelism, failure injection, observability, or CI quality gates.

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
