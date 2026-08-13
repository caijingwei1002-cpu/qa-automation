# 逐日学习计划

每天默认 90 分钟：10 分钟理解主题，50 分钟写脚本或工程改进，20 分钟运行并保存证据，10 分钟复盘和提交。

每天必须留下：可运行脚本或阻塞复现、运行证据、学习记录、Git 提交。性能测试只对本地或明确授权环境执行。

## TodoMVC UI 基础

### Day 1：环境与首个 UI 测试
- 学习重点：理解 Playwright、pytest、浏览器和断言的职责
- 今日产出：初始化项目并完成新增 Todo 测试
- 目标文件：`01-todomvc-ui/tests/test_todos.py`
- 运行命令：`pytest 01-todomvc-ui/tests/test_todos.py::test_add_todo -q`
- 完成标准：输入 Todo 后，列表文本和未完成计数断言通过
- 可选挑战：保存首个失败截图

### Day 2：完成状态
- 学习重点：掌握 checkbox 交互与状态断言
- 今日产出：完成一个 Todo 并验证 completed 状态
- 目标文件：`01-todomvc-ui/tests/test_todos.py`
- 运行命令：`pytest 01-todomvc-ui/tests/test_todos.py::test_complete_todo -q`
- 完成标准：复选框、样式状态和计数变化均被断言
- 可选挑战：增加取消完成场景

### Day 3：删除行为
- 学习重点：理解操作后的 DOM 与业务状态校验
- 今日产出：新增删除 Todo 测试
- 目标文件：`01-todomvc-ui/tests/test_todos.py`
- 运行命令：`pytest 01-todomvc-ui/tests/test_todos.py::test_delete_todo -q`
- 完成标准：目标项消失且剩余项目不受影响
- 可选挑战：验证最后一项删除后页脚消失

### Day 4：筛选功能
- 学习重点：掌握可见性和集合断言
- 今日产出：覆盖 All、Active、Completed 三种筛选
- 目标文件：`01-todomvc-ui/tests/test_filters.py`
- 运行命令：`pytest 01-todomvc-ui/tests/test_filters.py -q`
- 完成标准：每种筛选只展示正确状态的数据
- 可选挑战：验证刷新后的筛选状态

### Day 5：边界输入
- 学习重点：学习等价类和边界值
- 今日产出：覆盖空白、前后空格、重复文本和长文本
- 目标文件：`01-todomvc-ui/tests/test_input_validation.py`
- 运行命令：`pytest 01-todomvc-ui/tests/test_input_validation.py -q`
- 完成标准：至少四组边界数据有明确预期与断言
- 可选挑战：增加 Unicode 和 emoji 输入

### Day 6：参数化
- 学习重点：掌握 pytest.mark.parametrize
- 今日产出：把多组 Todo 输入改为参数化测试
- 目标文件：`01-todomvc-ui/tests/test_todo_data.py`
- 运行命令：`pytest 01-todomvc-ui/tests/test_todo_data.py -q`
- 完成标准：一份测试函数稳定运行多组数据
- 可选挑战：为失败数据增加可读 id

### Day 7：Fixture
- 学习重点：理解测试前置、后置和隔离
- 今日产出：用 fixture 统一打开页面和准备数据
- 目标文件：`01-todomvc-ui/tests/conftest.py`
- 运行命令：`pytest 01-todomvc-ui/tests -q`
- 完成标准：测试之间互不污染且公共准备代码减少
- 可选挑战：增加 browser context fixture

### Day 8：稳定定位
- 学习重点：比较 role、label、text、CSS 定位
- 今日产出：重构脆弱定位器并写定位规则
- 目标文件：`01-todomvc-ui/tests/test_locators.py`
- 运行命令：`pytest 01-todomvc-ui/tests -q`
- 完成标准：关键定位优先使用语义定位且全套通过
- 可选挑战：故意改 DOM 验证定位韧性

### Day 9：自动等待
- 学习重点：理解自动等待与显式等待边界
- 今日产出：移除固定 sleep 并增加状态等待测试
- 目标文件：`01-todomvc-ui/tests/test_waiting.py`
- 运行命令：`pytest 01-todomvc-ui/tests/test_waiting.py -q`
- 完成标准：代码无固定 sleep，异步状态有可解释等待
- 可选挑战：模拟较慢交互

### Day 10：失败证据
- 学习重点：掌握 screenshot、trace、日志用途
- 今日产出：配置失败截图和 Trace 保留
- 目标文件：`01-todomvc-ui/conftest.py`
- 运行命令：`pytest 01-todomvc-ui/tests -q`
- 完成标准：制造一次失败后可找到截图或 Trace
- 可选挑战：记录如何打开 Trace

### Day 11：标记与套件
- 学习重点：学习 smoke、regression 标记策略
- 今日产出：标记并拆分冒烟与回归测试
- 目标文件：`01-todomvc-ui/pytest.ini`
- 运行命令：`pytest 01-todomvc-ui/tests -m smoke -q`
- 完成标准：smoke 只包含关键路径且可单独执行
- 可选挑战：添加 slow 标记

### Day 12：数据与辅助函数
- 学习重点：区分测试数据、动作和断言
- 今日产出：提取 Todo 数据工厂或辅助函数
- 目标文件：`01-todomvc-ui/tests/helpers.py`
- 运行命令：`pytest 01-todomvc-ui/tests -q`
- 完成标准：测试主体更短且断言仍保留在测试中
- 可选挑战：随机生成唯一文本

### Day 13：小型回归
- 学习重点：学习按风险选择回归范围
- 今日产出：执行完整回归并整理失败清单
- 目标文件：`01-todomvc-ui/tests/test_regression.py`
- 运行命令：`pytest 01-todomvc-ui/tests -q`
- 完成标准：全套结果可复现，失败有原因和证据
- 可选挑战：生成 JUnit XML

### Day 14：阶段验收
- 学习重点：总结 UI 自动化基础与局限
- 今日产出：独立新增 Clear completed 端到端测试并写阶段总结
- 目标文件：`01-todomvc-ui/tests/test_clear_completed.py`
- 运行命令：`pytest 01-todomvc-ui/tests -q`
- 完成标准：不看示例完成新场景，全套通过并写阶段复盘
- 可选挑战：说明三个最常见 flaky 来源

## SauceDemo UI 框架

### Day 15：项目初始化
- 学习重点：理解电商业务流和测试边界
- 今日产出：初始化 SauceDemo 项目并完成标准用户登录
- 目标文件：`02-saucedemo-ui/tests/test_login.py`
- 运行命令：`pytest 02-saucedemo-ui/tests/test_login.py::test_standard_user_login -q`
- 完成标准：登录后 URL 和商品页标题断言通过
- 可选挑战：保存登录页元素清单

### Day 16：登录异常
- 学习重点：学习负向场景与错误信息断言
- 今日产出：覆盖错误密码和空用户名
- 目标文件：`02-saucedemo-ui/tests/test_login.py`
- 运行命令：`pytest 02-saucedemo-ui/tests/test_login.py -q`
- 完成标准：错误类型对应正确提示且不会进入商品页
- 可选挑战：增加空密码

### Day 17：特殊用户
- 学习重点：理解测试账号代表的风险场景
- 今日产出：覆盖 locked_out_user 与 problem_user
- 目标文件：`02-saucedemo-ui/tests/test_users.py`
- 运行命令：`pytest 02-saucedemo-ui/tests/test_users.py -q`
- 完成标准：锁定用户行为正确，问题用户异常被记录
- 可选挑战：研究 performance_glitch_user

### Day 18：商品列表
- 学习重点：学习列表完整性与集合断言
- 今日产出：验证商品名称、价格、图片和数量
- 目标文件：`02-saucedemo-ui/tests/test_inventory.py`
- 运行命令：`pytest 02-saucedemo-ui/tests/test_inventory.py -q`
- 完成标准：列表数量与每项关键字段都有断言
- 可选挑战：校验价格格式

### Day 19：商品详情
- 学习重点：掌握列表到详情的导航验证
- 今日产出：验证进入详情和返回列表
- 目标文件：`02-saucedemo-ui/tests/test_product_detail.py`
- 运行命令：`pytest 02-saucedemo-ui/tests/test_product_detail.py -q`
- 完成标准：详情名称价格与列表一致
- 可选挑战：参数化多个商品

### Day 20：商品排序
- 学习重点：学习从页面提取数据并验证排序
- 今日产出：覆盖名称和价格四种排序
- 目标文件：`02-saucedemo-ui/tests/test_sorting.py`
- 运行命令：`pytest 02-saucedemo-ui/tests/test_sorting.py -q`
- 完成标准：提取值与排序期望完全一致
- 可选挑战：处理浮点价格

