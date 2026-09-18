# 测试项目索引

本索引由 `config/project-roadmap.json` 生成。项目编号表示学习顺序；
只有已完成勘察并进入课程的项目才会在本目录创建测试资产。
第三方被测项目源码统一放在仓库外的 `D:\qa-automation-targets`。
当前课程已细化到 Day 77；完整路线预计在 Day 161–195 结束。

| 序号 | 状态 | 项目 | 测试资产目录 | 学习日 |
| --- | --- | --- | --- | --- |
| 01 | 已完成 | TodoMVC UI 基础 | `test-projects/01-todomvc-ui` | Day 1–14 |
| 02 | 已完成 | SauceDemo UI 业务流程 | `test-projects/02-saucedemo-ui` | Day 15–35、Day 66 |
| 03 | 已完成 | Restful Booker API | `test-projects/03-restful-booker-api` | Day 36–69 |
| 04 | 学习中 | Restful Booker Platform | `test-projects/04-booker-platform` | Day 70–77 |
| 05 | 待勘察 | Petstore 性能入门 | `test-projects/05-petstore-performance` | 待细化 |
| 06 | 待勘察 | Medusa 电商综合项目 | `test-projects/06-medusa-commerce` | 待细化 |
| 07 | 待勘察 | Saleor GraphQL 项目 | `test-projects/07-saleor-graphql` | 待细化 |
| 08 | 待勘察 | Juice Shop 安全专项 | `test-projects/08-juice-shop-security` | 待细化 |
| 09 | 待勘察 | 综合毕业项目 | `test-projects/09-capstone` | 待细化 |

新增项目时先完成版本、依赖、端口、契约和运行方式勘察，再更新路线图、
运行目标登记和课程源配置，最后运行 `python tools/build_daily_plan.py`。
待勘察项目不提前创建空目录、运行配置或学习日志。

测试代码通过环境配置访问目标，不依赖第三方源码的内部绝对路径。
