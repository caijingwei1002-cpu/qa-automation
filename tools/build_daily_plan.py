#!/usr/bin/env python3
"""Build the detailed, day-by-day QA automation learning plan."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def task(title: str, learn: str, deliverable: str, file: str, run: str, done: str, stretch: str) -> dict[str, str]:
    return {
        "title": title,
        "learn": learn,
        "deliverable": deliverable,
        "file": file,
        "run": run,
        "done": done,
        "stretch": stretch,
    }


PHASES = [
    {
        "id": "phase-1",
        "name": "TodoMVC UI 基础",
        "project": "01-todomvc-ui",
        "objective": "建立 UI 自动化基本功",
        "tasks": [
            task("环境与首个 UI 测试", "理解 Playwright、pytest、浏览器和断言的职责", "初始化项目并完成新增 Todo 测试", "01-todomvc-ui/tests/test_todos.py", "pytest 01-todomvc-ui/tests/test_todos.py::test_add_todo -q", "输入 Todo 后，列表文本和未完成计数断言通过", "保存首个失败截图"),
            task("完成状态", "掌握 checkbox 交互与状态断言", "完成一个 Todo 并验证 completed 状态", "01-todomvc-ui/tests/test_todos.py", "pytest 01-todomvc-ui/tests/test_todos.py::test_complete_todo -q", "复选框、样式状态和计数变化均被断言", "增加取消完成场景"),
            task("删除行为", "理解操作后的 DOM 与业务状态校验", "新增删除 Todo 测试", "01-todomvc-ui/tests/test_todos.py", "pytest 01-todomvc-ui/tests/test_todos.py::test_delete_todo -q", "目标项消失且剩余项目不受影响", "验证最后一项删除后页脚消失"),
            task("筛选功能", "掌握可见性和集合断言", "覆盖 All、Active、Completed 三种筛选", "01-todomvc-ui/tests/test_filters.py", "pytest 01-todomvc-ui/tests/test_filters.py -q", "每种筛选只展示正确状态的数据", "验证刷新后的筛选状态"),
            task("边界输入", "学习等价类和边界值", "覆盖空白、前后空格、重复文本和长文本", "01-todomvc-ui/tests/test_input_validation.py", "pytest 01-todomvc-ui/tests/test_input_validation.py -q", "至少四组边界数据有明确预期与断言", "增加 Unicode 和 emoji 输入"),
            task("参数化", "掌握 pytest.mark.parametrize", "把多组 Todo 输入改为参数化测试", "01-todomvc-ui/tests/test_todo_data.py", "pytest 01-todomvc-ui/tests/test_todo_data.py -q", "一份测试函数稳定运行多组数据", "为失败数据增加可读 id"),
            task("Fixture", "理解测试前置、后置和隔离", "用 fixture 统一打开页面和准备数据", "01-todomvc-ui/tests/conftest.py", "pytest 01-todomvc-ui/tests -q", "测试之间互不污染且公共准备代码减少", "增加 browser context fixture"),
            task("稳定定位", "比较 role、label、text、CSS 定位", "重构脆弱定位器并写定位规则", "01-todomvc-ui/tests/test_locators.py", "pytest 01-todomvc-ui/tests -q", "关键定位优先使用语义定位且全套通过", "故意改 DOM 验证定位韧性"),
            task("自动等待", "理解自动等待与显式等待边界", "移除固定 sleep 并增加状态等待测试", "01-todomvc-ui/tests/test_waiting.py", "pytest 01-todomvc-ui/tests/test_waiting.py -q", "代码无固定 sleep，异步状态有可解释等待", "模拟较慢交互"),
            task("失败证据", "掌握 screenshot、trace、日志用途", "配置失败截图和 Trace 保留", "01-todomvc-ui/conftest.py", "pytest 01-todomvc-ui/tests -q", "制造一次失败后可找到截图或 Trace", "记录如何打开 Trace"),
            task("标记与套件", "学习 smoke、regression 标记策略", "标记并拆分冒烟与回归测试", "01-todomvc-ui/pytest.ini", "pytest 01-todomvc-ui/tests -m smoke -q", "smoke 只包含关键路径且可单独执行", "添加 slow 标记"),
            task("数据与辅助函数", "区分测试数据、动作和断言", "提取 Todo 数据工厂或辅助函数", "01-todomvc-ui/tests/helpers.py", "pytest 01-todomvc-ui/tests -q", "测试主体更短且断言仍保留在测试中", "随机生成唯一文本"),
            task("小型回归", "学习按风险选择回归范围", "执行完整回归并整理失败清单", "01-todomvc-ui/tests/test_regression.py", "pytest 01-todomvc-ui/tests -q", "全套结果可复现，失败有原因和证据", "生成 JUnit XML"),
            task("阶段验收", "总结 UI 自动化基础与局限", "独立新增 Clear completed 端到端测试并写阶段总结", "01-todomvc-ui/tests/test_clear_completed.py", "pytest 01-todomvc-ui/tests -q", "不看示例完成新场景，全套通过并写阶段复盘", "说明三个最常见 flaky 来源"),
        ],
    },
    {
        "id": "phase-2",
        "name": "SauceDemo UI 框架",
        "project": "02-saucedemo-ui",
        "objective": "把脚本提升为可维护的业务自动化框架",
        "tasks": [
            task("项目初始化", "理解电商业务流和测试边界", "初始化 SauceDemo 项目并完成标准用户登录", "02-saucedemo-ui/tests/test_login.py", "pytest 02-saucedemo-ui/tests/test_login.py::test_standard_user_login -q", "登录后 URL 和商品页标题断言通过", "保存登录页元素清单"),
            task("登录异常", "学习负向场景与错误信息断言", "覆盖错误密码和空用户名", "02-saucedemo-ui/tests/test_login.py", "pytest 02-saucedemo-ui/tests/test_login.py -q", "错误类型对应正确提示且不会进入商品页", "增加空密码"),
            task("特殊用户", "理解测试账号代表的风险场景", "覆盖 locked_out_user 与 problem_user", "02-saucedemo-ui/tests/test_users.py", "pytest 02-saucedemo-ui/tests/test_users.py -q", "锁定用户行为正确，问题用户异常被记录", "研究 performance_glitch_user"),
            task("商品列表", "学习列表完整性与集合断言", "验证商品名称、价格、图片和数量", "02-saucedemo-ui/tests/test_inventory.py", "pytest 02-saucedemo-ui/tests/test_inventory.py -q", "列表数量与每项关键字段都有断言", "校验价格格式"),
            task("商品详情", "掌握列表到详情的导航验证", "验证进入详情和返回列表", "02-saucedemo-ui/tests/test_product_detail.py", "pytest 02-saucedemo-ui/tests/test_product_detail.py -q", "详情名称价格与列表一致", "参数化多个商品"),
            task("商品排序", "学习从页面提取数据并验证排序", "覆盖名称和价格四种排序", "02-saucedemo-ui/tests/test_sorting.py", "pytest 02-saucedemo-ui/tests/test_sorting.py -q", "提取值与排序期望完全一致", "处理浮点价格"),
            task("加入购物车", "理解跨页面状态断言", "加入单个商品并验证徽标和购物车内容", "02-saucedemo-ui/tests/test_cart.py", "pytest 02-saucedemo-ui/tests/test_cart.py::test_add_one_item -q", "徽标、名称和价格一致", "从详情页添加"),
            task("多商品购物车", "学习集合与合计准备", "加入多个商品并验证集合", "02-saucedemo-ui/tests/test_cart.py", "pytest 02-saucedemo-ui/tests/test_cart.py -q", "购物车集合与选择集合一致", "验证展示顺序"),
            task("移除商品", "掌握状态回退和幂等思路", "从列表和购物车分别移除商品", "02-saucedemo-ui/tests/test_cart_remove.py", "pytest 02-saucedemo-ui/tests/test_cart_remove.py -q", "徽标和购物车内容同步变化", "移除全部商品"),
            task("结算校验", "学习表单验证与字段组合", "覆盖姓名、姓氏、邮编必填错误", "02-saucedemo-ui/tests/test_checkout_validation.py", "pytest 02-saucedemo-ui/tests/test_checkout_validation.py -q", "每个缺失字段对应正确提示", "增加特殊字符"),
            task("结算概览", "学习金额与业务计算断言", "验证商品小计、税费和总价", "02-saucedemo-ui/tests/test_checkout_summary.py", "pytest 02-saucedemo-ui/tests/test_checkout_summary.py -q", "总价等于商品小计加税费", "使用 Decimal 计算"),
            task("完整下单", "建立关键端到端业务流", "完成登录到订单成功的 E2E 测试", "02-saucedemo-ui/tests/test_checkout_e2e.py", "pytest 02-saucedemo-ui/tests/test_checkout_e2e.py -q", "订单完成标题和购物车状态正确", "测试取消结算"),
            task("登出和会话", "理解认证状态和直接访问", "验证登出后不能直接进入商品页", "02-saucedemo-ui/tests/test_session.py", "pytest 02-saucedemo-ui/tests/test_session.py -q", "登出清理会话且受保护页面不可访问", "刷新页面验证会话"),
            task("Page Object 登录页", "理解页面对象职责边界", "创建 LoginPage 并重构登录测试", "02-saucedemo-ui/pages/login_page.py", "pytest 02-saucedemo-ui/tests/test_login.py -q", "定位和动作进入页面类，业务断言仍清晰", "增加组件对象"),
            task("Page Object 商品页", "减少重复选择器和操作", "创建 InventoryPage 与 CartPage", "02-saucedemo-ui/pages/inventory_page.py", "pytest 02-saucedemo-ui/tests/test_inventory.py 02-saucedemo-ui/tests/test_cart.py -q", "相关测试无重复关键定位器", "增加按商品名操作"),
            task("结算页面对象", "组织多页面业务流程", "创建 Checkout 页面对象并重构 E2E", "02-saucedemo-ui/pages/checkout_page.py", "pytest 02-saucedemo-ui/tests/test_checkout_e2e.py -q", "E2E 测试读起来像业务步骤", "避免万能 BasePage"),
            task("测试数据模型", "学习账号和商品数据管理", "集中管理用户、地址和商品数据", "02-saucedemo-ui/test_data.py", "pytest 02-saucedemo-ui/tests -q", "变化数据不散落在测试中", "使用 dataclass"),
            task("环境配置", "掌握 base_url 和环境切换", "加入 test 配置与命令行选项", "02-saucedemo-ui/config.py", "pytest 02-saucedemo-ui/tests -m smoke -q", "base_url 不硬编码且错误配置明确失败", "增加 .env.example"),
            task("多浏览器", "理解兼容性矩阵和执行成本", "在 Chromium、Firefox 运行 smoke", "02-saucedemo-ui/pytest.ini", "pytest 02-saucedemo-ui/tests -m smoke -q", "两种浏览器结果被记录", "增加移动视口"),
            task("报告与 flaky 分析", "区分产品缺陷、脚本缺陷和环境问题", "接入 HTML/Allure 报告并分析一次失败", "02-saucedemo-ui/README.md", "pytest 02-saucedemo-ui/tests -q", "报告包含步骤、失败证据和分类结论", "统计最慢测试"),
            task("阶段验收", "验证框架可维护性和独立开发能力", "独立新增跨页面回归场景并写架构说明", "02-saucedemo-ui/tests/test_portfolio_scenario.py", "pytest 02-saucedemo-ui/tests -q", "全套可运行、README 清楚、能解释 Page Object 取舍", "写五分钟演示脚本"),
        ],
    },
    {
        "id": "phase-3",
        "name": "Restful Booker API",
        "project": "03-restful-booker-api",
        "objective": "建立可回归、可关联、可清理的接口测试框架",
        "tasks": [
            task("HTTP 与健康检查", "理解请求、响应、状态码和超时", "初始化 API 项目并验证健康检查", "03-restful-booker-api/tests/test_health.py", "pytest 03-restful-booker-api/tests/test_health.py -q", "状态码、响应体和超时都有断言", "记录响应头"),
            task("查询列表", "掌握 GET 与集合响应", "查询 booking IDs 并校验结构", "03-restful-booker-api/tests/test_get_bookings.py", "pytest 03-restful-booker-api/tests/test_get_bookings.py -q", "列表类型和 bookingid 字段被校验", "按姓名过滤"),
            task("创建预订", "掌握 POST 与 JSON 请求体", "创建预订并断言完整返回", "03-restful-booker-api/tests/test_create_booking.py", "pytest 03-restful-booker-api/tests/test_create_booking.py -q", "id 存在且所有业务字段一致", "保存响应样例"),
            task("查询单条", "学习动态 ID 的接口关联", "创建后按 id 查询并比较数据", "03-restful-booker-api/tests/test_booking_flow.py", "pytest 03-restful-booker-api/tests/test_booking_flow.py -q", "创建与查询结果一致", "验证不存在 id"),
            task("过滤查询", "学习 query 参数和组合", "覆盖姓名和日期过滤", "03-restful-booker-api/tests/test_filters.py", "pytest 03-restful-booker-api/tests/test_filters.py -q", "每种过滤返回符合条件的数据", "组合多个参数"),
            task("Token 鉴权", "理解认证接口和凭据管理", "获取 Token 并验证无效凭据", "03-restful-booker-api/tests/test_auth.py", "pytest 03-restful-booker-api/tests/test_auth.py -q", "成功 Token 与失败原因都有断言", "Token 不打印到日志"),
            task("完整更新 PUT", "理解资源替换和认证头", "创建后完整更新预订", "03-restful-booker-api/tests/test_update_booking.py", "pytest 03-restful-booker-api/tests/test_update_booking.py -q", "更新响应和二次查询一致", "验证无 Token"),
            task("部分更新 PATCH", "理解 PUT 与 PATCH 差异", "只修改价格和附加需求", "03-restful-booker-api/tests/test_update_booking.py", "pytest 03-restful-booker-api/tests/test_update_booking.py -q", "目标字段变化，其他字段保持", "更新空字符串"),
            task("删除与清理", "学习资源生命周期和清理保证", "删除预订并确认不能查询", "03-restful-booker-api/tests/test_delete_booking.py", "pytest 03-restful-booker-api/tests/test_delete_booking.py -q", "删除成功且后续查询返回预期状态", "重复删除"),
            task("API Client", "建立请求封装边界", "封装 base URL、超时、headers 和通用请求", "03-restful-booker-api/src/api_client.py", "pytest 03-restful-booker-api/tests -q", "测试不再重复拼接 URL，失败信息可读", "增加响应日志"),
            task("Booking Client", "学习领域客户端", "封装 booking CRUD 方法", "03-restful-booker-api/src/booking_client.py", "pytest 03-restful-booker-api/tests -q", "测试通过领域方法表达业务动作", "保留原始 response"),
            task("Fixture 生命周期", "掌握 yield fixture 清理", "创建 booking fixture 并自动删除", "03-restful-booker-api/tests/conftest.py", "pytest 03-restful-booker-api/tests -q", "测试失败时也执行清理", "使用 session 级 Token"),
            task("数据工厂", "建立唯一且可复用的数据", "创建 booking data factory", "03-restful-booker-api/tests/factories.py", "pytest 03-restful-booker-api/tests -q", "每次数据唯一且默认值可覆盖", "使用 Faker 可选"),
            task("参数化边界", "覆盖价格、日期和姓名边界", "为核心字段增加参数化测试", "03-restful-booker-api/tests/test_boundaries.py", "pytest 03-restful-booker-api/tests/test_boundaries.py -q", "至少六组边界有明确预期", "加入超长文本"),
            task("缺失字段", "学习 API 负向测试", "逐个删除必填字段并记录行为", "03-restful-booker-api/tests/test_invalid_payloads.py", "pytest 03-restful-booker-api/tests/test_invalid_payloads.py -q", "服务行为被断言，意外行为记为缺陷", "测试空 JSON"),
            task("类型错误", "验证契约的输入类型边界", "覆盖字符串价格、非法布尔和嵌套错误", "03-restful-booker-api/tests/test_invalid_types.py", "pytest 03-restful-booker-api/tests/test_invalid_types.py -q", "错误类型结果可重复且有缺陷记录", "测试 null 值"),
            task("状态码与错误模型", "统一负向场景断言", "提取错误响应断言辅助函数", "03-restful-booker-api/tests/assertions.py", "pytest 03-restful-booker-api/tests -q", "状态码和错误体断言一致且可读", "禁止只断言非 200"),
            task("JSON Schema", "掌握结构契约验证", "为创建和查询响应增加 Schema", "03-restful-booker-api/schemas/booking.json", "pytest 03-restful-booker-api/tests -q", "缺失字段或类型变化能导致失败", "Schema 版本化"),
            task("业务断言", "区分结构正确和业务正确", "增加日期顺序、价格范围等规则", "03-restful-booker-api/tests/test_business_rules.py", "pytest 03-restful-booker-api/tests/test_business_rules.py -q", "至少三条业务规则被验证", "记录服务未校验规则"),
            task("接口链路", "组织创建、查询、更新、删除流程", "实现完整生命周期测试", "03-restful-booker-api/tests/test_booking_lifecycle.py", "pytest 03-restful-booker-api/tests/test_booking_lifecycle.py -q", "链路每一步都有局部断言和清理", "失败时打印当前 id"),
            task("配置分层", "学习环境变量与默认值", "加入 base_url、timeout、credentials 配置", "03-restful-booker-api/src/settings.py", "pytest 03-restful-booker-api/tests -m smoke -q", "配置可覆盖且敏感信息不进仓库", "增加配置校验"),
            task("日志与诊断", "学习请求上下文和脱敏", "记录 method、URL、耗时和状态码", "03-restful-booker-api/src/logging_config.py", "pytest 03-restful-booker-api/tests -q", "失败日志足够定位且 Token 被脱敏", "添加 correlation id"),
            task("重试边界", "理解可重试与不可重试错误", "为幂等 GET 设计有限重试", "03-restful-booker-api/src/retry.py", "pytest 03-restful-booker-api/tests/test_retry.py -q", "只对明确瞬态错误重试并有次数上限", "测试退避策略"),
            task("并行隔离", "理解并行导致的数据碰撞", "用 xdist 并行运行唯一数据测试", "03-restful-booker-api/tests/conftest.py", "pytest 03-restful-booker-api/tests -n 2 -q", "并行运行无共享数据冲突", "比较执行耗时"),
            task("测试标记", "建立 smoke、regression、negative 分类", "标记并验证不同套件", "03-restful-booker-api/pytest.ini", "pytest 03-restful-booker-api/tests -m smoke -q", "套件边界清晰且无 marker 警告", "生成 marker 清单"),
            task("报告", "把接口证据组织成可阅读报告", "接入 JUnit/Allure 并附加请求摘要", "03-restful-booker-api/README.md", "pytest 03-restful-booker-api/tests -q --junitxml=reports/api.xml", "报告可定位失败接口和数据", "统计错误类型"),
            task("缺陷案例", "训练高质量 Bug 表达", "基于异常行为写一份缺陷报告", "03-restful-booker-api/reports/defect-001.md", "pytest 03-restful-booker-api/tests/test_invalid_payloads.py -q", "包含复现、预期、实际、证据和影响", "补充最小 curl"),
            task("阶段验收", "验证独立设计 API 自动化能力", "独立新增一个资源链路并完成阶段报告", "03-restful-booker-api/reports/phase-review.md", "pytest 03-restful-booker-api/tests -q", "框架全套通过或失败可解释，文档可一键运行", "绘制 API 测试架构图"),
        ],
    },
    {
        "id": "phase-4",
        "name": "Swagger Petstore API 与性能入口",
        "project": "04-petstore-performance",
        "objective": "从 OpenAPI 契约进入性能和容量测试",
        "tasks": [
            task("本地 Petstore", "理解压测授权边界与本地环境", "用 Docker 启动 Petstore 并完成健康检查", "04-petstore-performance/docker-compose.yml", "docker compose -f 04-petstore-performance/docker-compose.yml up -d", "本地服务可访问且记录版本和端口", "保存容器资源基线"),
            task("OpenAPI 阅读", "学习从规范提取测试范围", "列出 pet、store、user 核心接口和字段", "04-petstore-performance/docs/api-inventory.md", "git diff --check", "接口清单包含方法、路径、鉴权和风险", "标注性能热点"),
            task("查询契约", "建立 API 契约回归", "为 GET pet 增加 Schema 和错误场景", "04-petstore-performance/tests/test_get_pet.py", "pytest 04-petstore-performance/tests/test_get_pet.py -q", "成功与不存在场景都有契约断言", "检查 content-type"),
            task("CRUD 链路", "准备性能测试前的功能基线", "实现 pet 创建、查询、修改、删除", "04-petstore-performance/tests/test_pet_lifecycle.py", "pytest 04-petstore-performance/tests/test_pet_lifecycle.py -q", "链路可重复且数据可清理", "加入唯一 id"),
            task("契约漂移", "理解 OpenAPI 与实现差异", "写脚本比较关键响应与规范", "04-petstore-performance/tests/test_contract.py", "pytest 04-petstore-performance/tests/test_contract.py -q", "至少覆盖两个接口并记录差异", "输出差异报告"),
            task("k6 首脚本", "理解 VU、iteration、duration", "编写单用户查询冒烟脚本", "04-petstore-performance/k6/smoke.js", "k6 run 04-petstore-performance/k6/smoke.js", "请求成功且 check、指标可读", "加入自定义 Trend"),
            task("性能断言", "学习 check 与 threshold 区别", "设置错误率和 p95 阈值", "04-petstore-performance/k6/thresholds.js", "k6 run 04-petstore-performance/k6/thresholds.js", "阈值通过，故意收紧时能失败", "加入 p99"),
            task("测试数据", "避免压测数据竞争", "编写 setup/teardown 生成和清理 pet", "04-petstore-performance/k6/data_setup.js", "k6 run 04-petstore-performance/k6/data_setup.js", "数据唯一且结束后可清理", "从 JSON 加载数据"),
            task("场景建模", "把真实业务比例映射到脚本", "设计读写比例和用户停顿", "04-petstore-performance/docs/workload-model.md", "git diff --check", "文档解释 VU、持续时间和业务比例", "使用 scenarios executor"),
            task("阶梯负载", "观察响应随负载变化", "实现 5→10→20 VU 负载脚本", "04-petstore-performance/k6/load.js", "k6 run 04-petstore-performance/k6/load.js", "记录各阶段吞吐、错误率和 p95", "输出 JSON summary"),
            task("基线报告", "学习可比较的性能基线", "执行固定负载并填写基线报告", "04-petstore-performance/reports/baseline.md", "k6 run --summary-export=artifacts/baseline.json 04-petstore-performance/k6/load.js", "报告包含环境、负载、指标和结论", "重复三次比较波动"),
            task("资源监控", "关联应用指标与请求指标", "记录容器 CPU、内存和网络", "04-petstore-performance/docs/monitoring.md", "docker stats --no-stream", "同一时间窗口有 k6 与资源证据", "加入数据库连接"),
            task("压力测试", "寻找性能拐点而非只压垮", "逐级增加 VU 直到阈值持续恶化", "04-petstore-performance/k6/stress.js", "k6 run 04-petstore-performance/k6/stress.js", "记录首个明显拐点和停止条件", "比较读写瓶颈"),
            task("峰值测试", "理解突发流量与恢复", "实现低负载瞬间升高再回落", "04-petstore-performance/k6/spike.js", "k6 run 04-petstore-performance/k6/spike.js", "记录峰值错误和恢复时间", "修改峰值持续时间"),
            task("稳定性测试", "识别资源泄漏和累积问题", "实现受控的 soak 脚本", "04-petstore-performance/k6/soak.js", "k6 run 04-petstore-performance/k6/soak.js", "趋势无持续恶化或有明确证据", "按机器能力缩短预演"),
            task("容量分析", "学习安全容量与极限容量区别", "根据负载曲线计算建议并发", "04-petstore-performance/reports/capacity.md", "python 04-petstore-performance/tools/analyze_results.py", "给出容量区间、依据和安全余量", "画 VU-p95 曲线"),
            task("瓶颈假设", "用证据建立可验证假设", "选择最慢接口分析可能原因", "04-petstore-performance/reports/bottleneck.md", "k6 run 04-petstore-performance/k6/focused.js", "假设引用请求和资源指标", "设计 A/B 验证"),
            task("参数与环境", "让性能脚本可复用", "支持 BASE_URL、VUS、DURATION 环境变量", "04-petstore-performance/k6/configurable.js", "k6 run -e VUS=5 -e DURATION=30s 04-petstore-performance/k6/configurable.js", "配置有默认值且输出实际参数", "防止误指向生产域名"),
            task("CI 性能冒烟", "学习性能质量门禁边界", "加入短时 k6 smoke CI 配置", "04-petstore-performance/.github/workflows/performance-smoke.yml", "k6 run 04-petstore-performance/k6/smoke.js", "CI 场景短、稳定且阈值明确", "保存 summary artifact"),
            task("性能报告", "形成可读的非功能测试结论", "完成包含图表、瓶颈和建议的报告", "04-petstore-performance/reports/performance-report.md", "git diff --check", "报告能回答容量、拐点、错误率和风险", "补充执行限制"),
            task("阶段验收", "验证独立设计性能测试能力", "从目标到报告独立完成一次受控测试", "04-petstore-performance/reports/phase-review.md", "k6 run 04-petstore-performance/k6/smoke.js", "脚本、阈值、证据、报告齐全且未测试公共服务", "五分钟讲解容量结论"),
        ],
    },
    {
        "id": "phase-5",
        "name": "测试工程化",
        "project": "03-restful-booker-api",
        "objective": "让测试框架能被团队持续使用",
        "tasks": [
            task("配置模型", "学习环境配置分层", "实现默认值、环境变量和校验", "03-restful-booker-api/src/settings.py", "pytest 03-restful-booker-api/tests/test_settings.py -q", "缺失必需配置时快速失败且敏感值不提交", "支持多个环境"),
            task("依赖锁定", "理解可复现环境", "整理 pyproject 或 requirements 与锁定策略", "03-restful-booker-api/pyproject.toml", "python -m pip check", "依赖声明可安装且无冲突", "加入开发依赖组"),
            task("Docker 化测试", "学习容器化测试运行器", "创建自动化测试 Dockerfile", "03-restful-booker-api/Dockerfile", "docker build -t qa-api-tests 03-restful-booker-api", "镜像构建成功且入口明确", "使用非 root 用户"),
            task("Compose 环境", "编排被测服务与测试", "创建测试环境 compose 文件", "03-restful-booker-api/docker-compose.yml", "docker compose -f 03-restful-booker-api/docker-compose.yml config", "配置解析成功且服务依赖清晰", "加入 healthcheck"),
            task("环境就绪检查", "避免服务未启动导致假失败", "实现轮询健康检查和超时", "03-restful-booker-api/tools/wait_for_service.py", "python 03-restful-booker-api/tools/wait_for_service.py", "可区分就绪、超时和连接错误", "加入指数退避"),
            task("数据库连接", "理解 API 与数据层校验边界", "封装只读数据库连接 fixture", "03-restful-booker-api/src/db_client.py", "pytest 03-restful-booker-api/tests/test_db_connection.py -q", "连接可关闭且查询参数化", "连接池"),
            task("数据库断言", "学习何时需要跨层校验", "创建预订后验证关键数据库字段", "03-restful-booker-api/tests/test_booking_db.py", "pytest 03-restful-booker-api/tests/test_booking_db.py -q", "API 与 DB 关键字段一致", "验证删除"),
            task("数据清理", "建立可靠 teardown", "实现带前缀的测试数据清理工具", "03-restful-booker-api/tools/cleanup_test_data.py", "python 03-restful-booker-api/tools/cleanup_test_data.py --dry-run", "默认 dry-run，只清理明确测试数据", "输出清理报告"),
            task("数据工厂进阶", "生成可控且可复现的数据", "支持 seed 和场景化 builder", "03-restful-booker-api/tests/factories.py", "pytest 03-restful-booker-api/tests/test_factories.py -q", "同 seed 可复现且字段可覆盖", "增加非法数据 builder"),
            task("日志结构化", "提高 CI 失败诊断效率", "输出 JSON 或键值日志并脱敏", "03-restful-booker-api/src/logging_config.py", "pytest 03-restful-booker-api/tests -m smoke -q", "日志含 test、method、status、duration", "增加 trace id"),
            task("自定义断言", "提升失败信息质量", "封装字段、Schema、业务断言", "03-restful-booker-api/tests/assertions.py", "pytest 03-restful-booker-api/tests/test_assertions.py -q", "失败信息显示期望、实际和上下文", "支持软断言讨论"),
            task("Allure 步骤", "让报告表达业务链路", "为 API client 和生命周期增加步骤", "03-restful-booker-api/tests/test_booking_lifecycle.py", "pytest 03-restful-booker-api/tests/test_booking_lifecycle.py --alluredir=allure-results", "报告步骤清楚且附件脱敏", "附加响应摘要"),
            task("报告历史", "观察趋势而非单次结果", "保存测试历史和趋势说明", "03-restful-booker-api/reports/README.md", "pytest 03-restful-booker-api/tests --junitxml=reports/latest.xml", "报告路径稳定且历史策略明确", "制作趋势脚本"),
            task("Marker 规范", "建立团队可理解的分类", "定义 smoke、regression、negative、db", "03-restful-booker-api/pytest.ini", "pytest 03-restful-booker-api/tests --markers", "无未知 marker 且分类说明清楚", "增加 owner 标记"),
            task("选择性执行", "根据变更范围运行测试", "编写按标签和路径的运行脚本", "03-restful-booker-api/tools/run_tests.ps1", "powershell -File 03-restful-booker-api/tools/run_tests.ps1 -Suite smoke", "参数错误会快速失败", "增加 dry-run"),
            task("并行基线", "量化并行收益和风险", "比较串行与 2 workers 执行", "03-restful-booker-api/reports/parallel.md", "pytest 03-restful-booker-api/tests -n 2 -q", "记录耗时、失败和资源差异", "测试 4 workers"),
            task("flaky 识别", "学习重复执行诊断", "重复运行疑似不稳定测试并统计", "03-restful-booker-api/tools/repeat_test.py", "python 03-restful-booker-api/tools/repeat_test.py", "结果显示运行次数、失败次数和种子", "不要自动忽略失败"),
            task("重试策略", "限制重试范围并保留首次失败", "为明确瞬态场景配置一次重试", "03-restful-booker-api/docs/retry-policy.md", "pytest 03-restful-booker-api/tests -m transient -q", "文档说明哪些可重试、哪些禁止", "验证首次失败证据"),
            task("超时治理", "防止测试无限等待", "为 HTTP、fixture、CI 设置分层超时", "03-restful-booker-api/pyproject.toml", "pytest 03-restful-booker-api/tests -m smoke -q", "超时有明确错误且值有依据", "记录慢测试"),
            task("GitHub Actions 基础", "建立自动执行", "创建 pull request smoke workflow", "03-restful-booker-api/.github/workflows/api-smoke.yml", "pytest 03-restful-booker-api/tests -m smoke -q", "workflow 含安装、执行和报告上传", "加入依赖缓存"),
            task("回归流水线", "区分快速反馈和完整回归", "创建 nightly/full regression workflow", "03-restful-booker-api/.github/workflows/api-regression.yml", "pytest 03-restful-booker-api/tests -m regression -q", "smoke 与 regression 时机和超时不同", "增加手动触发参数"),
            task("质量门禁", "把通过标准写成规则", "设置测试、覆盖率或失败率门禁", "03-restful-booker-api/docs/quality-gates.md", "pytest 03-restful-booker-api/tests -q", "规则可衡量且失败时阻止流水线", "区分警告指标"),
            task("测试覆盖映射", "连接需求、风险和自动化", "创建需求-用例-脚本追踪表", "03-restful-booker-api/docs/traceability.md", "pytest 03-restful-booker-api/tests --collect-only -q", "关键需求均有脚本或风险说明", "自动生成收集清单"),
            task("代码质量", "统一格式、lint 和类型检查", "配置 ruff 或等效工具", "03-restful-booker-api/pyproject.toml", "ruff check 03-restful-booker-api", "检查可执行且规则不过度噪声", "加入 pre-commit"),
            task("Secret 治理", "避免账号和 Token 泄漏", "增加 env 示例、忽略规则和脱敏测试", "03-restful-booker-api/tests/test_secret_masking.py", "pytest 03-restful-booker-api/tests/test_secret_masking.py -q", "日志与仓库不包含真实凭据", "扫描测试产物"),
            task("维护指南", "让别人能新增测试", "编写贡献、命名、fixture 和调试规范", "03-restful-booker-api/CONTRIBUTING.md", "pytest 03-restful-booker-api/tests -m smoke -q", "新成员按文档能运行并新增测试", "加入 PR checklist"),
            task("一键验证", "统一本地和 CI 入口", "创建 verify.ps1 执行格式、lint、smoke", "03-restful-booker-api/tools/verify.ps1", "powershell -File 03-restful-booker-api/tools/verify.ps1", "一个命令给出明确阶段结果", "失败即停止"),
            task("阶段验收", "评估工程是否可被团队持续使用", "从干净环境按 README 执行并写工程化报告", "03-restful-booker-api/reports/engineering-review.md", "powershell -File 03-restful-booker-api/tools/verify.ps1", "配置、环境、报告、CI、维护文档完整", "列出三项技术债"),
        ],
    },
    {
        "id": "phase-6",
        "name": "高级质量专项",
        "project": "advanced-quality",
        "objective": "覆盖真实团队常见的非功能质量问题",
        "tasks": [
            task("契约测试进阶", "理解消费者与提供者契约", "为一个 API 定义消费者期望", "advanced-quality/contracts/consumer_contract.json", "pytest advanced-quality/contracts/test_contract.py -q", "契约包含请求、响应和版本", "比较 Schema 测试"),
            task("契约破坏验证", "识别 breaking change", "制造字段删除并验证契约失败", "advanced-quality/contracts/test_breaking_change.py", "pytest advanced-quality/contracts/test_breaking_change.py -q", "破坏性变化能被测试捕获", "定义兼容变化"),
            task("Mock Server", "隔离不稳定下游", "创建本地 Mock 响应服务", "advanced-quality/mocks/mock_server.py", "pytest advanced-quality/mocks/test_mock_server.py -q", "正常、超时、5xx 可配置", "记录请求"),
            task("测试替身选择", "区分 stub、mock、fake", "为三个场景选择合适替身并实现一个", "advanced-quality/mocks/README.md", "pytest advanced-quality/mocks -q", "文档说明取舍且实现可运行", "避免过度 Mock"),
            task("异步轮询", "测试最终一致性", "实现带超时的状态轮询 helper", "advanced-quality/async/wait_until.py", "pytest advanced-quality/async/test_wait_until.py -q", "成功、超时、异常均有测试", "加入退避"),
            task("幂等与重复消费", "验证重复请求影响", "设计重复提交场景并断言副作用", "advanced-quality/async/test_idempotency.py", "pytest advanced-quality/async/test_idempotency.py -q", "重复操作不会产生意外重复数据或被记录为缺陷", "并发重复提交"),
            task("消息测试模型", "理解生产、消费和确认", "为模拟队列编写消息流程测试", "advanced-quality/async/test_message_flow.py", "pytest advanced-quality/async/test_message_flow.py -q", "覆盖成功、重试、死信概念", "测试乱序消息"),
            task("视觉基线", "理解截图比较和阈值", "创建稳定页面视觉基线", "advanced-quality/visual/test_visual_baseline.py", "pytest advanced-quality/visual/test_visual_baseline.py -q", "基线可复现且环境被记录", "增加跨视口"),
            task("动态区域处理", "降低视觉误报", "屏蔽时间、动画或随机内容", "advanced-quality/visual/test_masking.py", "pytest advanced-quality/visual/test_masking.py -q", "动态内容变化不导致误报，真实变化会失败", "比较阈值"),
            task("响应式布局", "覆盖桌面、平板、手机视口", "参数化三个视口的核心页面", "advanced-quality/visual/test_responsive.py", "pytest advanced-quality/visual/test_responsive.py -q", "无横向溢出且关键控件可见", "测试设备像素比"),
            task("键盘可访问性", "验证非鼠标操作", "覆盖 Tab、Enter、Escape 流程", "advanced-quality/accessibility/test_keyboard.py", "pytest advanced-quality/accessibility/test_keyboard.py -q", "焦点顺序和操作结果正确", "检查 focus 可见"),
            task("可访问性扫描", "学习自动扫描的边界", "接入 axe 或等效规则检查", "advanced-quality/accessibility/test_axe.py", "pytest advanced-quality/accessibility/test_axe.py -q", "严重违规被报告且有页面上下文", "人工检查一项"),
            task("语义与标签", "验证表单名称和错误关联", "覆盖 label、role、aria-describedby", "advanced-quality/accessibility/test_semantics.py", "pytest advanced-quality/accessibility/test_semantics.py -q", "关键控件有可访问名称，错误可关联", "检查标题层级"),
            task("移动端交互", "理解触摸和小屏风险", "验证移动视口下核心流程", "advanced-quality/mobile/test_mobile_flow.py", "pytest advanced-quality/mobile/test_mobile_flow.py -q", "关键按钮可点击且布局无阻断", "测试横屏"),
            task("慢网络", "测试等待和用户反馈", "模拟高延迟加载", "advanced-quality/network/test_slow_network.py", "pytest advanced-quality/network/test_slow_network.py -q", "加载态、超时或重试行为有断言", "模拟图片加载失败"),
            task("断网恢复", "验证网络切换后的恢复能力", "实现 offline 到 online 场景", "advanced-quality/network/test_offline_recovery.py", "pytest advanced-quality/network/test_offline_recovery.py -q", "离线提示正确，恢复后可继续", "重复切换"),
            task("服务 5xx", "验证错误处理与重试边界", "拦截 API 返回 500/503", "advanced-quality/network/test_server_errors.py", "pytest advanced-quality/network/test_server_errors.py -q", "用户提示和重试行为符合设计", "增加 429 限流"),
            task("认证边界", "覆盖未登录、过期和伪造凭据", "编写认证负向测试", "advanced-quality/security/test_authentication.py", "pytest advanced-quality/security/test_authentication.py -q", "三类无效凭据均不能访问", "Token 日志脱敏"),
            task("授权边界", "验证水平和垂直越权", "设计用户 A 访问用户 B 数据测试", "advanced-quality/security/test_authorization.py", "pytest advanced-quality/security/test_authorization.py -q", "未授权访问被拒绝且无数据泄漏", "验证管理员边界"),
            task("输入安全", "覆盖注入式和超长输入安全行为", "建立安全输入参数集", "advanced-quality/security/test_input_handling.py", "pytest advanced-quality/security/test_input_handling.py -q", "服务不崩溃且错误响应不泄漏内部信息", "测试文件名输入"),
            task("敏感信息", "检查响应、日志、报告泄漏", "扫描测试产物中的 Token/密码模式", "advanced-quality/security/test_secret_leaks.py", "pytest advanced-quality/security/test_secret_leaks.py -q", "示例秘密可检测，正常数据不误报", "扫描截图文本"),
            task("时间与时区", "验证边界日期和时区转换", "覆盖跨日、闰日、夏令时场景", "advanced-quality/time/test_timezones.py", "pytest advanced-quality/time/test_timezones.py -q", "固定时钟下结果可复现", "测试过期时间"),
            task("本地化", "测试多语言和字符集", "覆盖中文、英文、长文案和 RTL 风险", "advanced-quality/i18n/test_localization.py", "pytest advanced-quality/i18n/test_localization.py -q", "字符不乱码，布局关键元素可用", "验证数字日期格式"),
            task("文件上传", "验证类型、大小和错误处理", "测试允许、拒绝和边界文件", "advanced-quality/files/test_upload.py", "pytest advanced-quality/files/test_upload.py -q", "文件策略被断言且临时文件清理", "测试同名文件"),
            task("下载验证", "校验文件名、类型和内容", "实现下载并检查内容", "advanced-quality/files/test_download.py", "pytest advanced-quality/files/test_download.py -q", "下载文件存在、类型正确、内容可验证", "测试并发下载"),
            task("状态机测试", "用状态转换发现遗漏", "为订单或 Todo 建立状态机并测试", "advanced-quality/state/test_state_machine.py", "pytest advanced-quality/state/test_state_machine.py -q", "允许和禁止的转换均被覆盖", "尝试属性测试"),
            task("风险测试策略", "按风险分配自动化层级", "为四项目写风险与覆盖策略", "advanced-quality/TEST-STRATEGY.md", "git diff --check", "策略说明测什么、不测什么和原因", "增加测试金字塔"),
            task("阶段验收", "整合高级质量能力", "选择三项专项形成可运行质量套件", "advanced-quality/reports/phase-review.md", "pytest advanced-quality -q", "至少三类专项有脚本、证据和局限说明", "做一次风险评审演示"),
        ],
    },
    {
        "id": "phase-7",
        "name": "生产质量与可靠性",
        "project": "04-petstore-performance",
        "objective": "从测试结果推导系统容量、风险和恢复能力",
        "tasks": [
            task("监控基线", "理解 CPU、内存、连接池与错误率", "记录服务资源基线", "04-petstore-performance/reliability/baseline.md", "docker stats --no-stream", "同一时间窗口的资源基线可复现", "记录磁盘和网络"),
            task("请求指标", "理解吞吐、延迟和错误率关联", "整理 k6 指标采集脚本", "04-petstore-performance/reliability/metrics.js", "k6 run 04-petstore-performance/reliability/metrics.js", "关键指标按接口和场景区分", "增加自定义业务指标"),
            task("p95/p99 对比", "避免只看平均响应时间", "比较不同并发级别的尾延迟", "04-petstore-performance/reliability/tail-latency.md", "k6 run 04-petstore-performance/k6/load.js", "报告解释平均值与尾延迟差异", "按接口分组"),
            task("慢接口定位", "建立从指标到假设的路径", "选择最慢接口写瓶颈假设", "04-petstore-performance/reliability/slow-endpoint.md", "k6 run 04-petstore-performance/k6/focused.js", "假设引用请求和资源证据", "设计 A/B 验证"),
            task("30 分钟稳定性", "识别资源泄漏和累积问题", "执行受控 soak 测试", "04-petstore-performance/k6/soak.js", "k6 run 04-petstore-performance/k6/soak.js", "趋势无持续恶化或有明确证据", "按机器能力缩短预演"),
            task("恢复时间", "理解故障检测与恢复指标", "记录一次服务重启后的恢复时间", "04-petstore-performance/reliability/recovery.md", "docker compose restart", "恢复步骤、耗时和数据影响有记录", "自动化健康检查"),
            task("依赖故障", "理解下游故障对用户流的影响", "模拟依赖超时或 5xx", "04-petstore-performance/reliability/dependency-failure.md", "pytest advanced-quality/network/test_server_errors.py -q", "超时、错误提示和恢复路径有断言", "验证降级"),
            task("超时策略", "区分连接、读取和总超时", "为测试和服务列出超时策略", "04-petstore-performance/reliability/timeouts.md", "git diff --check", "每个超时有依据、上限和告警行为", "测慢网络"),
            task("重试风暴", "理解重试放大效应", "模拟重试并记录请求放大", "04-petstore-performance/reliability/retry-storm.md", "k6 run 04-petstore-performance/k6/retry.js", "能说明重试次数对吞吐和延迟的影响", "加入抖动"),
            task("限流", "理解保护系统的限流策略", "设计并验证 429 场景", "04-petstore-performance/reliability/rate-limit.md", "k6 run 04-petstore-performance/k6/spike.js", "限流阈值、用户提示和恢复有记录", "区分客户端和服务端限流"),
            task("峰值恢复", "观察突发流量后的恢复质量", "执行 spike 并记录恢复曲线", "04-petstore-performance/reports/spike-recovery.md", "k6 run 04-petstore-performance/k6/spike.js", "报告包含峰值、错误和恢复时间", "增加两种峰值"),
            task("容量拐点", "计算安全并发和极限并发", "更新容量曲线与建议", "04-petstore-performance/reports/capacity.md", "python 04-petstore-performance/tools/analyze_results.py", "建议包含依据、安全余量和限制", "区分读写容量"),
            task("SLO 草案", "把技术指标翻译成用户目标", "为核心接口写 SLI/SLO 草案", "04-petstore-performance/reliability/slo.md", "git diff --check", "指标、目标、窗口和排除项明确", "加入错误预算"),
            task("告警验证", "避免只配置不验证告警", "为错误率或 p95 写告警测试说明", "04-petstore-performance/reliability/alert-test.md", "git diff --check", "能说明如何触发、观察、恢复和关闭", "模拟告警噪声"),
            task("日志关联", "用 trace id 串起请求与错误", "为一次失败链路整理日志证据", "04-petstore-performance/reliability/traceability.md", "pytest advanced-quality -q", "从测试结果能定位到对应日志上下文", "加入请求 id"),
            task("数据一致性", "验证故障期间的数据状态", "设计中断后数据一致性检查", "04-petstore-performance/reliability/data-consistency.py", "pytest 03-restful-booker-api/tests -q", "中断、重试、恢复后的数据结论明确", "重复执行"),
            task("安全恢复", "考虑凭据和数据在恢复流程中的风险", "写恢复过程安全检查清单", "04-petstore-performance/reliability/recovery-security.md", "git diff --check", "清单覆盖秘密、权限、数据和日志", "做一次演练"),
            task("可靠性演练", "把故障注入变成可控实验", "设计一次本地故障演练方案", "04-petstore-performance/reliability/experiment.md", "git diff --check", "有假设、停止条件、观察指标和回滚步骤", "执行小规模演练"),
            task("性能回归", "理解基线变化与质量趋势", "将本轮性能结果与历史基线比较", "04-petstore-performance/reports/performance-regression.md", "k6 run 04-petstore-performance/k6/smoke.js", "报告说明指标变化、阈值判断和可能原因", "加入自动趋势差异"),
            task("完整性能复盘", "综合请求、资源和恢复证据", "完成一次可靠性报告", "04-petstore-performance/reports/reliability-report.md", "git diff --check", "报告有结论、证据、风险和后续动作", "制作指标图"),
            task("阶段验收", "评估从性能测试到生产质量的能力", "完成容量、稳定性和恢复三项验收", "04-petstore-performance/reports/reliability-review.md", "k6 run 04-petstore-performance/k6/smoke.js", "能讲清容量、瓶颈、恢复和限制", "做十分钟演示"),
        ],
    },
    {
        "id": "phase-8",
        "name": "作品集与技术表达",
        "project": "qa-automation-learning",
        "objective": "把学习成果整理为可展示、可复用的工程资产",
        "tasks": [
            task("项目 README", "学习让陌生人快速运行项目", "补齐根目录 README 和一键运行说明", "README.md", "git diff --check", "新用户能找到环境、命令和阶段入口", "增加故障排查"),
            task("架构图", "用图表达测试分层和数据流", "绘制 UI、API、性能和 CI 架构图", "docs/test-architecture.md", "git diff --check", "图中组件、依赖和证据流清晰", "加入 Mermaid"),
            task("测试策略", "从需求、风险到测试层级表达", "整理四项目总体测试策略", "docs/test-strategy.md", "git diff --check", "说明覆盖范围、优先级和不测项", "增加风险矩阵"),
            task("缺陷案例一", "训练高质量功能缺陷表达", "整理一个 UI 缺陷案例", "reports/defect-ui.md", "git diff --check", "复现、预期、实际、证据和影响完整", "补充修复验证"),
            task("缺陷案例二", "训练接口缺陷表达", "整理一个 API 缺陷案例", "reports/defect-api.md", "git diff --check", "请求、响应、环境和严重程度完整", "补充最小 curl"),
            task("性能案例", "训练性能问题叙述", "整理一次瓶颈定位案例", "reports/defect-performance.md", "git diff --check", "基线、负载、指标、假设和结论完整", "增加优化前后对比"),
            task("测试指标", "理解指标的价值和误用", "定义脚本数、通过率、flaky、p95 等指标", "docs/quality-metrics.md", "git diff --check", "每个指标有用途、计算和限制", "增加趋势示例"),
            task("报告截图", "选择能证明能力的证据", "整理测试报告、Trace 和性能图截图", "docs/evidence-index.md", "git diff --check", "每张图有上下文、日期和对应代码", "生成缩略图索引"),
            task("CI 展示", "理解流水线如何展示质量", "整理 smoke、regression、performance workflow", "docs/ci-overview.md", "git diff --check", "触发条件、门禁和产物清晰", "补充失败流程"),
            task("代码重构", "从学习代码提升工程质量", "选择一个重复最多的模块重构", "refactor/README.md", "pytest -q", "重构前后行为一致且重复减少", "记录取舍"),
            task("命名规范", "提高测试可读性", "统一测试、fixture、页面对象命名", "docs/naming.md", "git diff --check", "规范有正反例且已有代码至少改一处", "增加 lint 规则"),
            task("调试手册", "把个人经验变成可复用知识", "整理环境、定位、数据和性能排查手册", "docs/debugging.md", "git diff --check", "至少包含五类常见问题和命令", "让别人按手册排障"),
            task("学习总结", "识别能力变化而非只列工具", "写一份阶段能力矩阵", "docs/skills-matrix.md", "git diff --check", "能说明从基础到高级的能力证据", "给每项能力打等级"),
            task("五分钟演示", "训练技术方案口头表达", "写出五分钟项目演示脚本", "docs/demo-script.md", "git diff --check", "包含目标、架构、脚本、结果和下一步", "实际计时演练"),
            task("面试项目介绍", "把工程决策讲清楚", "准备项目介绍和常见追问答案", "docs/interview-project.md", "git diff --check", "能回答为什么选工具、如何处理 flaky 和性能", "增加英文术语"),
            task("测试设计题", "综合业务、风险和自动化", "为一个新功能写测试设计方案", "docs/test-design-exercise.md", "git diff --check", "包含场景、优先级、自动化层级和风险", "加容量问题"),
            task("贡献指南", "让仓库适合协作", "补充分支、提交、审查和报告规范", "CONTRIBUTING.md", "git diff --check", "新人可按文档完成第一次提交", "增加 PR 模板"),
            task("发布清单", "建立交付前质量检查", "写自动化测试项目发布 checklist", "docs/release-checklist.md", "git diff --check", "功能、性能、安全、文档和回滚都有检查", "接入 CI"),
            task("最终回归", "验证整理没有破坏已有成果", "运行各项目 smoke 和核心回归", "reports/final-regression.md", "pytest -q", "结果、失败和环境均有记录", "并行运行"),
            task("最终总结", "形成可展示的完整作品集", "完成项目总结、局限和下一轮路线", "FINAL-REPORT.md", "git diff --check", "报告能回答学了什么、做了什么、如何验证和下一步", "制作 PDF/演示版本"),
            task("阶段验收", "完成长期学习主线闭环", "提交最终作品集并规划下一个 28 天专项", "ROADMAP-NEXT.md", "git diff --check", "所有核心阶段有证据，下一轮有明确约束和目标", "选择框架架构或性能专项"),
        ],
    },
]


def build_plan() -> list[dict[str, object]]:
    plan: list[dict[str, object]] = []
    day = 1
    for phase in PHASES:
        for index, item in enumerate(phase["tasks"], start=1):
            plan.append(
                {
                    "day": day,
                    "phase_id": phase["id"],
                    "phase": phase["name"],
                    "project": phase["project"],
                    "objective": phase["objective"],
                    "phase_day": index,
                    "phase_total_days": len(phase["tasks"]),
                    "week": (index - 1) // 7 + 1,
                    **item,
                }
            )
            day += 1
    return plan


def write_outputs(plan: list[dict[str, object]]) -> None:
    (ROOT / "daily-plan.json").write_text(
        json.dumps({"core_days": len(plan), "session_minutes": 90, "days": plan}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# 逐日学习计划",
        "",
        "每天默认 90 分钟：10 分钟理解主题，50 分钟写脚本或工程改进，20 分钟运行并保存证据，10 分钟复盘和提交。",
        "",
        "每天必须留下：可运行脚本或阻塞复现、运行证据、学习记录、Git 提交。性能测试只对本地或明确授权环境执行。",
        "",
    ]
    current_phase = ""
    for item in plan:
        if item["phase"] != current_phase:
            current_phase = str(item["phase"])
            lines.extend([f"## {current_phase}", ""])
        lines.extend(
            [
                f"### Day {item['day']}：{item['title']}",
                f"- 学习重点：{item['learn']}",
                f"- 今日产出：{item['deliverable']}",
                f"- 目标文件：`{item['file']}`",
                f"- 运行命令：`{item['run']}`",
                f"- 完成标准：{item['done']}",
                f"- 可选挑战：{item['stretch']}",
                "",
            ]
        )
    (ROOT / "DAILY-PLAN.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    plan = build_plan()
    if len(plan) != 182:
        raise SystemExit(f"expected 182 detailed core days; got {len(plan)} days")
    write_outputs(plan)
    print(f"generated {len(plan)} daily plans")