### Day 21：加入购物车
- 学习重点：理解跨页面状态断言
- 今日产出：加入单个商品并验证徽标和购物车内容
- 目标文件：`02-saucedemo-ui/tests/test_cart.py`
- 运行命令：`pytest 02-saucedemo-ui/tests/test_cart.py::test_add_one_item -q`
- 完成标准：徽标、名称和价格一致
- 可选挑战：从详情页添加

### Day 22：多商品购物车
- 学习重点：学习集合与合计准备
- 今日产出：加入多个商品并验证集合
- 目标文件：`02-saucedemo-ui/tests/test_cart.py`
- 运行命令：`pytest 02-saucedemo-ui/tests/test_cart.py -q`
- 完成标准：购物车集合与选择集合一致
- 可选挑战：验证展示顺序

### Day 23：移除商品
- 学习重点：掌握状态回退和幂等思路
- 今日产出：从列表和购物车分别移除商品
- 目标文件：`02-saucedemo-ui/tests/test_cart_remove.py`
- 运行命令：`pytest 02-saucedemo-ui/tests/test_cart_remove.py -q`
- 完成标准：徽标和购物车内容同步变化
- 可选挑战：移除全部商品

### Day 24：结算校验
- 学习重点：学习表单验证与字段组合
- 今日产出：覆盖姓名、姓氏、邮编必填错误
- 目标文件：`02-saucedemo-ui/tests/test_checkout_validation.py`
- 运行命令：`pytest 02-saucedemo-ui/tests/test_checkout_validation.py -q`
- 完成标准：每个缺失字段对应正确提示
- 可选挑战：增加特殊字符

### Day 25：结算概览
- 学习重点：学习金额与业务计算断言
- 今日产出：验证商品小计、税费和总价
- 目标文件：`02-saucedemo-ui/tests/test_checkout_summary.py`
- 运行命令：`pytest 02-saucedemo-ui/tests/test_checkout_summary.py -q`
- 完成标准：总价等于商品小计加税费
- 可选挑战：使用 Decimal 计算

### Day 26：完整下单
- 学习重点：建立关键端到端业务流
- 今日产出：完成登录到订单成功的 E2E 测试
- 目标文件：`02-saucedemo-ui/tests/test_checkout_e2e.py`
- 运行命令：`pytest 02-saucedemo-ui/tests/test_checkout_e2e.py -q`
- 完成标准：订单完成标题和购物车状态正确
- 可选挑战：测试取消结算

### Day 27：登出和会话
- 学习重点：理解认证状态和直接访问
- 今日产出：验证登出后不能直接进入商品页
- 目标文件：`02-saucedemo-ui/tests/test_session.py`
- 运行命令：`pytest 02-saucedemo-ui/tests/test_session.py -q`
- 完成标准：登出清理会话且受保护页面不可访问
- 可选挑战：刷新页面验证会话

### Day 28：Page Object 登录页
- 学习重点：理解页面对象职责边界
- 今日产出：创建 LoginPage 并重构登录测试
- 目标文件：`02-saucedemo-ui/pages/login_page.py`
- 运行命令：`pytest 02-saucedemo-ui/tests/test_login.py -q`
- 完成标准：定位和动作进入页面类，业务断言仍清晰
- 可选挑战：增加组件对象

### Day 29：Page Object 商品页
- 学习重点：减少重复选择器和操作
- 今日产出：创建 InventoryPage 与 CartPage
- 目标文件：`02-saucedemo-ui/pages/inventory_page.py`
- 运行命令：`pytest 02-saucedemo-ui/tests/test_inventory.py 02-saucedemo-ui/tests/test_cart.py -q`
- 完成标准：相关测试无重复关键定位器
- 可选挑战：增加按商品名操作

### Day 30：结算页面对象
- 学习重点：组织多页面业务流程
- 今日产出：创建 Checkout 页面对象并重构 E2E
- 目标文件：`02-saucedemo-ui/pages/checkout_page.py`
- 运行命令：`pytest 02-saucedemo-ui/tests/test_checkout_e2e.py -q`
- 完成标准：E2E 测试读起来像业务步骤
- 可选挑战：避免万能 BasePage

### Day 31：测试数据模型
- 学习重点：学习账号和商品数据管理
- 今日产出：集中管理用户、地址和商品数据
- 目标文件：`02-saucedemo-ui/test_data.py`
- 运行命令：`pytest 02-saucedemo-ui/tests -q`
- 完成标准：变化数据不散落在测试中
- 可选挑战：使用 dataclass

### Day 32：环境配置
- 学习重点：掌握 base_url 和环境切换
- 今日产出：加入 test 配置与命令行选项
- 目标文件：`02-saucedemo-ui/config.py`
- 运行命令：`pytest 02-saucedemo-ui/tests -m smoke -q`
- 完成标准：base_url 不硬编码且错误配置明确失败
- 可选挑战：增加 .env.example

### Day 33：多浏览器
- 学习重点：理解兼容性矩阵和执行成本
- 今日产出：在 Chromium、Firefox 运行 smoke
- 目标文件：`02-saucedemo-ui/pytest.ini`
- 运行命令：`pytest 02-saucedemo-ui/tests -m smoke -q`
- 完成标准：两种浏览器结果被记录
- 可选挑战：增加移动视口

### Day 34：报告与 flaky 分析
- 学习重点：区分产品缺陷、脚本缺陷和环境问题
- 今日产出：接入 HTML/Allure 报告并分析一次失败
- 目标文件：`02-saucedemo-ui/README.md`
- 运行命令：`pytest 02-saucedemo-ui/tests -q`
- 完成标准：报告包含步骤、失败证据和分类结论
- 可选挑战：统计最慢测试

### Day 35：阶段验收
- 学习重点：验证框架可维护性和独立开发能力
- 今日产出：独立新增跨页面回归场景并写架构说明
- 目标文件：`02-saucedemo-ui/tests/test_portfolio_scenario.py`
- 运行命令：`pytest 02-saucedemo-ui/tests -q`
- 完成标准：全套可运行、README 清楚、能解释 Page Object 取舍
- 可选挑战：写五分钟演示脚本

## Restful Booker API

### Day 36：HTTP 与健康检查
- 学习重点：理解请求、响应、状态码和超时
- 今日产出：初始化 API 项目并验证健康检查
- 目标文件：`03-restful-booker-api/tests/test_health.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_health.py -q`
- 完成标准：状态码、响应体和超时都有断言
- 可选挑战：记录响应头

### Day 37：查询列表
- 学习重点：掌握 GET 与集合响应
- 今日产出：查询 booking IDs 并校验结构
- 目标文件：`03-restful-booker-api/tests/test_get_bookings.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_get_bookings.py -q`
- 完成标准：列表类型和 bookingid 字段被校验
- 可选挑战：按姓名过滤

### Day 38：创建预订
- 学习重点：掌握 POST 与 JSON 请求体
- 今日产出：创建预订并断言完整返回
- 目标文件：`03-restful-booker-api/tests/test_create_booking.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_create_booking.py -q`
- 完成标准：id 存在且所有业务字段一致
- 可选挑战：保存响应样例

### Day 39：查询单条
- 学习重点：学习动态 ID 的接口关联
- 今日产出：创建后按 id 查询并比较数据
- 目标文件：`03-restful-booker-api/tests/test_booking_flow.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_booking_flow.py -q`
- 完成标准：创建与查询结果一致
- 可选挑战：验证不存在 id

### Day 40：过滤查询
- 学习重点：学习 query 参数和组合
- 今日产出：覆盖姓名和日期过滤
- 目标文件：`03-restful-booker-api/tests/test_filters.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_filters.py -q`
- 完成标准：每种过滤返回符合条件的数据
- 可选挑战：组合多个参数

### Day 41：Token 鉴权
- 学习重点：理解认证接口和凭据管理
- 今日产出：获取 Token 并验证无效凭据
- 目标文件：`03-restful-booker-api/tests/test_auth.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_auth.py -q`
- 完成标准：成功 Token 与失败原因都有断言
- 可选挑战：Token 不打印到日志

### Day 42：完整更新 PUT
- 学习重点：理解资源替换和认证头
- 今日产出：创建后完整更新预订
- 目标文件：`03-restful-booker-api/tests/test_update_booking.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_update_booking.py -q`
- 完成标准：更新响应和二次查询一致
- 可选挑战：验证无 Token

