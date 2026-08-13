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
5. 一次有意义的 Git 提交。

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
