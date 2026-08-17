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
│   │   └── 04-petstore-performance
│   ├── config                          # 目标登记和可提交配置
│   ├── daily-log                       # 每日学习记录
│   ├── artifacts                       # 精选测试证据
│   ├── tools                           # 学习计划和辅助工具
│   └── plugins                         # 本地学习插件
│
└── qa-automation-targets              # 第三方被测项目，不属于当前 Git 仓库
    ├── todomvc
    ├── restful-booker
    └── swagger-petstore
```

四个 `test-projects/01-` 到 `test-projects/04-` 目录是测试工程目录，不是被测项目源码目录。被测项目的来源、路径、URL 和安全边界统一登记在 [config/targets.json](config/targets.json) 和 [TARGETS-SETUP.md](TARGETS-SETUP.md) 中。

## 学习路线

| 阶段 | 测试资产目录 | 被测目标 | 能力目标 |
| --- | --- | --- | --- |
| 1 | `test-projects/01-todomvc-ui` | 本地 TodoMVC clone | UI 定位、交互、断言、数据驱动 |
| 2 | `test-projects/02-saucedemo-ui` | SauceDemo 在线 Demo | 业务流程、Page Object、报告与稳定性 |
| 3 | `test-projects/03-restful-booker-api` | 本地 Restful Booker clone | API、鉴权、关联、Schema、清理 |
| 4 | `test-projects/04-petstore-performance` | 本地 Swagger Petstore clone | OpenAPI、接口回归、k6、性能与容量 |

公共网站只做轻量功能验证；压力、峰值、稳定性和容量测试只对本地或明确授权的环境执行。

## 初始化和运行

首次使用时，先复制环境模板并按实际端口修改：

```powershell
Copy-Item .env.example .env
```

再按 [GIT-WORKFLOW.md](GIT-WORKFLOW.md) 连接自己的远程仓库，并按 [TARGETS-SETUP.md](TARGETS-SETUP.md) 准备本地被测项目。

查看学习计划：

```powershell
python tools/plan_day.py today
python tools/plan_day.py plan 37
python tools/plan_day.py status
python tools/validate_repo.py
```

完成一个学习日并记录实际结果：

```powershell
python tools/plan_day.py complete 1 `
  --result "完成新增 Todo 测试并记录运行证据" `
  --next-step "增加完成状态场景"
```

当前计划包含 182 个核心学习日，覆盖 UI、API、性能、测试工程化、可靠性和作品集整理。每一天都按“学习 20 分钟 → 实践产出 50 分钟 → 运行验证 15 分钟 → 复盘 5 分钟”执行；计划明确记录知识、产出、验收标准和证据目录。计划由 [tools/build_daily_plan.py](tools/build_daily_plan.py) 生成，`daily-plan.json` 和 `DAILY-PLAN.md` 是生成结果，不应手工维护其中的单日路径。

## 每日完成标准

每个学习日至少留下：

1. 一条能用自己的话解释的知识重点；
2. 一个与该知识重点直接对应的可运行测试脚本或工程改动；
3. 一次真实执行结果，失败时记录根因或阻塞条件；
4. 一份学习记录、知识验收和证据路径；
5. 一份可脱离代码文件复习的 LEARNING-NOTES.md 知识章节；
6. 一次有意义的本地 Git 提交。

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
│   └── 04-petstore-performance/
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