### Day 43：部分更新 PATCH
- 学习重点：理解 PUT 与 PATCH 差异
- 今日产出：只修改价格和附加需求
- 目标文件：`03-restful-booker-api/tests/test_update_booking.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_update_booking.py -q`
- 完成标准：目标字段变化，其他字段保持
- 可选挑战：更新空字符串

### Day 44：删除与清理
- 学习重点：学习资源生命周期和清理保证
- 今日产出：删除预订并确认不能查询
- 目标文件：`03-restful-booker-api/tests/test_delete_booking.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_delete_booking.py -q`
- 完成标准：删除成功且后续查询返回预期状态
- 可选挑战：重复删除

### Day 45：API Client
- 学习重点：建立请求封装边界
- 今日产出：封装 base URL、超时、headers 和通用请求
- 目标文件：`03-restful-booker-api/src/api_client.py`
- 运行命令：`pytest 03-restful-booker-api/tests -q`
- 完成标准：测试不再重复拼接 URL，失败信息可读
- 可选挑战：增加响应日志

### Day 46：Booking Client
- 学习重点：学习领域客户端
- 今日产出：封装 booking CRUD 方法
- 目标文件：`03-restful-booker-api/src/booking_client.py`
- 运行命令：`pytest 03-restful-booker-api/tests -q`
- 完成标准：测试通过领域方法表达业务动作
- 可选挑战：保留原始 response

### Day 47：Fixture 生命周期
- 学习重点：掌握 yield fixture 清理
- 今日产出：创建 booking fixture 并自动删除
- 目标文件：`03-restful-booker-api/tests/conftest.py`
- 运行命令：`pytest 03-restful-booker-api/tests -q`
- 完成标准：测试失败时也执行清理
- 可选挑战：使用 session 级 Token

### Day 48：数据工厂
- 学习重点：建立唯一且可复用的数据
- 今日产出：创建 booking data factory
- 目标文件：`03-restful-booker-api/tests/factories.py`
- 运行命令：`pytest 03-restful-booker-api/tests -q`
- 完成标准：每次数据唯一且默认值可覆盖
- 可选挑战：使用 Faker 可选

### Day 49：参数化边界
- 学习重点：覆盖价格、日期和姓名边界
- 今日产出：为核心字段增加参数化测试
- 目标文件：`03-restful-booker-api/tests/test_boundaries.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_boundaries.py -q`
- 完成标准：至少六组边界有明确预期
- 可选挑战：加入超长文本

### Day 50：缺失字段
- 学习重点：学习 API 负向测试
- 今日产出：逐个删除必填字段并记录行为
- 目标文件：`03-restful-booker-api/tests/test_invalid_payloads.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_invalid_payloads.py -q`
- 完成标准：服务行为被断言，意外行为记为缺陷
- 可选挑战：测试空 JSON

### Day 51：类型错误
- 学习重点：验证契约的输入类型边界
- 今日产出：覆盖字符串价格、非法布尔和嵌套错误
- 目标文件：`03-restful-booker-api/tests/test_invalid_types.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_invalid_types.py -q`
- 完成标准：错误类型结果可重复且有缺陷记录
- 可选挑战：测试 null 值

### Day 52：状态码与错误模型
- 学习重点：统一负向场景断言
- 今日产出：提取错误响应断言辅助函数
- 目标文件：`03-restful-booker-api/tests/assertions.py`
- 运行命令：`pytest 03-restful-booker-api/tests -q`
- 完成标准：状态码和错误体断言一致且可读
- 可选挑战：禁止只断言非 200

### Day 53：JSON Schema
- 学习重点：掌握结构契约验证
- 今日产出：为创建和查询响应增加 Schema
- 目标文件：`03-restful-booker-api/schemas/booking.json`
- 运行命令：`pytest 03-restful-booker-api/tests -q`
- 完成标准：缺失字段或类型变化能导致失败
- 可选挑战：Schema 版本化

### Day 54：业务断言
- 学习重点：区分结构正确和业务正确
- 今日产出：增加日期顺序、价格范围等规则
- 目标文件：`03-restful-booker-api/tests/test_business_rules.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_business_rules.py -q`
- 完成标准：至少三条业务规则被验证
- 可选挑战：记录服务未校验规则

### Day 55：接口链路
- 学习重点：组织创建、查询、更新、删除流程
- 今日产出：实现完整生命周期测试
- 目标文件：`03-restful-booker-api/tests/test_booking_lifecycle.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_booking_lifecycle.py -q`
- 完成标准：链路每一步都有局部断言和清理
- 可选挑战：失败时打印当前 id

### Day 56：配置分层
- 学习重点：学习环境变量与默认值
- 今日产出：加入 base_url、timeout、credentials 配置
- 目标文件：`03-restful-booker-api/src/settings.py`
- 运行命令：`pytest 03-restful-booker-api/tests -m smoke -q`
- 完成标准：配置可覆盖且敏感信息不进仓库
- 可选挑战：增加配置校验

### Day 57：日志与诊断
- 学习重点：学习请求上下文和脱敏
- 今日产出：记录 method、URL、耗时和状态码
- 目标文件：`03-restful-booker-api/src/logging_config.py`
- 运行命令：`pytest 03-restful-booker-api/tests -q`
- 完成标准：失败日志足够定位且 Token 被脱敏
- 可选挑战：添加 correlation id

### Day 58：重试边界
- 学习重点：理解可重试与不可重试错误
- 今日产出：为幂等 GET 设计有限重试
- 目标文件：`03-restful-booker-api/src/retry.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_retry.py -q`
- 完成标准：只对明确瞬态错误重试并有次数上限
- 可选挑战：测试退避策略

### Day 59：并行隔离
- 学习重点：理解并行导致的数据碰撞
- 今日产出：用 xdist 并行运行唯一数据测试
- 目标文件：`03-restful-booker-api/tests/conftest.py`
- 运行命令：`pytest 03-restful-booker-api/tests -n 2 -q`
- 完成标准：并行运行无共享数据冲突
- 可选挑战：比较执行耗时

### Day 60：测试标记
- 学习重点：建立 smoke、regression、negative 分类
- 今日产出：标记并验证不同套件
- 目标文件：`03-restful-booker-api/pytest.ini`
- 运行命令：`pytest 03-restful-booker-api/tests -m smoke -q`
- 完成标准：套件边界清晰且无 marker 警告
- 可选挑战：生成 marker 清单

### Day 61：报告
- 学习重点：把接口证据组织成可阅读报告
- 今日产出：接入 JUnit/Allure 并附加请求摘要
- 目标文件：`03-restful-booker-api/README.md`
- 运行命令：`pytest 03-restful-booker-api/tests -q --junitxml=reports/api.xml`
- 完成标准：报告可定位失败接口和数据
- 可选挑战：统计错误类型

### Day 62：缺陷案例
- 学习重点：训练高质量 Bug 表达
- 今日产出：基于异常行为写一份缺陷报告
- 目标文件：`03-restful-booker-api/reports/defect-001.md`
- 运行命令：`pytest 03-restful-booker-api/tests/test_invalid_payloads.py -q`
- 完成标准：包含复现、预期、实际、证据和影响
- 可选挑战：补充最小 curl

### Day 63：阶段验收
- 学习重点：验证独立设计 API 自动化能力
- 今日产出：独立新增一个资源链路并完成阶段报告
- 目标文件：`03-restful-booker-api/reports/phase-review.md`
- 运行命令：`pytest 03-restful-booker-api/tests -q`
- 完成标准：框架全套通过或失败可解释，文档可一键运行
- 可选挑战：绘制 API 测试架构图

## Swagger Petstore API 与性能入口

### Day 64：本地 Petstore
- 学习重点：理解压测授权边界与本地环境
- 今日产出：用 Docker 启动 Petstore 并完成健康检查
- 目标文件：`04-petstore-performance/docker-compose.yml`
- 运行命令：`docker compose -f 04-petstore-performance/docker-compose.yml up -d`
- 完成标准：本地服务可访问且记录版本和端口
- 可选挑战：保存容器资源基线

### Day 65：OpenAPI 阅读
- 学习重点：学习从规范提取测试范围
- 今日产出：列出 pet、store、user 核心接口和字段
- 目标文件：`04-petstore-performance/docs/api-inventory.md`
- 运行命令：`git diff --check`
- 完成标准：接口清单包含方法、路径、鉴权和风险
- 可选挑战：标注性能热点

