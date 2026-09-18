# QA Automation Learning Lab

这是一个长期维护的个人 QA 自动化学习仓库，保存自己的测试代码、测试配置、学习记录、运行证据和工程化文档。

## 仓库边界

当前 Git 仓库只保存测试资产，不保存第三方被测项目源码：

```text
D:\
├── qa-automation-learning             # 当前 Git 仓库
│   ├── test-projects                   # 自己编写的自动化测试工程
│   │   ├── 01-todomvc-ui
│   │   ├── 02-saucedemo-ui
│   │   ├── 03-restful-booker-api
│   │   └── 04-booker-platform
│   ├── config                          # 目标登记和可提交配置
│   ├── daily-log                       # 每日学习记录
│   ├── artifacts                       # 精选测试证据
│   ├── tools                           # 学习计划和辅助工具
│   └── plugins                         # 本地学习插件
│
└── qa-automation-targets              # 第三方被测项目，不属于当前 Git 仓库
    ├── todomvc
    ├── restful-booker
    └── restful-booker-platform
```

`test-projects/` 只保留已进入实际课程的项目，并按学习顺序连续编号。完整顺序、状态、目录和学习日范围见自动生成的[测试项目索引](test-projects/README.md)。Petstore 等待勘察项目仅保留在路线图中。被测项目的来源、路径、URL 和安全边界统一登记在 [config/targets.json](config/targets.json) 和 [TARGETS-SETUP.md](TARGETS-SETUP.md) 中。

## 项目入口

当前项目是 `04-booker-platform`，Petstore 将作为 `05-petstore-performance` 在完成部署勘察后创建。项目编号以 [config/project-roadmap.json](config/project-roadmap.json) 为唯一配置，由计划生成器同步到[项目索引](test-projects/README.md)。

公共网站只做轻量功能验证；压力、峰值、稳定性和容量测试只对本地或明确授权的环境执行。

## 初始化和运行

首次使用时，先复制环境模板并按实际端口修改：

```powershell
Copy-Item .env.example .env
```

再按 [GIT-WORKFLOW.md](GIT-WORKFLOW.md) 连接自己的远程仓库，并按 [TARGETS-SETUP.md](TARGETS-SETUP.md) 准备本地被测项目。

新版总路线见 [ROADMAP.md](ROADMAP.md)，交互规则见 [docs/INTERACTIVE-LEARNING.md](docs/INTERACTIVE-LEARNING.md)，编码规范见 [docs/TEST-CODING-STANDARD.md](docs/TEST-CODING-STANDARD.md)。计划生成源为 `config/project-lessons.json` 与 `tools/build_daily_plan.py`；Booker Platform 正在学习，其余后续项目登记在 `config/project-roadmap.json`，部署后再细化课程。

查看学习计划：

```powershell
python tools/plan_day.py today
python tools/plan_day.py plan 37
python tools/plan_day.py status
python tools/validate_repo.py
```

## 开课前进度自检

每日流程统一为七步：开课核对与复习 → 场景与需求讨论 → 测试设计 → 实践与实现 → 验证与排错 → 审查与独立迁移 → 复盘与收尾。名称和顺序由 `config/learning-workflow.json` 管理；基础步骤记录从 Day 67 起生效，课型与能力证据规则从 Day 77 起生效，详细操作见 [交互协议](docs/INTERACTIVE-LEARNING.md)。

教练负责保存步骤记录；学习者可以继续直接说“开始 Day N”“继续学习”“帮我修改”。协助实现如实记录，测试通过与独立掌握分别验收。

```powershell
python tools/plan_day.py show 67
python tools/plan_day.py session 67
```

两条命令都只读。session 显示首个未完成步骤和上次下一动作；同一课可跨会话完成，工作台点击步骤不会更新验收状态。

当学习请求中写明 `Day N` 时，先执行只读校验，再开始讲解、提问或修改文件：

```powershell
python tools/plan_day.py check-day N
```

校验以 `progress.json` 的 `current_day` 为准。如果请求日与当前学习日不一致，先说明请求日是已完成、遗漏还是尚未到达；除非学习者明确要求复习或重学，否则不进入该日教学。`today` 和 `plan N` 命令都会生成对应日志和证据目录，因此不能用于开课前的只读自检，只应在学习日确认后使用。

从 Day 48 开始，正式验证证据统一保存为 `artifacts/day-XXX/verification.md`。使用以下命令执行当天计划中的目标测试和项目全量回归；命令会优先使用仓库 `.venv`，并把真实结果自动写入标准证据文件：

```powershell
python tools/run_day_verification.py 48
```

`verification.md` 是正式总结证据，其他 `.txt` 文件只能作为可选原始输出。完成学习日时，`plan_day.py complete` 会校验证据文件、目标测试、全量回归、关键验证和环境结论；证据不完整时不会推进 `progress.json`。

