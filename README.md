# QA Automation Learning Lab

这是一个“项目驱动、每天有产出、长期可扩展”的自动化测试学习工程。

核心约定：每天完成一个可运行的小任务，并留下测试证据。每天的最低产出不是“看完一节课”，而是：

1. 一个新增或改进的测试脚本；
2. 一次真实执行结果（通过、失败或已定位原因都可以）；
3. 一份简短学习记录；
4. 一次 Git 提交。

## 四个主项目与能力递进

| 阶段 | 项目 | 能力目标 | 建议工具 |
| --- | --- | --- | --- |
| 1 | TodoMVC | UI 自动化基础、定位、断言、数据驱动 | Playwright、pytest |
| 2 | SauceDemo | 完整业务流、Page Object、报告与稳定性 | Playwright、pytest、Allure |
| 3 | Restful Booker | 接口自动化、鉴权、接口关联、数据清理 | requests/httpx、pytest、JSON Schema |
| 4 | Swagger Petstore 本地版 | API 契约、性能、压力、容量分析 | k6、Docker、Prometheus/Grafana |

前三个阶段建立功能自动化能力，第四阶段进入性能与工程化。公共网站和公共 API 只做轻量功能验证；压力测试必须对本地或明确授权的环境执行。

## 仓库边界与被测项目

本仓库只保存自己的测试脚本、测试配置、学习记录和必要的测试证据。第三方被测项目单独放在仓库外：

```text
D:\
├── qa-automation-learning       # 当前仓库：测试成果和学习记录
│   ├── 01-todomvc-ui
│   ├── 02-saucedemo-ui
│   ├── 03-restful-booker-api
│   └── 04-petstore-performance
│
└── qa-automation-targets        # 被测项目：第三方 Git clone
    ├── todomvc
    ├── restful-booker
    └── swagger-petstore
```

TodoMVC、Restful Booker 和 Swagger Petstore 在需要本地环境时 clone 到 `qa-automation-targets`；SauceDemo 直接测试在线地址，不需要 clone。完整命令见 [TARGETS-SETUP.md](TARGETS-SETUP.md)。

## 长期路线

`daily-plan.json` 和 `DAILY-PLAN.md` 内置 182 个核心学习日，超过核心阶段后会进入可循环的长期专项路线，而不是结束。每个核心学习日都明确了学习重点、当天产出、目标文件、运行命令、完成标准和可选挑战。

`curriculum.json` 保存阶段级路线，适合查看整体能力递进；逐日执行以 `daily-plan.json` 为准。

超过核心阶段后会进入可循环的长期专项路线：

- 自动化框架架构与插件化；
- 性能、压力、峰值、稳定性和容量模型；
- Docker、CI/CD、质量门禁和测试环境治理；
- 契约测试、视觉回归、可访问性和移动端；
- 安全测试、混沌/韧性、可观测性和生产质量；
- 作品集、技术方案、缺陷分析和面试表达。

## 每日工作节奏

默认按 90 分钟设计，可按实际时间缩放：

```text
10 分钟：阅读当天主题和已有代码
50 分钟：编写或改造一个脚本
20 分钟：运行、调试、保留证据
10 分钟：填写复盘并提交 Git
```

## 使用命令

在项目根目录执行：

```powershell
# 查看下一个学习日并生成 daily-log/day-XXX.md
python tools/plan_day.py today

# 查看完整逐日计划
Get-Content DAILY-PLAN.md

# 查看指定学习日的详细计划
python tools/plan_day.py plan 37

# 查看累计进度
python tools/plan_day.py status

# 完成一天并保存结果
python tools/plan_day.py complete 1 --result "新增 Todo 并验证完成状态" --next-step "增加删除场景"
```

命令会创建：

```text
daily-plan.json            # 182 天机器可读逐日计划
DAILY-PLAN.md              # 182 天可直接阅读的逐日计划
daily-log/day-XXX.md       # 当日计划、证据和复盘
artifacts/day-XXX/         # 截图、报告、日志等证据
progress.json              # 当前进度
```

## 每天的完成定义

当天任务只有满足以下条件才算完成：

- 脚本可以独立运行，或明确记录阻塞原因；
- 至少有一个业务断言，不只是打开页面或打印响应；
- 记录运行命令和结果；
- 记录一个今天真正理解的新知识；
- 若发现问题，留下最小复现步骤或缺陷记录。

## 进入下一阶段的门槛

每个阶段结束后，不以“天数到了”为唯一标准。满足以下条件再晋级：

- 核心任务完成率至少 80%；
- 能不看示例独立新增 3 个场景；
- 能解释一次失败的根因，而不只是重跑；
- 能说明当前方案的局限和下一步改进；
- 形成一份阶段总结和一份可展示的报告。

## 目录说明

```text
qa-automation-learning/
├── curriculum.json
├── daily-plan.json
├── DAILY-PLAN.md
├── ROADMAP.md
├── tools/plan_day.py
├── templates/
├── daily-log/
├── artifacts/
├── TARGETS-SETUP.md
├── 01-todomvc-ui/               # 只放 TodoMVC 测试代码
├── 02-saucedemo-ui/              # 只放 SauceDemo 测试代码
├── 03-restful-booker-api/        # 只放 Restful Booker 测试代码
└── 04-petstore-performance/      # 只放 Petstore/API 性能测试代码
```

插件和 MCP 的接入说明见 [PLUGIN-AND-MCP.md](PLUGIN-AND-MCP.md)。