### Day 66：查询契约
- 学习重点：建立 API 契约回归
- 今日产出：为 GET pet 增加 Schema 和错误场景
- 目标文件：`04-petstore-performance/tests/test_get_pet.py`
- 运行命令：`pytest 04-petstore-performance/tests/test_get_pet.py -q`
- 完成标准：成功与不存在场景都有契约断言
- 可选挑战：检查 content-type

### Day 67：CRUD 链路
- 学习重点：准备性能测试前的功能基线
- 今日产出：实现 pet 创建、查询、修改、删除
- 目标文件：`04-petstore-performance/tests/test_pet_lifecycle.py`
- 运行命令：`pytest 04-petstore-performance/tests/test_pet_lifecycle.py -q`
- 完成标准：链路可重复且数据可清理
- 可选挑战：加入唯一 id

### Day 68：契约漂移
- 学习重点：理解 OpenAPI 与实现差异
- 今日产出：写脚本比较关键响应与规范
- 目标文件：`04-petstore-performance/tests/test_contract.py`
- 运行命令：`pytest 04-petstore-performance/tests/test_contract.py -q`
- 完成标准：至少覆盖两个接口并记录差异
- 可选挑战：输出差异报告

### Day 69：k6 首脚本
- 学习重点：理解 VU、iteration、duration
- 今日产出：编写单用户查询冒烟脚本
- 目标文件：`04-petstore-performance/k6/smoke.js`
- 运行命令：`k6 run 04-petstore-performance/k6/smoke.js`
- 完成标准：请求成功且 check、指标可读
- 可选挑战：加入自定义 Trend

### Day 70：性能断言
- 学习重点：学习 check 与 threshold 区别
- 今日产出：设置错误率和 p95 阈值
- 目标文件：`04-petstore-performance/k6/thresholds.js`
- 运行命令：`k6 run 04-petstore-performance/k6/thresholds.js`
- 完成标准：阈值通过，故意收紧时能失败
- 可选挑战：加入 p99

### Day 71：测试数据
- 学习重点：避免压测数据竞争
- 今日产出：编写 setup/teardown 生成和清理 pet
- 目标文件：`04-petstore-performance/k6/data_setup.js`
- 运行命令：`k6 run 04-petstore-performance/k6/data_setup.js`
- 完成标准：数据唯一且结束后可清理
- 可选挑战：从 JSON 加载数据

### Day 72：场景建模
- 学习重点：把真实业务比例映射到脚本
- 今日产出：设计读写比例和用户停顿
- 目标文件：`04-petstore-performance/docs/workload-model.md`
- 运行命令：`git diff --check`
- 完成标准：文档解释 VU、持续时间和业务比例
- 可选挑战：使用 scenarios executor

### Day 73：阶梯负载
- 学习重点：观察响应随负载变化
- 今日产出：实现 5→10→20 VU 负载脚本
- 目标文件：`04-petstore-performance/k6/load.js`
- 运行命令：`k6 run 04-petstore-performance/k6/load.js`
- 完成标准：记录各阶段吞吐、错误率和 p95
- 可选挑战：输出 JSON summary

### Day 74：基线报告
- 学习重点：学习可比较的性能基线
- 今日产出：执行固定负载并填写基线报告
- 目标文件：`04-petstore-performance/reports/baseline.md`
- 运行命令：`k6 run --summary-export=artifacts/baseline.json 04-petstore-performance/k6/load.js`
- 完成标准：报告包含环境、负载、指标和结论
- 可选挑战：重复三次比较波动

### Day 75：资源监控
- 学习重点：关联应用指标与请求指标
- 今日产出：记录容器 CPU、内存和网络
- 目标文件：`04-petstore-performance/docs/monitoring.md`
- 运行命令：`docker stats --no-stream`
- 完成标准：同一时间窗口有 k6 与资源证据
- 可选挑战：加入数据库连接

### Day 76：压力测试
- 学习重点：寻找性能拐点而非只压垮
- 今日产出：逐级增加 VU 直到阈值持续恶化
- 目标文件：`04-petstore-performance/k6/stress.js`
- 运行命令：`k6 run 04-petstore-performance/k6/stress.js`
- 完成标准：记录首个明显拐点和停止条件
- 可选挑战：比较读写瓶颈

### Day 77：峰值测试
- 学习重点：理解突发流量与恢复
- 今日产出：实现低负载瞬间升高再回落
- 目标文件：`04-petstore-performance/k6/spike.js`
- 运行命令：`k6 run 04-petstore-performance/k6/spike.js`
- 完成标准：记录峰值错误和恢复时间
- 可选挑战：修改峰值持续时间

### Day 78：稳定性测试
- 学习重点：识别资源泄漏和累积问题
- 今日产出：实现受控的 soak 脚本
- 目标文件：`04-petstore-performance/k6/soak.js`
- 运行命令：`k6 run 04-petstore-performance/k6/soak.js`
- 完成标准：趋势无持续恶化或有明确证据
- 可选挑战：按机器能力缩短预演

### Day 79：容量分析
- 学习重点：学习安全容量与极限容量区别
- 今日产出：根据负载曲线计算建议并发
- 目标文件：`04-petstore-performance/reports/capacity.md`
- 运行命令：`python 04-petstore-performance/tools/analyze_results.py`
- 完成标准：给出容量区间、依据和安全余量
- 可选挑战：画 VU-p95 曲线

### Day 80：瓶颈假设
- 学习重点：用证据建立可验证假设
- 今日产出：选择最慢接口分析可能原因
- 目标文件：`04-petstore-performance/reports/bottleneck.md`
- 运行命令：`k6 run 04-petstore-performance/k6/focused.js`
- 完成标准：假设引用请求和资源指标
- 可选挑战：设计 A/B 验证

### Day 81：参数与环境
- 学习重点：让性能脚本可复用
- 今日产出：支持 BASE_URL、VUS、DURATION 环境变量
- 目标文件：`04-petstore-performance/k6/configurable.js`
- 运行命令：`k6 run -e VUS=5 -e DURATION=30s 04-petstore-performance/k6/configurable.js`
- 完成标准：配置有默认值且输出实际参数
- 可选挑战：防止误指向生产域名

### Day 82：CI 性能冒烟
- 学习重点：学习性能质量门禁边界
- 今日产出：加入短时 k6 smoke CI 配置
- 目标文件：`04-petstore-performance/.github/workflows/performance-smoke.yml`
- 运行命令：`k6 run 04-petstore-performance/k6/smoke.js`
- 完成标准：CI 场景短、稳定且阈值明确
- 可选挑战：保存 summary artifact

### Day 83：性能报告
- 学习重点：形成可读的非功能测试结论
- 今日产出：完成包含图表、瓶颈和建议的报告
- 目标文件：`04-petstore-performance/reports/performance-report.md`
- 运行命令：`git diff --check`
- 完成标准：报告能回答容量、拐点、错误率和风险
- 可选挑战：补充执行限制

### Day 84：阶段验收
- 学习重点：验证独立设计性能测试能力
- 今日产出：从目标到报告独立完成一次受控测试
- 目标文件：`04-petstore-performance/reports/phase-review.md`
- 运行命令：`k6 run 04-petstore-performance/k6/smoke.js`
- 完成标准：脚本、阈值、证据、报告齐全且未测试公共服务
- 可选挑战：五分钟讲解容量结论

## 测试工程化

### Day 85：配置模型
- 学习重点：学习环境配置分层
- 今日产出：实现默认值、环境变量和校验
- 目标文件：`03-restful-booker-api/src/settings.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_settings.py -q`
- 完成标准：缺失必需配置时快速失败且敏感值不提交
- 可选挑战：支持多个环境

### Day 86：依赖锁定
- 学习重点：理解可复现环境
- 今日产出：整理 pyproject 或 requirements 与锁定策略
- 目标文件：`03-restful-booker-api/pyproject.toml`
- 运行命令：`python -m pip check`
- 完成标准：依赖声明可安装且无冲突
- 可选挑战：加入开发依赖组

### Day 87：Docker 化测试
- 学习重点：学习容器化测试运行器
- 今日产出：创建自动化测试 Dockerfile
- 目标文件：`03-restful-booker-api/Dockerfile`
- 运行命令：`docker build -t qa-api-tests 03-restful-booker-api`
- 完成标准：镜像构建成功且入口明确
- 可选挑战：使用非 root 用户

### Day 88：Compose 环境
- 学习重点：编排被测服务与测试
- 今日产出：创建测试环境 compose 文件
- 目标文件：`03-restful-booker-api/docker-compose.yml`
- 运行命令：`docker compose -f 03-restful-booker-api/docker-compose.yml config`
- 完成标准：配置解析成功且服务依赖清晰
- 可选挑战：加入 healthcheck