新验证同时保存 `run-record.json` 和 `runs/<run-id>/result.json`，包含执行项目、命令、退出码、时间、来源及测试代码指纹。工作台和 MCP 使用相同执行入口。更改测试代码或重新执行验证后，需要重新检查对应验收记录。
学习者提供的终端结果可由教练按 [运行记录说明](docs/VERIFICATION-RECORDS.md) 整理后导入，来源固定记为 learner。
完成命令从 Day 67 起还检查七步证据、独立迁移和明确确认，以及知识章节和日志；重复完成不追加历史，越级完成会被拒绝。

工程工具验证（不启动被测服务）：

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest tools -q
python -m unittest discover -s workbench/tests -v
python tools/validate_repo.py
```

完成一个学习日并记录实际结果：

```powershell
python tools/plan_day.py complete 1 `
  --result "完成新增 Todo 测试并记录运行证据" `
  --next-step "增加完成状态场景"
```

当前使用项目驱动的滚动计划：Day 1–55 保留，当前细化范围由 `daily-plan.json` 和 `config/project-roadmap.json` 共同校验；当前 Booker Platform 与后续 Petstore、Medusa、Saleor、Juice Shop 和毕业项目见 `ROADMAP.md`。每课建议 120–150 分钟，可延长或拆分，包含讨论、学习者实践、验证排错、审查和独立迁移。`core_days` 表示已细化范围，不是整个路线长度。`daily-plan.json`、`DAILY-PLAN.md` 和 `test-projects/README.md` 是生成结果，不应手工维护其中的索引内容。

## 每日完成标准

每个学习日至少留下：

1. 一条能用自己的话解释的知识重点；
2. 一个与课型和知识重点直接对应的产出；编码课必须是可运行测试脚本或工程改动；
3. 一次真实执行结果，失败时记录根因或阻塞条件；
4. 一份学习记录、知识验收和证据路径；
5. 一份可脱离代码文件复习的 LEARNING-NOTES.md 知识章节；
6. 一次有意义的本地 Git 提交，或明确记录本日未创建提交。

学习过程、能力掌握、自动化执行、真实环境和产品契约分别判断。格式检查通过不能代替测试通过，分析文档不能代替独立编码，Mock 通过不能代替真实服务契约。完整改进见 [学习平台优化实施说明](docs/LEARNING-PLATFORM-OPTIMIZATION.md)，历史边界见 [历史学习证据审查](docs/HISTORICAL-EVIDENCE-AUDIT.md)；Day 77 起的新知识章节进入 [分拆知识索引](docs/knowledge/README.md)。

## 每日完结后的知识落盘流程

学习者明确确认当天完成后，按以下顺序收尾。知识落盘是提交前置条件，未完成知识落盘时不得更新进度或创建提交：

1. 从当天讲解、实践和复盘中提取明确的知识点；
2. 在 `LEARNING-NOTES.md` 新增对应的 Day 章节，写入定义、解决的问题、心智模型、最小代码骨架、适用边界、常见误区、记忆要点和知识验收；
3. 同步 `LEARNING-NOTES.md` 的目录和知识主题索引，并确认章节可以脱离测试文件独立阅读；
4. 在 `daily-log/day-XXX.md` 填写明确的“知识点：”和“知识落盘记录”；
5. 更新 `progress.json`，使当天进入 `completed_days`；
6. 运行 `git diff --check` 和 `python tools/validate_repo.py`。验证失败时先修复知识落盘，不得提交；
7. 只暂存当天相关文件，复核暂存范围后创建本地提交；
8. 不执行 `git push`，除非用户明确要求。

知识文档的固定文本格式见 LEARNING-NOTES.md 的“落盘文本格式规范”。

## 目录说明

```text
qa-automation-learning/
├── .env.example
├── config/targets.json
├── test-projects/
│   ├── 01-todomvc-ui/
│   ├── 02-saucedemo-ui/
│   ├── 03-restful-booker-api/
│   └── 04-booker-platform/
├── daily-log/
├── artifacts/
├── LEARNING-NOTES.md
├── templates/
├── tools/
├── plugins/
├── TARGETS-SETUP.md
├── GIT-WORKFLOW.md
├── curriculum.json
├── daily-plan.json
├── DAILY-PLAN.md
├── ROADMAP.md
└── PLUGIN-AND-MCP.md
```

插件和本地 MCP 的边界见 [PLUGIN-AND-MCP.md](PLUGIN-AND-MCP.md)。

文件清理边界：`__pycache__`、`.pytest_cache`、`.ruff_cache` 可以再生成；本地服务日志和旧辅助截图不纳入日常提交。`docs/archive/*-v1.json` 仍用于生成历史课程，不能作为无用备份删除。`curriculum.json`、`daily-plan.json` 和 `DAILY-PLAN.md` 是不同入口使用的生成结果，更新时运行生成器，不手工删减。学习日志、正式验证记录和被引用的历史证据需要保留。

运行验证前，脚本会根据 config/targets.json 对已登记的本地目标执行服务预检：健康端点已可访问时直接复用；未启动时按目标配置启动并等待健康检查通过。服务启动失败会立即写入验证证据并跳过测试，避免长时间等待连接拒绝。需要手动管理服务时可使用 --skip-service。