### Day 89：环境就绪检查
- 学习重点：避免服务未启动导致假失败
- 今日产出：实现轮询健康检查和超时
- 目标文件：`03-restful-booker-api/tools/wait_for_service.py`
- 运行命令：`python 03-restful-booker-api/tools/wait_for_service.py`
- 完成标准：可区分就绪、超时和连接错误
- 可选挑战：加入指数退避

### Day 90：数据库连接
- 学习重点：理解 API 与数据层校验边界
- 今日产出：封装只读数据库连接 fixture
- 目标文件：`03-restful-booker-api/src/db_client.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_db_connection.py -q`
- 完成标准：连接可关闭且查询参数化
- 可选挑战：连接池

### Day 91：数据库断言
- 学习重点：学习何时需要跨层校验
- 今日产出：创建预订后验证关键数据库字段
- 目标文件：`03-restful-booker-api/tests/test_booking_db.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_booking_db.py -q`
- 完成标准：API 与 DB 关键字段一致
- 可选挑战：验证删除

### Day 92：数据清理
- 学习重点：建立可靠 teardown
- 今日产出：实现带前缀的测试数据清理工具
- 目标文件：`03-restful-booker-api/tools/cleanup_test_data.py`
- 运行命令：`python 03-restful-booker-api/tools/cleanup_test_data.py --dry-run`
- 完成标准：默认 dry-run，只清理明确测试数据
- 可选挑战：输出清理报告

### Day 93：数据工厂进阶
- 学习重点：生成可控且可复现的数据
- 今日产出：支持 seed 和场景化 builder
- 目标文件：`03-restful-booker-api/tests/factories.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_factories.py -q`
- 完成标准：同 seed 可复现且字段可覆盖
- 可选挑战：增加非法数据 builder

### Day 94：日志结构化
- 学习重点：提高 CI 失败诊断效率
- 今日产出：输出 JSON 或键值日志并脱敏
- 目标文件：`03-restful-booker-api/src/logging_config.py`
- 运行命令：`pytest 03-restful-booker-api/tests -m smoke -q`
- 完成标准：日志含 test、method、status、duration
- 可选挑战：增加 trace id

### Day 95：自定义断言
- 学习重点：提升失败信息质量
- 今日产出：封装字段、Schema、业务断言
- 目标文件：`03-restful-booker-api/tests/assertions.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_assertions.py -q`
- 完成标准：失败信息显示期望、实际和上下文
- 可选挑战：支持软断言讨论

### Day 96：Allure 步骤
- 学习重点：让报告表达业务链路
- 今日产出：为 API client 和生命周期增加步骤
- 目标文件：`03-restful-booker-api/tests/test_booking_lifecycle.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_booking_lifecycle.py --alluredir=allure-results`
- 完成标准：报告步骤清楚且附件脱敏
- 可选挑战：附加响应摘要

### Day 97：报告历史
- 学习重点：观察趋势而非单次结果
- 今日产出：保存测试历史和趋势说明
- 目标文件：`03-restful-booker-api/reports/README.md`
- 运行命令：`pytest 03-restful-booker-api/tests --junitxml=reports/latest.xml`
- 完成标准：报告路径稳定且历史策略明确
- 可选挑战：制作趋势脚本

### Day 98：Marker 规范
- 学习重点：建立团队可理解的分类
- 今日产出：定义 smoke、regression、negative、db
- 目标文件：`03-restful-booker-api/pytest.ini`
- 运行命令：`pytest 03-restful-booker-api/tests --markers`
- 完成标准：无未知 marker 且分类说明清楚
- 可选挑战：增加 owner 标记

### Day 99：选择性执行
- 学习重点：根据变更范围运行测试
- 今日产出：编写按标签和路径的运行脚本
- 目标文件：`03-restful-booker-api/tools/run_tests.ps1`
- 运行命令：`powershell -File 03-restful-booker-api/tools/run_tests.ps1 -Suite smoke`
- 完成标准：参数错误会快速失败
- 可选挑战：增加 dry-run

### Day 100：并行基线
- 学习重点：量化并行收益和风险
- 今日产出：比较串行与 2 workers 执行
- 目标文件：`03-restful-booker-api/reports/parallel.md`
- 运行命令：`pytest 03-restful-booker-api/tests -n 2 -q`
- 完成标准：记录耗时、失败和资源差异
- 可选挑战：测试 4 workers

### Day 101：flaky 识别
- 学习重点：学习重复执行诊断
- 今日产出：重复运行疑似不稳定测试并统计
- 目标文件：`03-restful-booker-api/tools/repeat_test.py`
- 运行命令：`python 03-restful-booker-api/tools/repeat_test.py`
- 完成标准：结果显示运行次数、失败次数和种子
- 可选挑战：不要自动忽略失败

### Day 102：重试策略
- 学习重点：限制重试范围并保留首次失败
- 今日产出：为明确瞬态场景配置一次重试
- 目标文件：`03-restful-booker-api/docs/retry-policy.md`
- 运行命令：`pytest 03-restful-booker-api/tests -m transient -q`
- 完成标准：文档说明哪些可重试、哪些禁止
- 可选挑战：验证首次失败证据

### Day 103：超时治理
- 学习重点：防止测试无限等待
- 今日产出：为 HTTP、fixture、CI 设置分层超时
- 目标文件：`03-restful-booker-api/pyproject.toml`
- 运行命令：`pytest 03-restful-booker-api/tests -m smoke -q`
- 完成标准：超时有明确错误且值有依据
- 可选挑战：记录慢测试

### Day 104：GitHub Actions 基础
- 学习重点：建立自动执行
- 今日产出：创建 pull request smoke workflow
- 目标文件：`03-restful-booker-api/.github/workflows/api-smoke.yml`
- 运行命令：`pytest 03-restful-booker-api/tests -m smoke -q`
- 完成标准：workflow 含安装、执行和报告上传
- 可选挑战：加入依赖缓存

### Day 105：回归流水线
- 学习重点：区分快速反馈和完整回归
- 今日产出：创建 nightly/full regression workflow
- 目标文件：`03-restful-booker-api/.github/workflows/api-regression.yml`
- 运行命令：`pytest 03-restful-booker-api/tests -m regression -q`
- 完成标准：smoke 与 regression 时机和超时不同
- 可选挑战：增加手动触发参数

### Day 106：质量门禁
- 学习重点：把通过标准写成规则
- 今日产出：设置测试、覆盖率或失败率门禁
- 目标文件：`03-restful-booker-api/docs/quality-gates.md`
- 运行命令：`pytest 03-restful-booker-api/tests -q`
- 完成标准：规则可衡量且失败时阻止流水线
- 可选挑战：区分警告指标

### Day 107：测试覆盖映射
- 学习重点：连接需求、风险和自动化
- 今日产出：创建需求-用例-脚本追踪表
- 目标文件：`03-restful-booker-api/docs/traceability.md`
- 运行命令：`pytest 03-restful-booker-api/tests --collect-only -q`
- 完成标准：关键需求均有脚本或风险说明
- 可选挑战：自动生成收集清单

### Day 108：代码质量
- 学习重点：统一格式、lint 和类型检查
- 今日产出：配置 ruff 或等效工具
- 目标文件：`03-restful-booker-api/pyproject.toml`
- 运行命令：`ruff check 03-restful-booker-api`
- 完成标准：检查可执行且规则不过度噪声
- 可选挑战：加入 pre-commit

### Day 109：Secret 治理
- 学习重点：避免账号和 Token 泄漏
- 今日产出：增加 env 示例、忽略规则和脱敏测试
- 目标文件：`03-restful-booker-api/tests/test_secret_masking.py`
- 运行命令：`pytest 03-restful-booker-api/tests/test_secret_masking.py -q`
- 完成标准：日志与仓库不包含真实凭据
- 可选挑战：扫描测试产物

### Day 110：维护指南
- 学习重点：让别人能新增测试
- 今日产出：编写贡献、命名、fixture 和调试规范
- 目标文件：`03-restful-booker-api/CONTRIBUTING.md`
- 运行命令：`pytest 03-restful-booker-api/tests -m smoke -q`
- 完成标准：新成员按文档能运行并新增测试
- 可选挑战：加入 PR checklist

### Day 111：一键验证
- 学习重点：统一本地和 CI 入口
- 今日产出：创建 verify.ps1 执行格式、lint、smoke
- 目标文件：`03-restful-booker-api/tools/verify.ps1`
- 运行命令：`powershell -File 03-restful-booker-api/tools/verify.ps1`
- 完成标准：一个命令给出明确阶段结果
- 可选挑战：失败即停止

### Day 112：阶段验收
- 学习重点：评估工程是否可被团队持续使用
- 今日产出：从干净环境按 README 执行并写工程化报告
- 目标文件：`03-restful-booker-api/reports/engineering-review.md`
- 运行命令：`powershell -File 03-restful-booker-api/tools/verify.ps1`
- 完成标准：配置、环境、报告、CI、维护文档完整
- 可选挑战：列出三项技术债

## 高级质量专项

### Day 113：契约测试进阶
- 学习重点：理解消费者与提供者契约
- 今日产出：为一个 API 定义消费者期望
- 目标文件：`advanced-quality/contracts/consumer_contract.json`
- 运行命令：`pytest advanced-quality/contracts/test_contract.py -q`
- 完成标准：契约包含请求、响应和版本
- 可选挑战：比较 Schema 测试

### Day 114：契约破坏验证
- 学习重点：识别 breaking change
- 今日产出：制造字段删除并验证契约失败
- 目标文件：`advanced-quality/contracts/test_breaking_change.py`
- 运行命令：`pytest advanced-quality/contracts/test_breaking_change.py -q`
- 完成标准：破坏性变化能被测试捕获
- 可选挑战：定义兼容变化

### Day 115：Mock Server
- 学习重点：隔离不稳定下游
- 今日产出：创建本地 Mock 响应服务
- 目标文件：`advanced-quality/mocks/mock_server.py`
- 运行命令：`pytest advanced-quality/mocks/test_mock_server.py -q`
- 完成标准：正常、超时、5xx 可配置
- 可选挑战：记录请求

### Day 116：测试替身选择
- 学习重点：区分 stub、mock、fake
- 今日产出：为三个场景选择合适替身并实现一个
- 目标文件：`advanced-quality/mocks/README.md`
- 运行命令：`pytest advanced-quality/mocks -q`
- 完成标准：文档说明取舍且实现可运行
- 可选挑战：避免过度 Mock

### Day 117：异步轮询
- 学习重点：测试最终一致性
- 今日产出：实现带超时的状态轮询 helper
- 目标文件：`advanced-quality/async/wait_until.py`
- 运行命令：`pytest advanced-quality/async/test_wait_until.py -q`
- 完成标准：成功、超时、异常均有测试
- 可选挑战：加入退避

### Day 118：幂等与重复消费
- 学习重点：验证重复请求影响
- 今日产出：设计重复提交场景并断言副作用
- 目标文件：`advanced-quality/async/test_idempotency.py`
- 运行命令：`pytest advanced-quality/async/test_idempotency.py -q`
- 完成标准：重复操作不会产生意外重复数据或被记录为缺陷
- 可选挑战：并发重复提交

### Day 119：消息测试模型
- 学习重点：理解生产、消费和确认
- 今日产出：为模拟队列编写消息流程测试
- 目标文件：`advanced-quality/async/test_message_flow.py`
- 运行命令：`pytest advanced-quality/async/test_message_flow.py -q`
- 完成标准：覆盖成功、重试、死信概念
- 可选挑战：测试乱序消息

### Day 120：视觉基线
- 学习重点：理解截图比较和阈值
- 今日产出：创建稳定页面视觉基线
- 目标文件：`advanced-quality/visual/test_visual_baseline.py`
- 运行命令：`pytest advanced-quality/visual/test_visual_baseline.py -q`
- 完成标准：基线可复现且环境被记录
- 可选挑战：增加跨视口

### Day 121：动态区域处理
- 学习重点：降低视觉误报
- 今日产出：屏蔽时间、动画或随机内容
- 目标文件：`advanced-quality/visual/test_masking.py`
- 运行命令：`pytest advanced-quality/visual/test_masking.py -q`
- 完成标准：动态内容变化不导致误报，真实变化会失败
- 可选挑战：比较阈值

### Day 122：响应式布局
- 学习重点：覆盖桌面、平板、手机视口
- 今日产出：参数化三个视口的核心页面
- 目标文件：`advanced-quality/visual/test_responsive.py`
- 运行命令：`pytest advanced-quality/visual/test_responsive.py -q`
- 完成标准：无横向溢出且关键控件可见
- 可选挑战：测试设备像素比

### Day 123：键盘可访问性
- 学习重点：验证非鼠标操作
- 今日产出：覆盖 Tab、Enter、Escape 流程
- 目标文件：`advanced-quality/accessibility/test_keyboard.py`
- 运行命令：`pytest advanced-quality/accessibility/test_keyboard.py -q`
- 完成标准：焦点顺序和操作结果正确
- 可选挑战：检查 focus 可见

### Day 124：可访问性扫描
- 学习重点：学习自动扫描的边界
- 今日产出：接入 axe 或等效规则检查
- 目标文件：`advanced-quality/accessibility/test_axe.py`
- 运行命令：`pytest advanced-quality/accessibility/test_axe.py -q`
- 完成标准：严重违规被报告且有页面上下文
- 可选挑战：人工检查一项

### Day 125：语义与标签
- 学习重点：验证表单名称和错误关联
- 今日产出：覆盖 label、role、aria-describedby
- 目标文件：`advanced-quality/accessibility/test_semantics.py`
- 运行命令：`pytest advanced-quality/accessibility/test_semantics.py -q`
- 完成标准：关键控件有可访问名称，错误可关联
- 可选挑战：检查标题层级

### Day 126：移动端交互
- 学习重点：理解触摸和小屏风险
- 今日产出：验证移动视口下核心流程
- 目标文件：`advanced-quality/mobile/test_mobile_flow.py`
- 运行命令：`pytest advanced-quality/mobile/test_mobile_flow.py -q`
- 完成标准：关键按钮可点击且布局无阻断
- 可选挑战：测试横屏

### Day 127：慢网络
- 学习重点：测试等待和用户反馈
- 今日产出：模拟高延迟加载
- 目标文件：`advanced-quality/network/test_slow_network.py`
- 运行命令：`pytest advanced-quality/network/test_slow_network.py -q`
- 完成标准：加载态、超时或重试行为有断言
- 可选挑战：模拟图片加载失败

### Day 128：断网恢复
- 学习重点：验证网络切换后的恢复能力
- 今日产出：实现 offline 到 online 场景
- 目标文件：`advanced-quality/network/test_offline_recovery.py`
- 运行命令：`pytest advanced-quality/network/test_offline_recovery.py -q`
- 完成标准：离线提示正确，恢复后可继续
- 可选挑战：重复切换

### Day 129：服务 5xx
- 学习重点：验证错误处理与重试边界
- 今日产出：拦截 API 返回 500/503
- 目标文件：`advanced-quality/network/test_server_errors.py`
- 运行命令：`pytest advanced-quality/network/test_server_errors.py -q`
- 完成标准：用户提示和重试行为符合设计
- 可选挑战：增加 429 限流

### Day 130：认证边界
- 学习重点：覆盖未登录、过期和伪造凭据
- 今日产出：编写认证负向测试
- 目标文件：`advanced-quality/security/test_authentication.py`
- 运行命令：`pytest advanced-quality/security/test_authentication.py -q`
- 完成标准：三类无效凭据均不能访问
- 可选挑战：Token 日志脱敏

### Day 131：授权边界
- 学习重点：验证水平和垂直越权
- 今日产出：设计用户 A 访问用户 B 数据测试
- 目标文件：`advanced-quality/security/test_authorization.py`
- 运行命令：`pytest advanced-quality/security/test_authorization.py -q`
- 完成标准：未授权访问被拒绝且无数据泄漏
- 可选挑战：验证管理员边界

### Day 132：输入安全
- 学习重点：覆盖注入式和超长输入安全行为
- 今日产出：建立安全输入参数集
- 目标文件：`advanced-quality/security/test_input_handling.py`
- 运行命令：`pytest advanced-quality/security/test_input_handling.py -q`
- 完成标准：服务不崩溃且错误响应不泄漏内部信息
- 可选挑战：测试文件名输入

### Day 133：敏感信息
- 学习重点：检查响应、日志、报告泄漏
- 今日产出：扫描测试产物中的 Token/密码模式
- 目标文件：`advanced-quality/security/test_secret_leaks.py`
- 运行命令：`pytest advanced-quality/security/test_secret_leaks.py -q`
- 完成标准：示例秘密可检测，正常数据不误报
- 可选挑战：扫描截图文本

### Day 134：时间与时区
- 学习重点：验证边界日期和时区转换
- 今日产出：覆盖跨日、闰日、夏令时场景
- 目标文件：`advanced-quality/time/test_timezones.py`
- 运行命令：`pytest advanced-quality/time/test_timezones.py -q`
- 完成标准：固定时钟下结果可复现
- 可选挑战：测试过期时间

### Day 135：本地化
- 学习重点：测试多语言和字符集
- 今日产出：覆盖中文、英文、长文案和 RTL 风险
- 目标文件：`advanced-quality/i18n/test_localization.py`
- 运行命令：`pytest advanced-quality/i18n/test_localization.py -q`
- 完成标准：字符不乱码，布局关键元素可用
- 可选挑战：验证数字日期格式

### Day 136：文件上传
- 学习重点：验证类型、大小和错误处理
- 今日产出：测试允许、拒绝和边界文件
- 目标文件：`advanced-quality/files/test_upload.py`
- 运行命令：`pytest advanced-quality/files/test_upload.py -q`
- 完成标准：文件策略被断言且临时文件清理
- 可选挑战：测试同名文件

### Day 137：下载验证
- 学习重点：校验文件名、类型和内容
- 今日产出：实现下载并检查内容
- 目标文件：`advanced-quality/files/test_download.py`
- 运行命令：`pytest advanced-quality/files/test_download.py -q`
- 完成标准：下载文件存在、类型正确、内容可验证
- 可选挑战：测试并发下载

### Day 138：状态机测试
- 学习重点：用状态转换发现遗漏
- 今日产出：为订单或 Todo 建立状态机并测试
- 目标文件：`advanced-quality/state/test_state_machine.py`
- 运行命令：`pytest advanced-quality/state/test_state_machine.py -q`
- 完成标准：允许和禁止的转换均被覆盖
- 可选挑战：尝试属性测试

### Day 139：风险测试策略
- 学习重点：按风险分配自动化层级
- 今日产出：为四项目写风险与覆盖策略
- 目标文件：`advanced-quality/TEST-STRATEGY.md`
- 运行命令：`git diff --check`
- 完成标准：策略说明测什么、不测什么和原因
- 可选挑战：增加测试金字塔

### Day 140：阶段验收
- 学习重点：整合高级质量能力
- 今日产出：选择三项专项形成可运行质量套件
- 目标文件：`advanced-quality/reports/phase-review.md`
- 运行命令：`pytest advanced-quality -q`
- 完成标准：至少三类专项有脚本、证据和局限说明
- 可选挑战：做一次风险评审演示

## 生产质量与可靠性

### Day 141：监控基线
- 学习重点：理解 CPU、内存、连接池与错误率
- 今日产出：记录服务资源基线
- 目标文件：`04-petstore-performance/reliability/baseline.md`
- 运行命令：`docker stats --no-stream`
- 完成标准：同一时间窗口的资源基线可复现
- 可选挑战：记录磁盘和网络

### Day 142：请求指标
- 学习重点：理解吞吐、延迟和错误率关联
- 今日产出：整理 k6 指标采集脚本
- 目标文件：`04-petstore-performance/reliability/metrics.js`
- 运行命令：`k6 run 04-petstore-performance/reliability/metrics.js`
- 完成标准：关键指标按接口和场景区分
- 可选挑战：增加自定义业务指标

### Day 143：p95/p99 对比
- 学习重点：避免只看平均响应时间
- 今日产出：比较不同并发级别的尾延迟
- 目标文件：`04-petstore-performance/reliability/tail-latency.md`
- 运行命令：`k6 run 04-petstore-performance/k6/load.js`
- 完成标准：报告解释平均值与尾延迟差异
- 可选挑战：按接口分组

### Day 144：慢接口定位
- 学习重点：建立从指标到假设的路径
- 今日产出：选择最慢接口写瓶颈假设
- 目标文件：`04-petstore-performance/reliability/slow-endpoint.md`
- 运行命令：`k6 run 04-petstore-performance/k6/focused.js`
- 完成标准：假设引用请求和资源证据
- 可选挑战：设计 A/B 验证

### Day 145：30 分钟稳定性
- 学习重点：识别资源泄漏和累积问题
- 今日产出：执行受控 soak 测试
- 目标文件：`04-petstore-performance/k6/soak.js`
- 运行命令：`k6 run 04-petstore-performance/k6/soak.js`
- 完成标准：趋势无持续恶化或有明确证据
- 可选挑战：按机器能力缩短预演

### Day 146：恢复时间
- 学习重点：理解故障检测与恢复指标
- 今日产出：记录一次服务重启后的恢复时间
- 目标文件：`04-petstore-performance/reliability/recovery.md`
- 运行命令：`docker compose restart`
- 完成标准：恢复步骤、耗时和数据影响有记录
- 可选挑战：自动化健康检查

### Day 147：依赖故障
- 学习重点：理解下游故障对用户流的影响
- 今日产出：模拟依赖超时或 5xx
- 目标文件：`04-petstore-performance/reliability/dependency-failure.md`
- 运行命令：`pytest advanced-quality/network/test_server_errors.py -q`
- 完成标准：超时、错误提示和恢复路径有断言
- 可选挑战：验证降级

### Day 148：超时策略
- 学习重点：区分连接、读取和总超时
- 今日产出：为测试和服务列出超时策略
- 目标文件：`04-petstore-performance/reliability/timeouts.md`
- 运行命令：`git diff --check`
- 完成标准：每个超时有依据、上限和告警行为
- 可选挑战：测慢网络

### Day 149：重试风暴
- 学习重点：理解重试放大效应
- 今日产出：模拟重试并记录请求放大
- 目标文件：`04-petstore-performance/reliability/retry-storm.md`
- 运行命令：`k6 run 04-petstore-performance/k6/retry.js`
- 完成标准：能说明重试次数对吞吐和延迟的影响
- 可选挑战：加入抖动

### Day 150：限流
- 学习重点：理解保护系统的限流策略
- 今日产出：设计并验证 429 场景
- 目标文件：`04-petstore-performance/reliability/rate-limit.md`
- 运行命令：`k6 run 04-petstore-performance/k6/spike.js`
- 完成标准：限流阈值、用户提示和恢复有记录
- 可选挑战：区分客户端和服务端限流

### Day 151：峰值恢复
- 学习重点：观察突发流量后的恢复质量
- 今日产出：执行 spike 并记录恢复曲线
- 目标文件：`04-petstore-performance/reports/spike-recovery.md`
- 运行命令：`k6 run 04-petstore-performance/k6/spike.js`
- 完成标准：报告包含峰值、错误和恢复时间
- 可选挑战：增加两种峰值

### Day 152：容量拐点
- 学习重点：计算安全并发和极限并发
- 今日产出：更新容量曲线与建议
- 目标文件：`04-petstore-performance/reports/capacity.md`
- 运行命令：`python 04-petstore-performance/tools/analyze_results.py`
- 完成标准：建议包含依据、安全余量和限制
- 可选挑战：区分读写容量

### Day 153：SLO 草案
- 学习重点：把技术指标翻译成用户目标
- 今日产出：为核心接口写 SLI/SLO 草案
- 目标文件：`04-petstore-performance/reliability/slo.md`
- 运行命令：`git diff --check`
- 完成标准：指标、目标、窗口和排除项明确
- 可选挑战：加入错误预算

### Day 154：告警验证
- 学习重点：避免只配置不验证告警
- 今日产出：为错误率或 p95 写告警测试说明
- 目标文件：`04-petstore-performance/reliability/alert-test.md`
- 运行命令：`git diff --check`
- 完成标准：能说明如何触发、观察、恢复和关闭
- 可选挑战：模拟告警噪声

### Day 155：日志关联
- 学习重点：用 trace id 串起请求与错误
- 今日产出：为一次失败链路整理日志证据
- 目标文件：`04-petstore-performance/reliability/traceability.md`
- 运行命令：`pytest advanced-quality -q`
- 完成标准：从测试结果能定位到对应日志上下文
- 可选挑战：加入请求 id

### Day 156：数据一致性
- 学习重点：验证故障期间的数据状态
- 今日产出：设计中断后数据一致性检查
- 目标文件：`04-petstore-performance/reliability/data-consistency.py`
- 运行命令：`pytest 03-restful-booker-api/tests -q`
- 完成标准：中断、重试、恢复后的数据结论明确
- 可选挑战：重复执行

### Day 157：安全恢复
- 学习重点：考虑凭据和数据在恢复流程中的风险
- 今日产出：写恢复过程安全检查清单
- 目标文件：`04-petstore-performance/reliability/recovery-security.md`
- 运行命令：`git diff --check`
- 完成标准：清单覆盖秘密、权限、数据和日志
- 可选挑战：做一次演练

### Day 158：可靠性演练
- 学习重点：把故障注入变成可控实验
- 今日产出：设计一次本地故障演练方案
- 目标文件：`04-petstore-performance/reliability/experiment.md`
- 运行命令：`git diff --check`
- 完成标准：有假设、停止条件、观察指标和回滚步骤
- 可选挑战：执行小规模演练

### Day 159：性能回归
- 学习重点：理解基线变化与质量趋势
- 今日产出：将本轮性能结果与历史基线比较
- 目标文件：`04-petstore-performance/reports/performance-regression.md`
- 运行命令：`k6 run 04-petstore-performance/k6/smoke.js`
- 完成标准：报告说明指标变化、阈值判断和可能原因
- 可选挑战：加入自动趋势差异

### Day 160：完整性能复盘
- 学习重点：综合请求、资源和恢复证据
- 今日产出：完成一次可靠性报告
- 目标文件：`04-petstore-performance/reports/reliability-report.md`
- 运行命令：`git diff --check`
- 完成标准：报告有结论、证据、风险和后续动作
- 可选挑战：制作指标图

### Day 161：阶段验收
- 学习重点：评估从性能测试到生产质量的能力
- 今日产出：完成容量、稳定性和恢复三项验收
- 目标文件：`04-petstore-performance/reports/reliability-review.md`
- 运行命令：`k6 run 04-petstore-performance/k6/smoke.js`
- 完成标准：能讲清容量、瓶颈、恢复和限制
- 可选挑战：做十分钟演示

## 作品集与技术表达

### Day 162：项目 README
- 学习重点：学习让陌生人快速运行项目
- 今日产出：补齐根目录 README 和一键运行说明
- 目标文件：`README.md`
- 运行命令：`git diff --check`
- 完成标准：新用户能找到环境、命令和阶段入口
- 可选挑战：增加故障排查

### Day 163：架构图
- 学习重点：用图表达测试分层和数据流
- 今日产出：绘制 UI、API、性能和 CI 架构图
- 目标文件：`docs/test-architecture.md`
- 运行命令：`git diff --check`
- 完成标准：图中组件、依赖和证据流清晰
- 可选挑战：加入 Mermaid

### Day 164：测试策略
- 学习重点：从需求、风险到测试层级表达
- 今日产出：整理四项目总体测试策略
- 目标文件：`docs/test-strategy.md`
- 运行命令：`git diff --check`
- 完成标准：说明覆盖范围、优先级和不测项
- 可选挑战：增加风险矩阵

### Day 165：缺陷案例一
- 学习重点：训练高质量功能缺陷表达
- 今日产出：整理一个 UI 缺陷案例
- 目标文件：`reports/defect-ui.md`
- 运行命令：`git diff --check`
- 完成标准：复现、预期、实际、证据和影响完整
- 可选挑战：补充修复验证

### Day 166：缺陷案例二
- 学习重点：训练接口缺陷表达
- 今日产出：整理一个 API 缺陷案例
- 目标文件：`reports/defect-api.md`
- 运行命令：`git diff --check`
- 完成标准：请求、响应、环境和严重程度完整
- 可选挑战：补充最小 curl

### Day 167：性能案例
- 学习重点：训练性能问题叙述
- 今日产出：整理一次瓶颈定位案例
- 目标文件：`reports/defect-performance.md`
- 运行命令：`git diff --check`
- 完成标准：基线、负载、指标、假设和结论完整
- 可选挑战：增加优化前后对比

### Day 168：测试指标
- 学习重点：理解指标的价值和误用
- 今日产出：定义脚本数、通过率、flaky、p95 等指标
- 目标文件：`docs/quality-metrics.md`
- 运行命令：`git diff --check`
- 完成标准：每个指标有用途、计算和限制
- 可选挑战：增加趋势示例

### Day 169：报告截图
- 学习重点：选择能证明能力的证据
- 今日产出：整理测试报告、Trace 和性能图截图
- 目标文件：`docs/evidence-index.md`
- 运行命令：`git diff --check`
- 完成标准：每张图有上下文、日期和对应代码
- 可选挑战：生成缩略图索引

### Day 170：CI 展示
- 学习重点：理解流水线如何展示质量
- 今日产出：整理 smoke、regression、performance workflow
- 目标文件：`docs/ci-overview.md`
- 运行命令：`git diff --check`
- 完成标准：触发条件、门禁和产物清晰
- 可选挑战：补充失败流程

### Day 171：代码重构
- 学习重点：从学习代码提升工程质量
- 今日产出：选择一个重复最多的模块重构
- 目标文件：`refactor/README.md`
- 运行命令：`pytest -q`
- 完成标准：重构前后行为一致且重复减少
- 可选挑战：记录取舍

### Day 172：命名规范
- 学习重点：提高测试可读性
- 今日产出：统一测试、fixture、页面对象命名
- 目标文件：`docs/naming.md`
- 运行命令：`git diff --check`
- 完成标准：规范有正反例且已有代码至少改一处
- 可选挑战：增加 lint 规则

### Day 173：调试手册
- 学习重点：把个人经验变成可复用知识
- 今日产出：整理环境、定位、数据和性能排查手册
- 目标文件：`docs/debugging.md`
- 运行命令：`git diff --check`
- 完成标准：至少包含五类常见问题和命令
- 可选挑战：让别人按手册排障

### Day 174：学习总结
- 学习重点：识别能力变化而非只列工具
- 今日产出：写一份阶段能力矩阵
- 目标文件：`docs/skills-matrix.md`
- 运行命令：`git diff --check`
- 完成标准：能说明从基础到高级的能力证据
- 可选挑战：给每项能力打等级

### Day 175：五分钟演示
- 学习重点：训练技术方案口头表达
- 今日产出：写出五分钟项目演示脚本
- 目标文件：`docs/demo-script.md`
- 运行命令：`git diff --check`
- 完成标准：包含目标、架构、脚本、结果和下一步
- 可选挑战：实际计时演练

### Day 176：面试项目介绍
- 学习重点：把工程决策讲清楚
- 今日产出：准备项目介绍和常见追问答案
- 目标文件：`docs/interview-project.md`
- 运行命令：`git diff --check`
- 完成标准：能回答为什么选工具、如何处理 flaky 和性能
- 可选挑战：增加英文术语

### Day 177：测试设计题
- 学习重点：综合业务、风险和自动化
- 今日产出：为一个新功能写测试设计方案
- 目标文件：`docs/test-design-exercise.md`
- 运行命令：`git diff --check`
- 完成标准：包含场景、优先级、自动化层级和风险
- 可选挑战：加容量问题

### Day 178：贡献指南
- 学习重点：让仓库适合协作
- 今日产出：补充分支、提交、审查和报告规范
- 目标文件：`CONTRIBUTING.md`
- 运行命令：`git diff --check`
- 完成标准：新人可按文档完成第一次提交
- 可选挑战：增加 PR 模板

### Day 179：发布清单
- 学习重点：建立交付前质量检查
- 今日产出：写自动化测试项目发布 checklist
- 目标文件：`docs/release-checklist.md`
- 运行命令：`git diff --check`
- 完成标准：功能、性能、安全、文档和回滚都有检查
- 可选挑战：接入 CI

### Day 180：最终回归
- 学习重点：验证整理没有破坏已有成果
- 今日产出：运行各项目 smoke 和核心回归
- 目标文件：`reports/final-regression.md`
- 运行命令：`pytest -q`
- 完成标准：结果、失败和环境均有记录
- 可选挑战：并行运行

### Day 181：最终总结
- 学习重点：形成可展示的完整作品集
- 今日产出：完成项目总结、局限和下一轮路线
- 目标文件：`FINAL-REPORT.md`
- 运行命令：`git diff --check`
- 完成标准：报告能回答学了什么、做了什么、如何验证和下一步
- 可选挑战：制作 PDF/演示版本

### Day 182：阶段验收
- 学习重点：完成长期学习主线闭环
- 今日产出：提交最终作品集并规划下一个 28 天专项
- 目标文件：`ROADMAP-NEXT.md`
- 运行命令：`git diff --check`
- 完成标准：所有核心阶段有证据，下一轮有明确约束和目标
- 可选挑战：选择框架架构或性能专项
