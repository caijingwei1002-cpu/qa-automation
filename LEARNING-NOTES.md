# QA 自动化学习知识库

这是长期复习用的独立知识文档，集中记录每天学习的核心概念、它解决的问题、代码落地方式、常见误区和知识验收问题。

当天的执行细节仍记录在 daily-log/，测试输出、截图和其他客观证据仍保存到 artifacts/day-XXX/。

## 目录

- [学习方式](#学习方式)
- [Day 1：环境与首个 UI 测试](#day-1环境与首个-ui-测试)
- [Day 2：完成状态](#day-2完成状态)
- [Day 3：删除行为](#day-3删除行为)
- [Day 4：筛选功能](#day-4筛选功能)
- [Day 5：边界输入](#day-5边界输入)
- [Day 6：参数化](#day-6参数化)
- [Day 7：Fixture](#day-7fixture)
- [Day 8：稳定定位](#day-8稳定定位)
- [Day 9：自动等待](#day-9自动等待)
- [Day 10：失败证据](#day-10失败证据)
- [Day 11：标记与套件](#day-11标记与套件)
- [Day 12：数据与辅助函数](#day-12数据与辅助函数)
- [Day 13：小型回归](#day-13小型回归)
- [Day 14：阶段验收](#day-14阶段验收)
- [Day 15：项目初始化](#day-15项目初始化)
- [Day 16：登录异常](#day-16登录异常)
- [Day 17：特殊用户](#day-17特殊用户)
- [Day 18：商品列表](#day-18商品列表)
- [Day 19：商品详情](#day-19商品详情)
- [Day 20：商品排序](#day-20商品排序)
- [Day 21：加入购物车](#day-21加入购物车)
- [Day 22：多商品购物车](#day-22多商品购物车)
- [Day 23：移除商品](#day-23移除商品)
- [Day 24：结算校验](#day-24结算校验)
- [Day 25：结算概览](#day-25结算概览)
- [Day 26：完整下单](#day-26完整下单)
- [Day 27：登出和会话](#day-27登出和会话)
- [Day 28：Page Object 登录页](#day-28page-object-登录页)
- [Day 29：Page Object 商品页](#day-29page-object-商品页)
- [Day 30：结算页面对象](#day-30结算页面对象)
- [Day 31：测试数据模型](#day-31测试数据模型)
- [Day 32：环境配置](#day-32环境配置)
- [Day 33：多浏览器](#day-33多浏览器)
- [Day 34：报告与 flaky 分析](#day-34报告与-flaky-分析)
- [Day 35：阶段验收](#day-35阶段验收)
- [Day 36：HTTP 与健康检查](#day-36http-与健康检查)
- [Day 37：查询列表](#day-37查询列表)
- [Day 38：创建预订](#day-38创建预订)
- [Day 39：查询单条](#day-39查询单条)
- [Day 40：过滤查询](#day-40过滤查询)
- [Day 41：Token 鉴权](#day-41token-鉴权)
- [Day 42：完整更新 PUT](#day-42完整更新-put)
- [Day 43：部分更新 PATCH](#day-43部分更新-patch)
- [Day 44：删除与清理](#day-44删除与清理)
- [Day 45：API Client](#day-45api-client)
- [Day 46：Booking Client](#day-46booking-client)
- [Day 47：Fixture 生命周期](#day-47fixture-生命周期)
- [Day 48：数据工厂](#day-48数据工厂)
- [Day 49：参数化边界](#day-49参数化边界)
- [Day 50：缺失字段](#day-50缺失字段)
- [Day 51：类型错误](#day-51类型错误)
- [知识主题索引](#知识主题索引)

## 学习方式

每个学习日按以下闭环执行：

1. 学习 20 分钟：理解一个核心知识点，以及它解决的问题。
2. 实践 50 分钟：把知识落实到代码、测试、配置或文档。
3. 验证 15 分钟：运行命令并保存结果到 artifacts/day-XXX/。
4. 复盘 5 分钟：说明知识如何落实、记录问题，并完成知识验收。

判断一个知识点是否真正学会，不只看能否背出定义，还要确认它已经出现在项目产出中，并且有可重复的验证结果。

---

## Day 1：环境与首个 UI 测试

### 核心知识点

理解 pytest 调用 Playwright 完成 UI 断言的执行链：pytest 负责发现和组织测试，Playwright 负责浏览器操作，expect 负责等待并断言页面状态，fixture 负责准备测试环境。

### 它解决的问题

把手工操作转成可重复执行的 UI 检查，并用用户可观察的业务结果证明功能确实生效。仅仅确认点击或输入没有抛异常，并不能证明 Todo 已经正确创建。

### 理论基础

#### 1. UI 自动化测试在验证什么

UI 自动化不是简单地“用代码点击页面”，而是验证用户通过界面触发后，系统是否产生了可观察且正确的业务结果。一个完整的 UI 测试通常包含四类信息：

- 前置条件：页面、用户、数据和环境处于什么状态；
- 操作：用户做了什么，例如输入文本、点击按钮或勾选 checkbox；
- 观察点：从页面或接口读取什么结果；
- 断言：什么结果才算符合预期。

如果只有操作没有断言，测试最多证明浏览器没有在这一行报错；如果只有一个很宽松的断言，测试可能在错误实现上也通过。

#### 2. pytest、Playwright、expect 的职责边界

pytest 是测试运行器和组织框架，主要负责发现测试函数、注入 fixture、管理参数化用例、收集结果。它本身不负责理解浏览器页面。

Playwright 是浏览器自动化库，负责打开页面、定位元素、执行输入和点击、读取 DOM 状态。它提供的是“如何与页面交互”的能力。

expect 是 Playwright 的断言接口，负责检查页面最终状态，并通常带有自动等待。它表达的是“最终应该是什么”，而不是简单读取一次当前值。

fixture 是测试依赖的声明方式。测试函数声明需要 todo_page，pytest 就负责把准备好的页面对象注入进来。这样测试关注业务行为，页面初始化集中在公共位置。

#### 3. 操作与结果必须分离

可以把测试写成以下公式：

~~~text
给定一个已知前置状态
    当执行用户操作
    那么验证可观察的业务结果
~~~

例如“输入 Buy milk 并回车”只是 When；“列表出现一条 Buy milk 且未完成数为 1”才是 Then。操作本身成功，不代表业务状态正确。

#### 4. 为什么 UI 测试要验证最终状态

页面交互通常会经过事件处理、状态更新、DOM 渲染等步骤。点击动作成功只说明事件被触发，不能证明事件监听器、应用状态、页面渲染和派生状态都正确更新。

因此断言应优先落在用户能看到、业务真正关心的结果上，而不是只断言某个方法被调用。

#### 5. 记忆要点

看到一个 UI 测试时，按四个问题复盘：

1. 测试开始时系统处于什么状态？
2. 用户操作是什么？
3. 用户能观察到的结果是什么？
4. 如果实现只完成了一半，哪条断言能发现它？


### 执行链

~~~text
pytest 发现测试
    ↓
fixture 准备 Playwright 页面
    ↓
Playwright 定位元素并执行操作
    ↓
expect 等待并断言最终 UI 状态
~~~

### 代码落地

在 test_todos.py 中，测试通过 todo_page fixture 打开 TodoMVC 页面，定位输入框，输入 Buy milk 并按下 Enter，然后断言：

- Todo 列表数量为 1；
- 列表文本为 Buy milk；
- 未完成计数包含 1。

### 常见问题与经验

- 测试节点名称必须和实际测试结构一致，例如模块级函数与类方法的 pytest 节点路径不同。
- ERR_CONNECTION_REFUSED 通常先指向被测服务未启动，不应立即归因于测试代码。
- “操作无异常”不是充分断言，必须检查最终业务状态。

### 知识验收

能够说明 pytest、Playwright、expect 和 fixture 在代码中的职责，并解释为什么需要验证最终 UI 状态。

### 关联产出

- 目标文件：test-projects/01-todomvc-ui/tests/test_todos.py
- 证据目录：artifacts/day-001/

---

## Day 2：完成状态

### 核心知识点

掌握 checkbox 交互与状态断言，验证一个 Todo 从未完成到已完成的完整状态转换。

### 它解决的问题

避免只断言 checkbox 被选中而产生假通过。控件状态发生变化，不代表 Todo 行样式和业务计数已经同步更新。

### 理论基础

#### 1. 状态转换而不是单次点击

完成 Todo 是一个状态转换问题：

~~~text
未完成 Todo
    -- check() -->
已完成 Todo
~~~

测试目标不是证明“调用过 check”，而是证明状态从 S0 正确转换到 S1。一个可靠的状态转换测试至少要覆盖控件、实体和业务结果三个层面。

#### 2. check() 与 click() 的语义差异

click() 表示模拟一次点击。如果 checkbox 已经选中，再 click() 可能把它取消选中，因此测试结果依赖执行前状态。

check() 表示确保 checkbox 最终处于选中状态，更接近“完成 Todo”这种目标状态。对应地，uncheck() 表达确保最终处于未选中状态。

选择操作 API 时，要问：

~~~text
我是在模拟一个动作，还是在声明一个最终状态？
~~~

动作需要关注当前状态和副作用；目标状态操作更容易表达稳定、幂等的测试意图。

#### 3. 状态断言的三层含义

- 控件层：checkbox 是否 checked；
- 实体层：Todo 行是否带 completed 类或其他完成标记；
- 业务层：未完成计数是否从 1 变为 0。

只验证控件层，可能漏掉渲染和业务计算缺陷；只验证计数，可能漏掉错误的 Todo 被完成。多层断言的价值在于覆盖状态转换链路，而不是盲目增加断言数量。

#### 4. 派生状态与不变量

未完成计数是 Todo 集合的派生状态。对于一条 Todo，完成后应满足：

~~~text
checkbox.checked = true
Todo.class contains completed
active_count = total_active_items - 1
~~~

这些同时成立的关系可以看作业务不变量。状态断言不仅检查单个元素，还在检查相关状态之间是否保持一致。

#### 5. 常见假通过模式

- 只断言 checkbox 可见：可见不代表选中；
- 只断言点击没有异常：事件可能没有正确处理；
- 只断言计数变化：可能完成了错误的 Todo；
- 只断言样式：样式可能更新了，但计数没有同步。

#### 6. 记忆要点

状态测试可以记成“控件—实体—业务”三层。每次设计状态转换测试时，至少问自己：控件变了吗？实体变了吗？业务结果同步了吗？


### 三层断言

~~~text
控件状态：checkbox 已选中
    ↓
Todo 状态：Todo 行具有 completed 类
    ↓
业务结果：未完成计数从 1 变为 0
~~~

### 代码落地

测试使用 check() 表达“确保最终为选中状态”，再分别断言 checkbox 已选中、Todo 行具有 completed 类、未完成计数为 0。

### 常见问题与经验

- checkbox 测试失败前，先确认本地 HTTP 服务是否运行。
- 应同时验证控件、DOM 状态和业务结果，避免只覆盖其中一层。
- 环境不可用和测试代码失败是不同类型的问题，应分别记录根因。

### 知识验收

能够解释为什么 to_be_checked()、to_have_class("completed") 和未完成计数断言需要同时存在。

### 关联产出

- 目标文件：test-projects/01-todomvc-ui/tests/test_todos.py
- 证据目录：artifacts/day-002/

---

## Day 3：删除行为

### 核心知识点

理解操作后的 DOM 与业务状态校验，确认删除的是目标数据，并确认其他数据没有被误删。

### 理论基础

#### 1. 删除测试的核心不是按钮，而是对象身份

删除行为真正要表达的是：

~~~text
删除指定对象 A
    → A 不再存在
    → 其他对象 B 仍然存在且内容未变
    → 派生业务状态正确
~~~

因此定位目标时应优先使用对象的稳定身份或内容范围，再在目标范围内定位删除按钮。不要先用列表中的第一个或第二个按钮代表业务对象。

#### 2. 为什么数量断言不够

假设初始集合是 [Buy milk, Learn pytest]，预期删除 Buy milk，结果却删除了 Learn pytest，最终集合仍然只有一条。只断言列表数量为 1 会错误通过。

只有把集合内容也写出来，测试才能区分：

~~~text
预期：[Learn pytest]
实际：[Buy milk]
~~~

这就是“数量正确但对象错误”的假通过。

#### 3. 定位范围的思想

推荐的定位层级是：

1. 先定位 Todo 集合；
2. 用文本或其他业务特征筛选目标 Todo；
3. 在目标 Todo 内定位 destroy 按钮；
4. 执行操作；
5. 回到集合和目标对象上验证结果。

这种范围限定可以降低误操作风险，也让代码更接近用户语义：删除名为 Buy milk 的 Todo，而不是点击页面上的第一个删除按钮。

#### 4. 删除后的后置条件

删除测试的后置条件至少包括：

- 目标对象不存在；
- 其他对象仍存在；
- 结果集合内容精确匹配预期；
- 数量和未完成计数与新集合一致。

其中“不存在”是负向断言，“保留项正确”是正向断言，两者缺一都可能留下漏洞。

#### 5. 隐藏按钮与用户交互

TodoMVC 的删除按钮默认隐藏。hover() 不是多余步骤，而是模拟真实用户把鼠标移动到目标行后，页面才显示该行操作按钮。交互前置条件也属于测试行为的一部分。

#### 6. 记忆要点

删除测试记成“目标消失、同伴保留、集合正确、计数同步”。只看到数量变化时，要警惕是否漏了对象身份。


### 它解决的问题

只断言列表数量从 2 变为 1 可能产生假通过，因为误删另一条 Todo 也会满足数量变化。测试必须同时证明目标消失、正确项目保留、业务计数同步。

### 代码落地

测试先创建 Buy milk 和 Learn pytest，再使用目标过滤器精确定位：

~~~python
target_todo = todo_items.filter(has_text="Buy milk")
target_todo.hover()
target_todo.locator(".destroy").click()
~~~

删除后验证：

- 目标 Todo 数量为 0；
- 列表总数为 1；
- 保留项为 Learn pytest；
- 未完成计数为 1。

### 常见问题与经验

- 删除按钮默认隐藏，需要先对目标 Todo 执行 hover()。
- 删除操作要在目标元素范围内定位按钮，避免误操作其他项目。
- DOM 断言关注页面留下什么，业务状态断言关注数据计算出的状态是否同步。

### 知识验收

能够解释为什么只断言列表数量不足以证明删除正确，并指出用于捕获误删的关键断言。

### 关联产出

- 目标文件：test-projects/01-todomvc-ui/tests/test_todos.py
- 证据目录：artifacts/day-003/

---

## Day 4：筛选功能

### 核心知识点

掌握可见性和集合断言，区分“某个目标存在”和“当前结果集合完全正确”。

### 理论基础

#### 1. 筛选本质上是集合运算

把所有 Todo 看成集合 All，筛选器是在这个集合上应用条件：

~~~text
All       = 全部 Todo
Active    = { todo | todo.completed = false }
Completed = { todo | todo.completed = true }
~~~

因此筛选测试不是只检查一个元素，而是检查条件过滤后的整个集合是否正确。

#### 2. 集合正确性的三个维度

一个完整的集合断言至少考虑：

- 基数：结果有多少条；
- 成员：结果包含哪些对象；
- 排列或顺序：对象顺序是否符合产品行为。

只断言 Active 中 Buy milk 可见，无法发现 Learn pytest 也错误地混入 Active。数量加完整文本集合才能捕获这种问题。

#### 3. selected 与结果集合是两个状态

筛选器本身的 selected 类表示当前交互选择，Todo 列表表示业务筛选结果。两者需要分别断言：

~~~text
筛选器状态正确
    +
结果集合正确
    =
筛选功能验证完整
~~~

如果只看 Todo 列表，可能无法发现点击后选中状态没有更新；如果只看 selected，又无法证明过滤逻辑正确。

#### 4. 正向与负向覆盖

Active 场景既要确认 Active Todo 存在，也要确认 Completed Todo 不存在。Completed 场景同理。集合数量和完整文本断言通常能同时表达正向和负向要求，比逐个写可见性断言更不容易漏项。

#### 5. 如何选择筛选测试数据

至少准备两个状态明确、文本不同的对象：一条 Active Todo 和一条 Completed Todo。这样三种筛选都有可观测差异。

#### 6. 记忆要点

筛选测试记成“筛选器选中、集合数量正确、集合成员正确、错误状态不混入”。这比“点击三个按钮”更接近真实测试目标。


### 它解决的问题

只断言目标 Todo 可见，无法发现筛选结果中混入了其他状态的 Todo。集合断言可以同时发现缺少数据和多余数据。

### 单元素与集合断言

~~~text
单元素断言：某个目标存在或可见
集合断言：数量、完整内容以及是否存在多余项目
~~~

### 代码落地

测试创建一条 Active Todo 和一条 Completed Todo，依次验证 All、Active、Completed。每种筛选都断言筛选器具有 selected 状态，并使用数量和完整文本验证结果集合。

~~~python
expect(todo_items).to_have_count(2)
expect(todo_items.locator("label")).to_have_text(
    ["Buy milk", "Learn pytest"]
)
~~~

### 常见问题与经验

- 筛选器交互状态和筛选后的业务结果是两个不同的断言对象。
- 集合断言应尽量验证数量和完整文本，而不是只检查其中一个目标。
- All、Active、Completed 应使用状态明确的测试数据，避免场景含义模糊。

### 知识验收

能够解释为什么“目标可见”可能假通过，以及数量和完整文本断言如何捕获多余数据。

### 关联产出

- 目标文件：test-projects/01-todomvc-ui/tests/test_filters.py
- 证据目录：artifacts/day-004/

---

## Day 5：边界输入

### 核心知识点

学习等价类和边界值，用少量代表性数据覆盖不同输入行为，并识别断言本身可能掩盖缺陷的风险。

### 理论基础

#### 1. 等价类划分

等价类是指在测试目标上可以认为行为相同的一组输入。测试不可能穷举所有字符串，因此要按预期行为划分代表类：

~~~text
无效类：只包含空白
规范化类：首尾有空格
重复数据类：与已有 Todo 相同
健壮性类：长度明显增加
~~~

每个类至少选择一个代表值，并为它写出明确预期。等价类关注的是行为分类，不是字符串表面长得是否不同。

#### 2. 边界值分析

边界值关注规则可能发生变化的位置，例如空字符串与第一个有效字符之间、去除空格后长度为 0 的位置、允许长度与超出长度之间、第一次创建与重复创建之间。

当前项目没有提供最大长度规格，所以 256 个字符是健壮性样本，而不是已证明的系统边界。没有产品规则时，必须把假设写出来。

#### 3. 测试预言与断言精度

测试预言是“根据输入，我们认为系统应该产生什么结果”。如果预期没有写清楚，测试只是执行脚本。

断言也存在精度差异：

- 可见性断言：证明元素用户可见；
- 文本断言：可能按 Playwright 的文本规范化规则比较；
- textContent 属性断言：检查 DOM 原始文本内容；
- 数量断言：检查集合基数，但不检查成员身份。

选择断言时，必须让断言精度至少达到风险所需的精度。

#### 4. 输入规范化与信息损失

如果应用会 trim 首尾空格，这是一次输入规范化。宽松文本断言可能把多个实际结果视为相同，导致信息损失。因此高风险边界需要使用更精确的属性断言。

#### 5. 代表性数据的取舍

好的边界测试不是数据越多越好，而是每个数据都代表一个风险。应记录：

- 这个数据属于哪个等价类；
- 它要验证什么行为；
- 如果失败，说明哪条产品规则可能有问题；
- 当前预期是产品事实还是学习阶段的假设。

#### 6. 记忆要点

边界测试记成“先分行为类，再找变化边界，最后选择足够精确的断言”。正常值证明主路径，边界值暴露规则交界处的缺陷。


### 它解决的问题

只测试正常文本会漏掉空输入、规范化、重复数据和长文本处理问题。合理划分输入类别，可以用较少测试覆盖更有价值的风险。

### 四类输入

| 输入类别 | 代表风险 | 预期关注点 |
| --- | --- | --- |
| 空白输入 | 无效数据 | 不创建 Todo |
| 前后空格 | 输入规范化 | 是否去除首尾空格 |
| 重复文本 | 重复数据规则 | 是否允许创建重复项 |
| 256 字符长文本 | 健壮性输入 | 文本是否被截断 |

没有明确最大长度规格时，256 字符只是代表性长文本，不应直接宣称它是系统最大边界。

### 代码落地

测试分别验证：

- 空白输入创建 0 条；
- 两侧带空格的 Buy milk 创建 1 条且原始 textContent 是 Buy milk；
- 两次 Buy milk 创建 2 条；
- 256 个 A 创建 1 条且文本未被截断。

### 常见问题与经验

普通的 to_have_text("Buy milk") 可能进行空白规范化，无法严格证明 DOM 原始文本已经去除首尾空格。需要使用以下精确属性断言：

~~~python
expect(todo_label).to_have_js_property("textContent", "Buy milk")
~~~

断言语义本身也要纳入测试设计，否则宽松断言可能把缺陷判成通过。

### 知识验收

能够解释四类输入的风险，说明为什么前后空格场景需要 textContent，并区分代表性长文本与已知产品最大长度。

### 关联产出

- 目标文件：test-projects/01-todomvc-ui/tests/test_input_validation.py
- 证据目录：artifacts/day-005/

---

## Day 6：参数化

### 核心知识点

掌握 pytest.mark.parametrize，在测试步骤相同、输入不同且预期结构相同时，用一份测试逻辑覆盖多组数据。

### 理论基础

#### 1. 参数化的本质：测试矩阵

参数化把测试逻辑和测试数据分开：

~~~text
固定测试步骤 × 多组输入数据 = 测试矩阵
~~~

pytest 会为每一行数据生成一个独立的测试调用，而不是把所有数据塞进一次循环。

#### 2. 参数化与普通循环的区别

普通循环通常表现为一个测试：

~~~python
def test_create_todos(todo_page):
    for text in texts:
        ...
~~~

如果循环中第二组失败，报告可能只显示整个测试失败，失败数据需要自己排查。参数化会把每组数据拆成独立用例，因此报告能指出具体哪一组失败，也能独立重跑。

循环适合同一个业务场景中的批量操作；参数化更适合多个相互独立、步骤结构相同的测试场景。

#### 3. 独立性来自 fixture 生命周期

参数化函数每次调用时，todo_page fixture 通常也会按其作用域准备页面。这样每组数据从干净状态开始，不会因为上一组已经创建了 Todo 而影响下一组。

如果把页面或数据放到模块级全局变量中，参数化仍然可能发生污染。参数化解决的是数据复用，不会自动修复共享状态问题。

#### 4. 何时适合参数化

适合的特征：

- 前置条件基本一致；
- 操作步骤一致；
- 断言结构一致；
- 只有输入值或预期值变化；
- 每组数据可以独立运行。

不适合的特征：

- 不同数据需要完全不同的操作流程；
- 某些数据需要额外的前置准备；
- 断言逻辑差异大；
- 为了兼容差异而在函数中堆积 if/else；
- 测试名称变得难以理解。

#### 5. 参数化数据的可读性

简单数据可以直接使用字符串；复杂数据通常应使用多个字段：

~~~python
@pytest.mark.parametrize(
    "input_text, expected_count",
    [
        ("Buy milk", 1),
        ("   ", 0),
    ],
    ids=["normal-text", "blank-text"],
)
~~~

ids 不是参数化的核心要求，但在数据较多或输入不直观时，可以显著提高失败定位速度。

#### 6. 记忆要点

参数化记成“逻辑只写一次，数据按行展开，调用彼此独立，失败能够定位”。减少重复代码只是表面收益，更重要的是让测试矩阵和覆盖意图变得清晰。


### 它解决的问题

避免为多组输入复制几乎一样的测试代码，同时让测试数据集中、覆盖范围清晰、失败用例容易定位。

### 基本模型

~~~python
@pytest.mark.parametrize(
    "todo_text",
    ["Buy milk", "Learn pytest", "Write parameterized test"],
)
def test_create_todo_for_each_input(todo_page: Page, todo_text: str):
    ...
~~~

pytest 会把每组数据依次传给 todo_text，将同一个函数独立执行三次，并分别报告每个用例的通过或失败。

### 判断是否适合参数化

~~~text
测试步骤相同
    +
输入数据不同
    +
预期结果结构相同
    =
适合使用参数化
~~~

如果不同数据需要完全不同的操作流程或不同的断言逻辑，就不应为了减少文件数量强行参数化。

### 代码落地

test_todo_data.py 使用 todo_text 接收三组 Todo 文本，每次执行相同的：

1. 定位输入框；
2. fill(todo_text)；
3. press("Enter")；
4. 断言列表数量为 1；
5. 断言 Todo 文本匹配输入。

测试结果为 3 个参数化用例全部通过。

### 常见错误

- 装饰器中的参数名与测试函数参数名不一致；
- 把有不同业务流程的数据强行塞进同一个测试函数；
- 在参数化用例之间共享页面状态，造成数据污染；
- 只减少代码行数，却没有为每组数据保留清晰的失败信息。

### 知识验收

能够说明装饰器如何为每组数据生成独立用例，并指出代码中“输入不同、步骤相同”的位置。

### 关联产出

- 目标文件：test-projects/01-todomvc-ui/tests/test_todo_data.py
- 验证命令：pytest test-projects/01-todomvc-ui/tests/test_todo_data.py -q
- 验证结果：3 passed
- 证据文件：artifacts/day-006/pytest-parametrize.txt

---

## Day 7：Fixture

### 核心知识点

理解测试前置、后置和隔离，掌握 fixture（测试夹具）如何通过依赖注入复用 Setup（准备）和 Teardown（清理），并用作用域控制资源生命周期。

### 它解决的问题

如果每个测试都手动打开页面、创建浏览器资源和准备相同数据，代码会重复；如果测试共享可变页面或数据，前一个测试的删除、完成状态或登录信息可能污染后一个测试。fixture 把公共准备集中起来，同时让每个测试获得明确的隔离边界。

### 理论基础

#### 定义与关键概念

fixture 是 pytest 提供的可复用测试依赖。测试函数在参数中声明 fixture 名称后，pytest 会解析依赖、执行准备代码，并把结果注入测试函数。

- Setup：测试开始前创建页面、打开 URL 或准备测试数据；
- 注入：fixture 通过 `yield` 或 `return` 把对象交给测试；
- Teardown：测试结束后关闭 page、context 或 browser 等资源；
- 作用域（scope）：决定 fixture 多久创建一次，常见有 `function`、`class`、`module` 和 `session`；
- 隔离：每个测试使用独立的可变状态，避免测试顺序改变结果。

#### 心智模型或执行链

~~~text
pytest 收集测试
    ↓
解析测试参数中的 fixture
    ↓
按依赖顺序执行 Setup 并注入对象
    ↓
执行测试操作和业务断言
    ↓
按依赖的逆序执行 Teardown
~~~

本日项目的依赖链是：`browser（session） → context（function） → page（function） → todo_page → todo_page_with_todos → 测试函数`。

#### 作用域与隔离的取舍

| Fixture | 作用域 | 适合承担的职责 | 主要风险 |
| --- | --- | --- | --- |
| `browser` | `session` | 复用启动成本较高的浏览器进程 | 把可变业务状态放在这里会跨测试污染 |
| `context` | `function` | 隔离 Cookie、Local Storage、登录状态和页面环境 | 每个测试重新创建有少量开销 |
| `page` | `function` | 为每个测试提供独立页面并在结束后关闭 | 忘记关闭会造成资源泄漏 |
| `todo_page_with_todos` | `function` | 准备当前测试需要的 Todo 数据 | 固定数据过多会隐藏场景意图 |

一般原则是：昂贵且无状态的资源可以扩大作用域；会被测试修改的页面、context 和业务数据应保持函数级隔离。

#### `yield` 与最小代码骨架

~~~python
@pytest.fixture
def todo_page_with_todos(todo_page: Page):
    todo_input = todo_page.get_by_placeholder("What needs to be done?")
    for todo_text in ["Buy milk", "Learn pytest"]:
        todo_input.fill(todo_text)
        todo_input.press("Enter")
    yield todo_page
~~~

`yield` 前的代码是 Setup，`yield` 产出的对象传给测试；测试结束后，pytest 回到 `yield` 后执行清理。当前 fixture 没有重复关闭 page，因为它依赖的 `page`、`context` fixture 会负责资源回收。

#### 适用场景与边界

适合提取为 fixture：多个测试重复出现的稳定前置条件、资源创建与清理、每次都应重新生成的测试数据和基础页面状态。不适合提取：只被一个测试使用的业务操作、删除或筛选等核心行为、业务断言，以及依赖测试顺序的共享可变状态。

如果多个测试只是输入不同、步骤和断言结构相同，优先考虑参数化；如果多个测试需要相同的前置状态，才考虑 fixture。两者可以组合，但解决的问题不同。

#### 常见错误、反例与假通过

- 把 context 或业务数据设为 `session` 作用域，导致前一个测试的修改残留；
- 把断言放入 fixture，混合准备逻辑和业务验证职责；
- fixture 内部偷偷执行大量业务操作，测试函数看不出真正场景；
- 只减少重复代码，却没有验证每个测试是否仍从独立状态开始。

#### 记忆要点

先找重复的 Arrange/Setup，再抽取 fixture；让 fixture 准备环境和数据，让测试执行行为和断言；用函数级作用域隔离可变状态，用 `yield` 管理资源生命周期。

### 代码落地

本日新增 `todo_page_with_todos`，依赖已打开页面的 `todo_page`，每个测试创建独立的 `Buy milk` 和 `Learn pytest`。`test_delete_todo` 和 `test_filter_todos` 不再重复填写输入框和提交 Todo，只声明需要的 fixture；删除、完成、筛选和结果断言仍保留在测试中。

这体现了两点：数据准备被复用，但业务行为没有被隐藏；函数级 fixture 让删除测试对页面的修改不会影响筛选测试。

### 知识验收

1. 为什么 `browser` 可以使用 `session` 作用域，而 `context` 和测试数据通常使用 `function` 作用域？
2. `yield` 前后分别承担什么职责？
3. 为什么 `todo_page_with_todos` 不应该包含删除或筛选断言？
4. 如何判断重复代码应该提取为 fixture，还是应该使用参数化？

### 关联产出

- 目标文件：`test-projects/01-todomvc-ui/tests/conftest.py`
- 关联测试：`test-projects/01-todomvc-ui/tests/test_todos.py`、`test-projects/01-todomvc-ui/tests/test_filters.py`
- 验证命令：`.\.venv\Scripts\python.exe -m pytest test-projects/01-todomvc-ui/tests -q`
- 验证结果：授权环境中 `11 passed in 9.71s`
- 证据文件：`artifacts/day-007/pytest-fixtures.txt`
---

## Day 8：稳定定位

### 核心知识点

稳定定位（stable locator）是根据用户可感知的语义、业务对象和明确的结构范围查找页面元素，而不是把测试绑定到容易变化的 CSS class 或 DOM 细节。Playwright 中常见的定位信息包括 role、label、text、placeholder 和 CSS 结构选择器。

### 它解决的问题

脆弱定位器会让测试随着无业务影响的前端重构一起失败。例如 `.toggle` 依赖 CSS class 名；class 改成 `.todo-checkbox` 后，用户仍然看到并操作同一个 checkbox，但测试已经无法找到元素。稳定定位降低了测试与实现细节的耦合，也让失败信息更接近真实业务意图。

### 理论基础

#### 定位策略

| 定位方式 | 适合场景 | 主要风险 |
| --- | --- | --- |
| `get_by_role()` | 链接、按钮、checkbox 等用户可操作控件 | role 可能在页面中重复，需要名称或容器作用域 |
| `get_by_label()` | 有明确可访问 label 的表单控件 | 页面没有正确关联 label 时不能强行使用 |
| `get_by_text()` | 唯一的用户可见文本，或已缩小到明确业务对象内 | 重复文本、包含匹配和文本变化会造成歧义 |
| `get_by_placeholder()` | 页面没有 label 但 placeholder 是稳定契约的输入框 | placeholder 变化会影响测试，不能替代真正的 label |
| CSS | 稳定的结构容器，或缺少语义钩子的元素 | 直接依赖 class、层级和样式实现，容易随重构失效 |

优先使用 role、label、明确的 placeholder 或经过作用域限制的 text。CSS 可以用于锁定结构区域；进入结构区域后，再用语义定位业务对象和交互控件。

#### 心智模型

定位可以看成两层：

```text
页面结构范围：.todo-list
        ↓
业务对象：get_by_role("listitem")
        ↓
对象内控件：get_by_role("checkbox") / get_by_role("button")
```

语义定位不是“全页面搜索 role”。同一种 role 可能出现在多个区域，必须用业务容器、名称或唯一文本继续缩小范围。

#### 最小代码骨架

```python
todo_items = page.locator(".todo-list").get_by_role("listitem")
target_todo = todo_items.filter(has_text="Buy milk")

expect(target_todo).to_have_count(1)
target_todo.get_by_role("checkbox").check()
```

`to_have_count(1)` 证明当前 Todo 列表中唯一匹配一个目标；它不能证明整张页面只有一个相同文本。`get_by_role("checkbox")` 表达的是用户要操作的控件类型；如果页面有多个 checkbox，仍需要先限定业务对象。

#### 适用场景与边界

- role 适合用户能识别和操作的控件，优先使用可访问名称进一步提高唯一性。
- label 适合真正关联到表单控件的标签；没有关联关系时不要为了形式强行使用。
- text 适合唯一文本，重复文本必须先限定到具体业务对象。
- CSS 适合稳定的结构容器，或页面没有可访问语义的元素；不要把普通样式 class 当成首选定位器。
- 状态 class（例如 `.completed`）可以作为状态断言，但不应拿它作为查找目标元素的主要依据。

#### 常见错误、反例与假通过

1. 把 `.toggle`、`.destroy` 或 `.todo-list li` 当作默认定位器，测试会绑定到 CSS 和 DOM 实现。
2. 直接使用全页 `get_by_role("listitem")`，会把筛选导航中的 `li` 也计算进去。本日第一次授权运行得到 `10 failed, 2 passed`，根因就是作用域过宽。
3. 对重复文本使用 `get_by_text("Buy milk").first`，虽然可能通过，却没有表达真正的业务选择条件。
4. 使用无名称的 `get_by_role("button")` 时不限定父级对象，未来增加按钮后可能出现歧义。本日将它限制在目标 Todo 内。

#### 记忆要点

先用结构范围确定“在哪个业务区域找”，再用 role、label 或唯一文本确定“要找什么”，最后在业务对象内部操作控件。CSS 可以锁定容器，但不应成为用户控件的默认语义。

### 代码落地

本日新增 `test_locators.py`，并将 Todo、新增、完成、删除、筛选、参数化和边界输入测试中的脆弱元素定位重构为“`.todo-list` 容器 + 语义 locator”。新增和完成测试使用 `listitem`、`checkbox`；筛选链接继续使用带名称的 `link`；删除按钮使用目标 Todo 作用域内的 `button`。`.completed` 和 `.todo-count` 仍用于状态验证，而不是作为业务对象定位器。

### 知识验收

1. 为什么语义 role 仍然需要容器作用域？
2. 什么情况下 CSS 结构定位是合理例外，什么情况下它会变成脆弱实现定位？
3. 为什么重复 Todo 文本不能直接使用全页 `get_by_text()`？
4. 本日第一次测试失败暴露了什么定位问题，最终如何修复？

### 关联产出

- 目标文件：`test-projects/01-todomvc-ui/tests/test_locators.py`
- 重构文件：`test-projects/01-todomvc-ui/tests/test_todos.py`、`test-projects/01-todomvc-ui/tests/test_filters.py`、`test-projects/01-todomvc-ui/tests/test_todo_data.py`、`test-projects/01-todomvc-ui/tests/test_input_validation.py`
- 验证命令：`.\.venv\Scripts\python.exe -m pytest test-projects/01-todomvc-ui/tests -q`
- 验证结果：授权环境中 `12 passed in 9.88s`
- 证据文件：`artifacts/day-008/pytest-locators.txt`
---

## Day 9：自动等待

### 核心知识点

自动等待（auto-waiting）负责在 Playwright 执行操作前等待元素达到可操作状态；显式条件等待（condition-based waiting）使用 `expect` 在超时范围内反复检查业务状态。两者共同替代没有业务含义的固定 `sleep`。

### 它解决的问题

固定时间等待只表达“再等一段时间”，不表达页面何时真正准备好。页面响应较快时它浪费时间，响应较慢时它仍可能过早读取结果，导致 CI 中的偶发失败。等待明确的 UI 状态可以让测试更稳定、更快，也让失败信息直接说明哪个业务条件没有成立。

### 理论基础

#### 定义与关键概念

- `Locator` 是惰性页面元素引用，通常在实际操作或断言时才解析页面。
- `click()`、`check()`、`fill()`、`press()` 等操作会自动等待元素可见、稳定、启用并能接收事件等可操作条件。
- `expect(locator).to_have_count()`、`to_have_text()`、`to_be_checked()`、`to_have_class()` 等断言会在默认超时内重试，直到状态满足或超时失败。
- `time.sleep()` 和 `page.wait_for_timeout()` 是固定时间等待，不应作为业务同步机制。

#### 心智模型或执行链

```text
准备 Locator
    ↓
执行 click / check / press
    ↓
Playwright 自动等待元素可操作
    ↓
页面发生业务变化
    ↓
expect(...) 等待并验证目标状态
```

可以记成：自动等待保证“操作能做”，`expect` 保证“结果做对”。

#### 最小代码骨架

```python
todo_input.press("Enter")
todo_items = page.locator(".todo-list").get_by_role("listitem")

expect(todo_items).to_have_count(1)
expect(todo_items).to_have_text(["Wait for state"])
```

这段代码没有猜测等待 1 秒，而是等待 Todo 数量和文本真正达到预期。

#### 断言、数据或状态的含义

`expect(todo_items).to_have_count(1)` 证明列表中当前有一条匹配的 Todo，但不能证明文本正确；`to_have_text(["Wait for state"])` 证明这条 Todo 的文本符合预期，但不能单独证明未完成计数正确。因此需要根据业务结果组合数量、文本和计数断言。

#### 适用场景与边界

- 页面操作前优先依赖 Locator 的自动等待，不要用 `sleep` 预留时间。
- 操作后等待用户可观察的业务状态，例如列表数量、文本、选中状态、完成状态或计数。
- `wait_for_load_state("networkidle")` 可以表达导航后的网络状态，但不能替代“业务状态已完成”的断言。
- 只有在确实需要等待非 UI 条件、且没有可观察状态时，才考虑更底层的等待机制，并应说明原因和超时边界。

#### 常见错误、反例与假通过

1. `sleep(1); expect(todo_items).to_have_text(...)` 仍然把稳定性押在固定时间上，页面慢时可能失败。
2. 只验证 `click()` 没抛异常，最多证明点击操作完成，不能证明筛选、创建或删除结果正确。
3. 只等待 `networkidle`，可能因为网络空闲但前端状态仍未更新而产生假通过或误判。
4. 使用过长的全局超时掩盖错误，应该等待具体业务状态并保持失败信息可解释。

#### 记忆要点

操作前问：“元素现在能不能安全操作？”交给 Locator 自动等待；操作后问：“页面是否已经达到业务预期？”交给 `expect` 条件等待；不要用固定秒数代替状态。

### 代码落地

本日新增 `test_waiting.py`，创建 Todo 后使用 `.todo-list` 作用域取得 Todo 项，并用 `expect(todo_items).to_have_count(1)`、`to_have_text(["Wait for state"])` 和未完成计数断言等待并验证页面状态。测试目录静态扫描未发现 `sleep(` 或 `wait_for_timeout`，目标测试通过 `1 passed in 1.90s`。

### 知识验收

1. 为什么固定 `sleep(1)` 不能表达页面真正准备好？
2. `locator.click()` 的自动等待与 `expect(...)` 的条件等待分别验证什么？
3. `to_have_count(1)` 能证明什么，不能证明什么？
4. 为什么 `networkidle` 不能替代业务状态断言？

### 关联产出

- 目标文件：`test-projects/01-todomvc-ui/tests/test_waiting.py`
- 验证命令：`pytest test-projects/01-todomvc-ui/tests/test_waiting.py -q`
- 验证结果：`1 passed in 1.90s`
- 静态检查：`tests/` 未发现 `sleep(` 或 `wait_for_timeout`
- 证据文件：`artifacts/day-009/pytest-waiting.txt`
---

## Day 10：失败证据

### 核心知识点

失败证据是测试失败后自动保留的、能够帮助还原现场的调试信息。截图记录某个时间点的页面外观，Trace 记录测试操作和页面变化的时间线，日志记录断言、异常、超时和堆栈。三者组合起来，才能同时回答“当时看到了什么”“之前发生了什么”和“程序为什么失败”。

### 它解决的问题

只有断言错误时，失败信息可能无法说明页面当时是否加载、输入是否成功、元素是否可见，或者失败前哪一个操作改变了状态。失败截图提供现场，Trace 提供过程，日志提供原因，从而减少只能在本地重新猜测和复现的排查成本。

### 理论基础

#### 定义与关键概念

- **截图（screenshot）**：页面在单个时间点的 PNG 快照，适合确认可见文本、控件、布局和业务状态。
- **Trace**：Playwright 的过程记录，通常包含操作时间线、页面快照、网络活动和资源，保存后可在 Trace Viewer 中回放。
- **日志（log）**：pytest 和 Playwright 输出的测试名、断言差异、超时、异常类型与堆栈，适合快速定位失败位置和技术原因。
- **失败保留策略**：通过测试停止并丢弃 Trace，失败测试保存截图和 Trace，避免成功用例持续产生大量调试文件。

#### 心智模型或执行链

```text
创建 BrowserContext
        ↓
启动 context.tracing.start(...)
        ↓
执行操作和业务断言
        ↓
pytest 生成 rep_call
        ├── 通过：tracing.stop()，丢弃 Trace
        └── 失败：保存 screenshot，再 tracing.stop(path=...) 保存 ZIP
```

可以记成：**截图看现场，Trace 看过程，日志看原因；绿测清理，红测留证。**

#### 最小代码骨架

```python
context.tracing.start(
    screenshots=True,
    snapshots=True,
    sources=True,
)

yield

report = getattr(request.node, "rep_call", None)
if report is None or not report.failed:
    page.context.tracing.stop()
else:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(artifact_dir / "test.png"))
    page.context.tracing.stop(path=str(artifact_dir / "test.zip"))
```

启动和停止必须属于同一个 BrowserContext 生命周期。成功分支调用不带路径的 `stop()`，表示结束并丢弃本次 Trace；失败分支给 `stop()` 传入 ZIP 路径，才能把 Trace 保存为可回放证据。

#### 截图、Trace、日志各自证明什么

| 证据 | 最适合回答的问题 | 不能单独证明什么 |
| --- | --- | --- |
| 截图 | 失败那一刻页面长什么样？ | 失败前的操作顺序和完整网络过程 |
| Trace | 测试如何一步步走到失败？ | 业务断言是否合理，仍需要测试代码和日志解释 |
| 日志 | 哪一步、因为什么异常或断言失败？ | 页面视觉状态和完整交互过程 |

#### 适用场景与边界

- 失败截图适合 UI 状态、布局、文本和元素可见性问题；不要把截图当作唯一的业务断言。
- Trace 适合异步交互、定位器、页面状态和网络过程排查；它可能较大，应优先按失败保留而不是每次运行都保存。
- 日志适合 CI 中快速筛选失败和审计；关键步骤仍应通过可解释的断言表达，而不是只打印大量文本。
- 当前 fixture 在测试执行阶段失败时保留证据；如果页面 fixture 在进入测试前就创建失败，后续可以再设计更早的全局失败处理。
- 文件名应清理空格和特殊字符，避免参数化测试名在 Windows 路径中造成歧义。

#### 常见错误、反例与假通过

1. 只调用 `tracing.start()`，没有在所有分支停止 Trace，可能导致资源未关闭或文件不完整。
2. 失败时调用 `tracing.stop()` 却不传路径，Trace 会被丢弃，最终只剩截图和日志。
3. 每个成功用例都保存截图和 Trace，短期看信息更多，长期会污染工作区并增加存储成本。
4. 只验证证据文件存在，不检查 Trace ZIP 内容，可能把空文件或损坏文件误当成有效证据。
5. 只看截图而不看断言和日志，可能看到正确的页面现场，却仍不清楚失败是期望值错误还是应用状态错误。

#### 记忆要点

失败排查的三问是：“页面当时是什么样？”看截图；“之前发生了什么？”看 Trace；“程序为什么失败？”看日志。成功运行清理调试数据，失败运行保留可回放证据。

### 代码落地

本日将 Trace 在 `test-projects/01-todomvc-ui/tests/conftest.py` 的 `context` fixture 中启动，并在自动 fixture teardown 阶段根据 `rep_call.failed` 选择保存或丢弃。可控地把 Todo 数量期望从 1 改为 99 后，生成了 `artifacts/day-010/test_add_todo.png` 和 `artifacts/day-010/test_add_todo.zip`；恢复断言后目标测试通过，全套测试为 `13 passed`。

### 知识验收

1. 截图、Trace、日志分别最适合回答什么问题？
2. 为什么成功测试应丢弃 Trace，而失败测试应保留 Trace？
3. 可控失败如何证明失败证据链本身可靠？
4. 为什么 Trace 必须在同一个 BrowserContext 中启动和停止？
5. 当前失败 fixture 对测试 setup 阶段失败有什么边界？

### 关联产出

- 目标文件：`test-projects/01-todomvc-ui/tests/conftest.py`
- 验证命令：`pytest test-projects/01-todomvc-ui/tests -q`
- 验证结果：`13 passed in 11.85s`
- 失败证据：`artifacts/day-010/test_add_todo.png`、`artifacts/day-010/test_add_todo.zip`
---

## Day 11：标记与套件

### 核心知识点

使用 pytest marker 按风险和反馈速度组织测试套件：`smoke` 是少量、高价值的关键路径集合，`regression` 是覆盖面更大的功能回归集合。smoke 通常是 regression 的子集，而不是与 regression 互斥的两组测试。

### 它解决的问题

如果所有测试只能整套执行，提交后的快速反馈会变慢；如果只运行少数测试，又可能漏掉边界输入和历史功能回归。marker 让同一批测试可以按执行目的筛选：开发中快速运行 smoke，发布或较大修改后运行 regression。

### 理论基础

#### 1. marker 是分类，不是测试逻辑

marker 只给测试增加可查询的分类标签，不会替代操作、观察点或断言，也不会自动让测试跳过。`pytest -m smoke` 只是选择带有 `smoke` 标签的测试执行。

#### 2. smoke 与 regression 的集合关系

本项目采用以下关系：

~~~text
全部已收集测试：13
└── regression：13
    └── smoke：4 条关键路径
~~~

关键路径同时拥有两个 marker：

~~~python
import pytest

pytestmark = pytest.mark.regression


@pytest.mark.smoke
def test_add_todo(todo_page):
    ...
~~~

模块级 `pytestmark` 让模块中的测试进入 regression；函数级 `@pytest.mark.smoke` 再把关键路径加入 smoke。这样 `pytest -m smoke` 不会漏掉核心功能，`pytest -m regression` 也不会因为 smoke 筛选而排除核心测试。

#### 3. marker 必须在项目配置中声明

最小配置如下：

~~~ini
[pytest]
addopts = -ra --strict-markers

markers =
    smoke: critical user journeys for fast feedback
    regression: broader functional regression coverage
~~~

声明 marker 有两个作用：让团队知道每个标签的语义，并在 `--strict-markers` 下阻止拼写错误或未注册的 marker 被悄悄使用。

#### 4. 筛选结果如何解释

如果执行 smoke 得到：

~~~text
4 passed, 9 deselected
~~~

它表示 pytest 总共发现 13 个测试，其中 4 个符合 `-m smoke` 并实际运行，9 个因为筛选条件被排除。`deselected` 不是 failed，也不是 skipped；它不代表那 9 个测试已经通过，因为它们这次根本没有执行。

### 常见错误、反例与假通过

1. 只写 `@pytest.mark.smoke` 而不在 `pytest.ini` 注册 marker，可能产生未知 marker 警告；启用 `--strict-markers` 后会直接暴露配置问题。
2. 把 smoke 和 regression 设计成互斥集合，可能导致运行 regression 时漏掉核心关键路径。除非项目有特殊约定，核心测试应同时属于两个集合。
3. 把所有测试都标为 smoke，会让 smoke 失去快速反馈价值；边界输入、参数化数据和定位专项通常优先留在 regression。
4. 看到 `deselected` 就把它当作通过，属于错误的结果解读；要确认完整质量仍需运行 regression 或默认全量套件。
5. marker 名称不能代替风险分析。哪些测试进入 smoke，应该由用户关键路径、失败影响和执行成本共同决定。

### 记忆要点

**smoke 看关键路径，regression 看覆盖面；marker 负责选择，不负责断言；核心测试可同时属于两个集合。**

### 代码落地

本日将 `smoke` 和 `regression` 注册在 `test-projects/01-todomvc-ui/pytest.ini`。6 个测试模块通过模块级 `pytestmark` 进入 regression；`test_add_todo`、`test_complete_todo`、`test_delete_todo`、`test_filter_todos` 通过函数级 `@pytest.mark.smoke` 进入关键路径集合。

收集结果为 smoke 4/13、regression 13/13；实际执行结果为 smoke `4 passed, 9 deselected`，regression `13 passed`。首次运行因 Playwright 启动子进程时的 Windows named pipe 权限 `WinError 5` 在 fixture 初始化阶段受阻，授权环境重跑后通过；该环境根因和处理记录在 `artifacts/day-011/verification.md`。

### 知识验收

1. 为什么 smoke 通常是 regression 的子集，而不是两组互斥测试？
2. `pytestmark` 和函数级 `@pytest.mark.smoke` 在本日分别承担什么作用？
3. `4 passed, 9 deselected` 能证明什么，不能证明什么？
4. 为什么 marker 声明和 `--strict-markers` 能减少配置错误？

### 关联产出

- 目标配置：`test-projects/01-todomvc-ui/pytest.ini`
- 标记测试：`test-projects/01-todomvc-ui/tests/`
- 运行说明：`test-projects/01-todomvc-ui/README.md`
- 验证证据：`artifacts/day-011/verification.md`

---

## Day 12：数据与辅助函数

### 核心知识点

测试数据、动作和断言是测试中的三种不同职责：数据决定“拿什么测”，动作描述“如何操作”，断言说明“操作后必须满足什么业务结果”。辅助函数（helper）适合封装可复用动作，fixture 适合准备页面、浏览器上下文和测试前置条件，测试函数则应保留业务场景和断言。

### 它解决的问题

当每个测试都重复定位输入框、填充文本和提交时，测试主体会被操作细节淹没，定位器变化也需要逐个文件修复。把稳定且无业务判断的动作集中起来，可以减少重复和维护成本；同时把断言留在测试主体，读者仍能直接看到每个测试验证的业务结果，避免 helper 产生隐藏断言和不透明的假通过。

### 理论基础

#### 1. 三种职责的边界

| 职责 | 典型内容 | 应该放在哪里 |
| --- | --- | --- |
| 测试数据 | `"Buy milk"`、边界文本、参数化列表、重复次数 | 测试或 fixture |
| 动作 | 定位输入框、填充文本、按 Enter | `helpers.py` |
| 断言 | 数量、文本、状态、计数和可见性 | 测试函数 |

fixture 是测试生命周期和前置条件的抽象，例如打开页面或准备两条 Todo；它不是把所有业务验证都藏起来的地方。helper 是动作级复用，不应替测试决定期望结果。

#### 2. 最小代码骨架

~~~python
from playwright.sync_api import Page


def add_todo(page: Page, text: str) -> None:
    todo_input = page.get_by_placeholder("What needs to be done?")
    todo_input.fill(text)
    todo_input.press("Enter")


def test_add_todo(todo_page: Page):
    add_todo(todo_page, "Buy milk")

    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")
    expect(todo_items).to_have_count(1)
    expect(todo_items).to_contain_text("Buy milk")
~~~

这个执行链是：测试提供数据 → helper 执行动作 → 测试读取业务对象并断言。循环仍由测试或 fixture 控制，因此抽取动作不会改变测试覆盖的数据数量或数据集合。

#### 3. 适用场景与边界

适合抽取：多个测试重复、动作语义稳定、动作本身不依赖某个测试专属期望的操作。暂不适合抽取：只出现一次且带有复杂业务判断的流程，或把动作、数据变换和断言混在一起的“万能 helper”。如果不同测试需要不同的期望结果，应共享动作而不是共享断言。

#### 4. 常见错误、反例与假通过

1. 在 helper 中加入 `expect`，会隐藏测试目标，使同一个动作无法自然复用于不同期望。
2. 抽取动作时误改测试数据，例如把参数化变量固定成某个文本、丢失边界输入的空格，可能让测试“通过”但覆盖范围已经缩小。
3. 让 helper 同时创建随机数据、准备 fixture 和断言，会让失败难以复现、职责难以定位。
4. 只看到全套测试通过就认为产品没有缺陷；通过结果只能说明当前收集到的测试在当前环境和覆盖范围内通过。

### 记忆要点

**helper 负责怎么做，fixture 负责准备条件，test 负责表达业务行为和断言；抽取动作，不抽走数据控制和验收标准。**

### 代码落地

本日新增 `test-projects/01-todomvc-ui/tests/helpers.py` 的 `add_todo(page, text)`。`tests/conftest.py` 的 `todo_page_with_todos` fixture 使用它准备两条固定 Todo；新增、完成、边界输入、参数化、定位和等待测试也复用该动作。输入框定位、`fill` 和 `press` 最终只保留在 helper 中，数量、文本、状态和计数断言仍位于测试主体。

全套验证命令得到 `13 passed in 11.10s`。验证结果保存于 `artifacts/day-012/verification.md`。

### 知识验收

1. 为什么 `add_todo` 可以共享，而 `expect` 应保留在具体测试中？
2. fixture 与 helper 的职责有什么不同？
3. 参数化测试和重复 Todo 场景中，为什么数据控制逻辑不能被 helper 吞掉？
4. `13 passed` 能证明什么，不能证明什么？

### 关联产出

- 目标文件：`test-projects/01-todomvc-ui/tests/helpers.py`
- 相关 fixture：`test-projects/01-todomvc-ui/tests/conftest.py`
- 相关测试：`test-projects/01-todomvc-ui/tests/`
- 验证命令：`pytest test-projects/01-todomvc-ui/tests -q`
- 验证证据：`artifacts/day-012/verification.md`

---

## Day 13：小型回归

### 核心知识点

按风险选择回归范围（risk-based regression scope）是根据业务影响、变更关联、历史易错点、状态联动和执行成本，决定哪些测试应进入快速 smoke、完整 regression 或更深的专项验证。回归的目标不是测试数量最大化，而是在合理成本内优先发现高影响的回归。

### 它解决的问题

如果每次只运行少量 smoke，主路径可能保持可用，但边界输入、参数化数据和跨功能状态联动仍可能被破坏；如果每次不加区分地运行所有场景，又会增加反馈时间并降低失败定位效率。风险分层让团队先获得关键路径反馈，再用更完整的集合检查已有功能是否被破坏。

### 理论基础

#### 1. 回归范围的风险维度

| 风险维度 | 选择依据 | 本项目示例 |
| --- | --- | --- |
| 业务影响 | 失败会阻断核心流程 | 新增、完成、删除 Todo |
| 状态联动 | 多个操作连续发生后状态可能不一致 | 完成后筛选、返回 All、删除 |
| 输入边界 | 非典型数据容易暴露规则问题 | 空白、空格、重复和长文本 |
| 变更关联 | 本次修改直接影响的模块优先 | helper、fixture、locator 相关测试 |
| 历史易错 | 曾经失败或环境敏感的路径优先复查 | 浏览器启动、等待和失败证据 |

#### 2. Smoke 与 regression 的边界

smoke 是少量、快速、高价值的关键路径集合，回答“核心功能现在还能不能用”；regression 是覆盖面更广的集合，回答“这次改动有没有破坏已有功能”。smoke 可以是 regression 的子集，但 smoke 全绿不能替代完整回归。

#### 3. 跨功能状态回归的执行链

```text
准备多个业务对象
    ↓
执行状态转换
    ↓
切换筛选或视图
    ↓
验证 DOM 集合与选中状态
    ↓
执行后续操作
    ↓
验证剩余对象与业务计数
```

每个断言都应说明它证明了什么：列表数量和文本证明 DOM 集合正确，筛选器的 `selected` 类证明当前视图状态正确，`todo-count` 证明未完成业务计数同步。它们不能证明未覆盖的浏览器、输入或业务路径没有缺陷。

#### 4. 失败分层与证据

看到 `12 passed, 1 failed` 时，不能直接把失败归因于产品 Bug。应按“环境 → 测试实现 → 测试隔离/数据 → 同步等待 → 产品行为”的顺序检查，并记录命令、完整输出、根因和截图或 Trace（如果测试确实执行到失败阶段）。命令未找到属于执行环境阻塞，不是测试失败。

#### 5. 适用场景与边界

适合按风险选择范围：发布前回归、变更影响较大的模块、测试数量较多且需要分层反馈的工程。它不能替代需求分析、探索式测试、跨浏览器矩阵或性能和安全专项；风险列表本身也需要随着产品变化和历史失败持续维护。

#### 6. 常见错误、反例与假通过

1. 只运行 smoke 并宣称“全量回归通过”，会把未执行的边界和组合场景误当成已验证。
2. 把每个按钮复制到一个长测试中，却没有断言状态、集合和业务计数，无法证明联动一致性。
3. 看到测试失败就写成产品 Bug，忽略服务未启动、浏览器权限、定位器、数据污染和等待问题。
4. 只记录 `14 passed` 而不记录命令和环境，之后无法复现结果或解释执行范围。

### 记忆要点

**回归范围不是越多越好，而是优先覆盖高影响、易变更、易出错和强联动的风险；通过结果只对已执行、已覆盖的场景负责。**

### 代码落地

本日新增 `test-projects/01-todomvc-ui/tests/test_regression.py` 的 `test_regression_state_transition_workflow`。它创建两个 Todo，完成其中一个，依次验证 Active、Completed 和 All 筛选，再删除已完成 Todo，最后检查剩余文本和未完成计数。这个场景没有标记为 smoke，因为它重点覆盖跨功能状态联动而不是最小关键路径。

目标测试得到 `1 passed in 2.26s`，完整回归得到 `14 passed in 12.08s`。初始直接运行 `pytest` 时因当前 PowerShell 找不到命令而未执行测试；激活项目 `.venv` 并使用 `python -m pytest` 后验证成功。

### 知识验收

1. 为什么 smoke 不能完全替代 regression？
2. 选择回归范围时至少应考虑哪些风险维度？
3. 为什么跨功能回归要同时断言 DOM 集合、筛选状态和业务计数？
4. `14 passed` 能证明什么，不能证明什么？
5. 如何区分命令未找到、测试实现失败和产品行为失败？

### 关联产出

- 目标文件：`test-projects/01-todomvc-ui/tests/test_regression.py`
- 验证命令：`python -m pytest test-projects/01-todomvc-ui/tests -q`
- 验证证据：`artifacts/day-013/verification.md`
- 当天记录：`daily-log/day-013.md`

---

## Day 14：阶段验收

### 核心知识点

UI 端到端测试（UI end-to-end test）从用户视角驱动真实页面，验证操作、页面状态和业务结果能否贯通。它适合覆盖高价值、可观察的完整用户链路，但不应被当成唯一测试层；单元、API、集成、性能、安全和兼容性测试仍承担不同职责。

### 它解决的问题

只做底层测试可能无法发现页面定位、交互绑定、DOM 状态和用户可见结果之间的集成问题；只做 UI 测试又会导致执行慢、失败定位困难、边界覆盖成本高。理解 UI 自动化的价值与局限，可以把关键链路放在正确的测试层，并根据失败位置选择正确的排查方向。

### 理论基础

#### 1. UI 端到端测试的执行链

```text
准备业务数据
    ↓
定位用户可见控件
    ↓
执行点击、输入或勾选
    ↓
等待页面达到可观察状态
    ↓
断言 DOM、业务状态和用户可见结果
```

例如 `Clear completed` 不是单纯验证按钮能点击，而是验证点击之后已完成 Todo 消失、未完成 Todo 保留、列表数量和未完成计数保持一致。

#### 2. 测试层的职责边界

| 测试层 | 适合验证 | 不应承担的主要任务 |
| --- | --- | --- |
| 单元测试 | 函数、类、纯业务规则和大量边界 | 浏览器真实交互 |
| API 测试 | 状态码、响应契约、异常和数据规则 | 页面可见性和用户操作链路 |
| 集成测试 | 模块、服务、数据库之间的协作 | 完整用户界面表现 |
| UI 端到端测试 | 高价值用户流程、DOM 状态和跨组件联动 | 取代所有底层测试或性能测试 |
| 性能/安全/兼容性专项 | 吞吐、风险、浏览器和设备差异 | 取代功能正确性断言 |

#### 3. 断言证明什么

在本日测试中：

- 前置列表数量和文本证明测试数据确实准备成功；
- checkbox 选中状态和 `completed` 类证明 Todo 已进入完成状态；
- Completed 项数量为 0 证明目标项消失；
- 剩余文本证明未完成项没有被误删；
- `todo-count` 为 1 证明未完成业务计数同步正确。

这些断言只对当前覆盖的输入、浏览器、页面流程和运行环境负责，不能证明所有未覆盖场景没有缺陷。

#### 4. UI 自动化的主要局限

UI 测试依赖浏览器、被测服务、操作系统进程、网络、定位器和测试数据，因此比单元或 API 测试更慢，也更容易受到环境和同步问题影响。它对内部代码分支不可见，难以经济地覆盖大量异常组合，也不能自然替代性能、安全、兼容性和数据层验证。

#### 5. Flaky 的常见来源与控制

首要风险是页面状态尚未完成更新，测试就开始读取结果。应优先使用 Playwright Locator 操作的自动等待和 `expect` 条件等待，不用固定 `time.sleep`。其他常见来源包括共享页面或 context 造成的数据污染、脆弱 CSS 定位、本地服务不稳定、浏览器驱动权限和外部网络依赖。

#### 6. 失败分层与证据

UI 测试失败只是异常信号，不是产品 Bug 的最终结论。应先定位失败发生在哪一层：环境启动、fixture 前置、测试定位器或断言、数据隔离、同步等待，最后才判断产品行为。若失败实际进入浏览器步骤，应保留截图、Trace 和日志；若在浏览器启动前因权限失败，则应记录调用栈和环境根因。

#### 7. 适用场景与边界

适合使用 UI 端到端测试：登录、核心 CRUD、订单提交、关键筛选和跨组件状态联动等高价值流程。不适合用它独占验证：大量纯规则边界、接口契约、并发性能、安全策略和多浏览器矩阵。合理做法是让 UI、API 和单元测试形成互补的测试组合。

#### 8. 常见错误、反例与假通过

1. 只断言按钮存在或点击不报错，却不检查业务结果，容易得到“交互成功但功能错误”的假通过。
2. 把 `15 passed` 解释成产品零缺陷，忽略测试覆盖范围和环境条件。
3. 看到 `WinError 5` 就修改 locator 或断言，绕过了真正的 Playwright 子进程权限问题。
4. 用固定 sleep 掩盖同步问题，导致本地偶尔通过、CI 偶尔失败。

### 记忆要点

**UI 测试证明用户可观察的关键链路；它是测试组合的一层，不是全部。失败先分层定位，断言必须落到业务结果。**

### 代码落地

本日独立新增 `test-projects/01-todomvc-ui/tests/test_clear_completed.py` 的 `test_clear_completed_todos`。测试复用 `todo_page_with_todos` 准备两条 Todo，将 `Learn pytest` 标记为 Completed，使用用户可见名称定位 `Clear completed`，然后断言 Completed 被清除、`Buy milk` 保留、列表数量为 1、未完成计数为 1。

目标测试在允许启动 Playwright 子进程的环境中得到 `1 passed in 2.10s`，完整回归得到 `15 passed in 12.67s`。受限环境首次运行在 browser fixture 启动阶段遇到 `PermissionError: [WinError 5] Access is denied`；调用栈指向 Windows named pipe 创建，重跑环境修复后测试通过。

### 知识验收

1. UI 自动化最适合验证什么，不能替代哪些测试层？
2. `Clear completed` 测试中的每类断言分别证明什么？
3. `15 passed` 能证明什么，不能证明什么？
4. 为什么页面状态同步是 flaky 的主要来源？
5. 如何区分 Playwright 权限阻塞、测试实现失败和产品行为失败？

### 关联产出

- 目标文件：`test-projects/01-todomvc-ui/tests/test_clear_completed.py`
- 验证命令：`python -m pytest test-projects/01-todomvc-ui/tests -q`
- 验证证据：`artifacts/day-014/verification.md`
- 当天记录：`daily-log/day-014.md`

---

## Day 15：项目初始化

### 核心知识点

理解电商业务流和测试边界（business flow and test scope）是先确定业务目标，再决定一个测试负责哪一段可观察流程。今天的标准登录测试只覆盖“标准用户输入正确凭据并进入商品页”，不把商品、购物车和结账流程混入登录测试。

### 它解决的问题

没有边界的端到端测试会把多个业务模块串在一起，导致执行失败后难以判断问题属于认证、商品页、购物车还是结账；测试也会变慢、重复和难以维护。明确边界让每条测试围绕一个业务行为，并让 URL、页面标题等断言有清晰含义。

### 理论基础

#### 1. 电商业务流与测试切片

```text
登录
  ↓
商品浏览
  ↓
加入购物车
  ↓
填写结账信息
  ↓
提交订单
```

今天只验证第一段：

```text
标准用户 + 正确凭据
  ↓
登录成功
  ↓
进入 inventory.html
  ↓
Products 页面标题出现
```

登录测试的直接业务结果是“用户进入登录后的商品页”；购物车、结账、登出和异常用户应拆成独立测试。

#### 2. URL 与页面内容的双重断言

| 断言 | 主要证明 | 不能单独证明 |
| --- | --- | --- |
| URL 匹配 `/inventory.html` | 浏览器完成预期路由跳转 | 页面内容一定正确渲染 |
| 页面标题为 `Products` | 商品页关键 UI 已经出现 | 所有商品数据、购物车和权限都正确 |

组合断言形成“导航正确 + 目标页面可观察”的最小登录验收，而不是只证明点击动作没有抛异常。

#### 3. 最小初始化结构

```text
test-projects/02-saucedemo-ui/
├── pytest.ini
└── tests/
    ├── conftest.py
    └── test_login.py
```

`pytest.ini` 负责测试发现和 marker 注册；`conftest.py` 负责浏览器、context、page、登录页和账号 fixture；`test_login.py` 负责表达登录业务步骤和断言。Page Object 暂不提前引入，留给后续框架化学习日。

#### 4. Fixture 与注释的维护边界

fixture 集中管理重复的环境准备、资源生命周期和测试隔离；测试函数保留业务行为和验收标准。注释不应重复“这一行调用了 fill”，而应解释“为什么使用环境变量”“为什么每条测试使用独立 context”“为什么登录测试停在商品页”。

#### 5. 失败分层与证据

测试失败必须先定位层级：

```text
操作系统/权限
    ↓
Playwright/浏览器驱动
    ↓
页面加载/网络
    ↓
测试定位器和数据
    ↓
业务断言/产品行为
```

本日的 `WinError 5` 发生在浏览器驱动创建 named pipe 时，测试还没有执行登录；`ERR_CONNECTION_REFUSED` 发生在 TodoMVC `page.goto` 时，原因是本地服务未监听 8080。两者都不能直接判定为产品 Bug。

#### 6. 适用场景与边界

适合拆成独立测试：标准登录、错误密码、锁定用户、商品列表、加入购物车、结账校验和登出。今天不适合覆盖：商品选择、购物车、订单提交、错误用户和会话刷新；这些属于后续业务目标。

#### 7. 常见错误、反例与假通过

1. 一个登录测试继续加入购物车和结账，失败后无法快速定位责任模块。
2. 只断言 URL，可能漏掉 URL 正确但页面空白或前端渲染失败。
3. 只断言按钮点击不报错，不能证明登录后的业务状态正确。
4. 把账号密码硬编码在每个测试中，导致配置变化时需要批量修改。
5. 看到 `WinError 5` 或 `ERR_CONNECTION_REFUSED` 就改业务 locator，反而掩盖了环境根因。

### 记忆要点

**一个测试围绕一个明确业务目标；URL 证明导航，页面内容证明状态；fixture 管环境，注释记录设计意图，失败先定位层级。**

### 代码落地

本日新增 `test-projects/02-saucedemo-ui/tests/test_login.py` 的 `test_standard_user_login`。测试从 `saucedemo_page` fixture 开始，使用 `standard_user_credentials` 读取账号，通过 Username、Password 和 Login 完成登录，最后断言 `/inventory.html` 路由和 `Products` 标题。测试标记为 `smoke` 和 `regression`，分别表示关键路径和完整回归归属。

同时为 Day 1–14 的 TodoMVC Python 代码补充了学习型注释，说明 fixture、helper、定位器、边界数据、等待、状态转换和失败证据的设计原因；注释后的旧测试全套得到 `15 passed in 13.01s`。

SauceDemo 目标测试在授权环境中得到 `1 passed in 4.16s`。首次受限运行遇到 `WinError 5`，旧 TodoMVC 首次回归遇到服务未启动的 `ERR_CONNECTION_REFUSED`；分别通过授权重跑和启动 React dist 静态服务器处理。

### 知识验收

1. 为什么登录测试只到商品页，不继续测购物车？
2. URL 断言和 `Products` 标题断言分别证明什么？
3. `WinError 5` 与 `ERR_CONNECTION_REFUSED` 分别属于什么失败层级？
4. fixture 和注释分别如何帮助测试维护？
5. 为什么注释应解释设计意图，而不是逐行翻译语法？

### 关联产出

- 目标文件：`test-projects/02-saucedemo-ui/tests/test_login.py`
- 初始化文件：`test-projects/02-saucedemo-ui/pytest.ini`、`test-projects/02-saucedemo-ui/tests/conftest.py`
- 历史注释范围：`test-projects/01-todomvc-ui/tests/`
- 验证命令：`python -m pytest test-projects/02-saucedemo-ui/tests/test_login.py::test_standard_user_login -q`
- 验证证据：`artifacts/day-015/verification.md`
- 当天记录：`daily-log/day-015.md`

---

## Day 16：登录异常

### 核心知识点

负向场景（negative scenario）用于验证系统在无效输入或不满足业务条件时，是否以正确方式拒绝操作。高质量的负向测试不只证明“没有成功”，还要同时证明错误反馈正确、成功状态没有出现。

### 它解决的问题

如果只断言登录没有跳转，测试可能在没有提示、页面卡死、前端异常或错误文案不正确时仍然通过。错误信息断言把“系统为什么拒绝”纳入验证范围；成功状态排除则确认无效凭据没有真正绕过认证。

### 理论基础

#### 1. 负向测试的双重证据

登录异常的最小验证模型是：

```text
无效输入
    ↓
系统拒绝操作
    ↓
返回与失败原因匹配的错误反馈
    ↓
不进入登录后的成功页面
```

因此，一条负向 UI 测试通常至少包含两类断言：

| 断言 | 它证明什么 | 它不能单独证明什么 |
| --- | --- | --- |
| 错误容器包含预期文案 | 系统向用户返回了正确失败原因 | 不能证明认证一定被阻止 |
| 不进入 `/inventory.html` | 错误操作没有进入商品页 | 不能证明错误原因和提示文案正确 |

两类证据组合起来，才是“拒绝了，而且拒绝得对”。

#### 2. Authentication 与 Validation

错误密码和空用户名都是登录失败，但它们验证的业务规则不同：

- 身份认证（authentication）：有效用户名配合错误密码时，系统应拒绝不匹配的凭据；
- 输入校验（validation）：用户名为空时，系统应先阻止提交并提示必填字段。

不同业务规则应拆成独立测试。这样一个场景失败时，报告能够直接指向认证逻辑或字段校验，而不会把多个原因混在一个测试函数中。

#### 3. 最小代码骨架

```python
page.get_by_placeholder("Username").fill(username)
page.get_by_placeholder("Password").fill(password)
page.get_by_role("button", name="Login").click()

expect(page.locator('[data-test="error"]')).to_have_text(expected_error)
expect(page).not_to_have_url(re.compile(r"/inventory\.html$"))
```

错误容器应优先使用页面提供的语义化或稳定属性定位。`to_have_text` 断言错误文案，`not_to_have_url` 排除成功路由；两者都要放在点击登录之后，否则可能产生测试一开始就在登录页的假通过。

#### 4. 适用场景与边界

适合用独立负向 UI 测试覆盖：错误密码、空用户名、空密码、锁定用户和其他用户可见的登录拒绝反馈。今天只覆盖错误密码和空用户名，不扩展到锁定用户、会话保持、接口响应或权限矩阵；后者应由后续场景或更合适的 API/集成测试覆盖。

#### 5. 常见错误、反例与假通过

1. 只断言 URL 没有变化：没有验证用户是否得到正确提示。
2. 只搜索整个页面是否包含 `error`：可能匹配到无关文本，无法确认错误类型。
3. 在点击登录前断言“不在商品页”：测试没有真正执行被测行为。
4. 把空用户名和错误密码放进一个函数：一个场景失败后，后续场景可能不执行，报告也难以定位规则。
5. 错误密码测试误用了正确密码：测试名看起来是负向场景，实际验证的却不是目标风险。

### 记忆要点

**负向测试要证明“拒绝了”也要证明“拒绝得对”；Authentication 验证凭据，Validation 验证输入，规则不同就拆成独立测试。**

### 代码落地

Day 16 在 `test-projects/02-saucedemo-ui/tests/test_login.py` 中保留标准登录 smoke 测试，并新增两个回归场景：`test_wrong_password_shows_error` 使用有效用户名和错误密码，验证认证错误文案；`test_empty_username_shows_error` 使用空用户名和有效密码，验证必填校验文案。两个测试都断言不会进入 `/inventory.html`，且代码中保留了说明业务意图的注释。

### 知识验收

1. 为什么负向测试要同时断言错误提示和没有进入商品页？
2. 错误密码与空用户名分别属于 Authentication 还是 Validation？
3. 测试失败时，为什么要先排查环境和测试代码，再判断产品 Bug？

### 关联产出

- 目标文件：`test-projects/02-saucedemo-ui/tests/test_login.py`
- 验证命令：`python -m pytest test-projects/02-saucedemo-ui/tests/test_login.py -q`
- 验证结果：`3 passed in 12.67s`（补充文件末尾换行后重新验证）
- 验证证据：`artifacts/day-016/verification.md`
- 当天记录：`daily-log/day-016.md`

---

## Day 17：特殊用户

### 核心知识点

测试账号不是普通测试数据的替换品，而是风险模型（risk model）的具体载体。每个账号应代表一个明确的用户状态或故障类型，测试断言必须根据该账号的业务预期设计。

### 它解决的问题

如果所有测试都只使用 `standard_user`，只能证明正常用户路径，无法覆盖账号锁定、特殊用户状态或登录后页面异常。把账号与风险绑定，可以让测试回答更具体的问题：系统是否正确拒绝锁定用户？问题用户能否登录？异常发生在认证阶段还是商品页面？

### 理论基础

#### 1. 账号与业务预期的映射

不同账号代表不同的测试策略：

| 账号 | 风险模型 | 主要断言或观察 |
| --- | --- | --- |
| `standard_user` | 正常用户 | 登录成功、进入商品页、核心内容正确 |
| `locked_out_user` | 账号已被锁定 | 错误提示正确、不能进入商品页 |
| `problem_user` | 可登录但登录后页面可能异常 | 先确认进入商品页，再收集异常状态 |
| `performance_glitch_user` | 时序或性能风险 | 后续用专门的等待与性能场景验证 |

因此，`locked_out_user` 不能复用标准用户的成功 URL 断言；它的业务规则是“应该被拒绝”。`problem_user` 则必须先断言登录成功，才能把后续页面现象定位到登录后阶段。

#### 2. 认证结果与异常观察要分层

特殊账号测试可以拆成两层：

```text
选择风险账号
    ↓
执行登录
    ↓
断言账号对应的认证结果
    ↓
如果登录成功，观察后续页面状态
    ↓
保存可重复的事实证据
```

锁定账号的稳定契约是拒绝登录，因此应断言错误容器和非商品页 URL。问题账号的第一层契约是能登录并显示商品页；图片 `alt`、`src`、DOM 或网络状态属于第二层观察数据，不能在尚未确认产品预期时直接当作“应该如此”的断言。

#### 3. 最小观察代码骨架

```python
expect(page).to_have_url(re.compile(r"/inventory\.html$"))
expect(page.locator(".title")).to_have_text("Products")

images = page.locator(".inventory_item_img img")
expect(images).to_have_count(6)
image_states = images.evaluate_all(
    """images => images.map(image => ({
        alt: image.getAttribute("alt"),
        src: image.getAttribute("src"),
    }))"""
)
print(f"observed image states: {image_states}")
```

`to_have_url` 和标题断言证明认证已经到达商品页；数量断言证明图片节点完整渲染；`evaluate_all` 把页面现象转成可比较的事实。它们不能单独证明图片内容符合产品需求，因此需要把观察结果保存到证据文件，并结合对照和预期继续分析。

#### 4. 从异常观察到 Bug 判断

`problem_user` 观察到 6 个商品都指向同一个 `sl-404` 资源时，当前得到的是 Actual Result（实际结果），不是最终 Bug 结论。可靠判断还需要：

1. 与 `standard_user` 在同一环境、同一商品列表做对照；
2. 在独立 context 中重复执行，确认现象稳定复现；
3. 保存截图、Trace、DOM、图片 URL 和网络状态等证据；
4. 确认产品需求或测试账号定义中的 Expected Result（预期结果）；
5. 排除 locator、测试数据、网络和静态资源服务问题。

只有当实际结果稳定、测试和环境没有问题，且与明确预期不一致时，才适合提交产品缺陷候选。

#### 5. 适用场景与边界

适合用特殊账号覆盖：账号锁定、权限状态、数据异常用户、性能迟缓用户和视觉异常用户。今天只覆盖 `locked_out_user` 与 `problem_user`，不提前扩展到购物车、性能专项或完整浏览器矩阵。问题探索阶段可以记录事实；稳定回归阶段再把确认过的业务预期固化为断言。

#### 6. 常见错误、反例与假通过

1. 所有账号都使用“登录后进入商品页”的同一套断言，导致锁定账号的正确拒绝被当成失败。
2. 看到 `problem_user` 页面异常就直接写死错误图片 URL，把当前缺陷误当成长期预期。
3. 只观察问题用户而没有标准用户对照，无法判断异常是否由环境或资源服务造成。
4. 只运行一次就下 Bug 结论，忽略偶发网络失败、缓存和时序问题。
5. 为了让测试变绿而修改断言，没有保存原始现象和复现证据。

### 记忆要点

**账号代表风险，断言跟随业务预期；先确定认证边界，再记录页面异常；`Actual Result` 是证据，不等于 `Product Bug`。**

### 代码落地

Day 17 在 `test-projects/02-saucedemo-ui/tests/test_users.py` 中新增两个回归测试。`test_locked_out_user_cannot_login` 断言锁定提示和未进入商品页；`test_problem_user_login_records_product_state` 先断言问题用户完成登录和商品页加载，再收集 6 个商品图片的 `alt/src`。本次观察显示 6 个图片都指向 `/assets/sl-404-Cq1a9k9X.jpg`，该现象已保存到验证证据，但没有未经需求确认就直接判定为产品 Bug。

### 知识验收

1. 为什么锁定用户和问题用户必须使用不同的断言策略？
2. 为什么问题用户测试要先断言能登录，再收集页面状态？
3. 从异常观察到产品 Bug 结论还缺哪些证据？

### 关联产出

- 目标文件：`test-projects/02-saucedemo-ui/tests/test_users.py`
- 验证命令：`python -m pytest test-projects/02-saucedemo-ui/tests/test_users.py -q`
- 验证结果：`2 passed in 9.41s`（补充文件末尾换行后重新验证）
- 验证证据：`artifacts/day-017/verification.md`
- 当天记录：`daily-log/day-017.md`

---

## Day 18：商品列表

### 核心知识点

列表完整性不是“页面上有一些商品”，而是要验证集合规模、集合成员和每个成员的关键字段。集合断言把页面实际结果与独立的预期数据进行比较，避免只抽查第一项造成假通过。

### 它解决的问题

如果只验证第一件商品，后续商品可能缺失、重复、价格错误或图片缺失而不被发现；如果只验证数量，页面也可能用重复商品凑够数量。分层断言可以把“有多少件”“是哪几件”和“每件数据是否对应”分别验证清楚。

### 理论基础

#### 1. 列表完整性的三层模型

| 层次 | 典型断言 | 证明什么 |
| --- | --- | --- |
| 集合规模 | `expect(items).to_have_count(6)` | 页面渲染了预期数量的商品 |
| 集合成员 | `actual_names == expected_names` | 商品名称集合与预期成员一致，能发现缺失和重复 |
| 元素字段 | 逐个断言名称、价格、图片 | 每个商品内部的字段正确对应 |

三层断言的职责不同，不能用数量断言替代成员断言，也不能用第一件商品的字段替代逐项验证。

#### 2. 集合断言与顺序边界

今天使用集合比较表达“成员完整但不额外要求顺序”：

```python
expected_names = {name for name, _ in EXPECTED_PRODUCTS}
actual_names = set(
    items.locator(".inventory_item_name").all_text_contents()
)
assert actual_names == expected_names
```

如果顺序是明确的业务契约，可以使用有序列表断言，例如 `to_have_text([...])`；如果顺序不是业务要求，集合比较可以避免把无关的排序变化误报成失败。但集合会丢失重复项的计数信息，因此应与数量断言组合使用。

#### 3. 最小代码骨架

```python
items = page.locator(".inventory_item")
expect(items).to_have_count(len(EXPECTED_PRODUCTS))

expected_names = {name for name, _ in EXPECTED_PRODUCTS}
actual_names = set(
    items.locator(".inventory_item_name").all_text_contents()
)
assert actual_names == expected_names

for product_name, expected_price in EXPECTED_PRODUCTS:
    item = items.filter(has_text=product_name)
    expect(item).to_have_count(1)
    expect(item.locator(".inventory_item_price")).to_have_text(expected_price)
```

预期数据必须独立于页面实际数据定义。否则如果直接把页面读出的名称或价格当作预期值，页面错误也可能让测试通过。

#### 4. 图片字段断言的边界

今天验证每件商品都有一张可见图片，并且 `alt` 与 `src` 非空：

```python
product_image = item.locator(".inventory_item_img img")
expect(product_image).to_have_count(1)
expect(product_image).to_be_visible()
expect(product_image).to_have_attribute("alt", re.compile(r".+"))
expect(product_image).to_have_attribute("src", re.compile(r".+"))
```

这证明图片节点存在并具备基本可用属性，但不自动证明图片内容符合视觉需求。若要判断具体图片是否正确，还需要明确的产品预期、资源可访问性或截图/网络证据。

#### 5. 常见错误、反例与假通过

1. 只断言 `items.first()`：后续商品的错误全部可能被漏掉。
2. 只断言数量：重复商品仍可能通过。
3. 只比较名称集合：价格和图片字段仍可能错误。
4. 只比较价格集合：不同商品可能共享同一价格，无法证明价格与商品正确对应。
5. 直接用页面实时结果生成预期：页面错误会被测试当成正确结果。
6. 在顺序不是契约时使用有序断言：排序变化会产生不必要的失败。

### 记忆要点

**数量证明“有多少”，集合证明“是谁”，逐项字段证明“每个成员的数据是否正确对应”；数量与集合组合才能可靠发现缺失和重复。**

### 代码落地

Day 18 在 `test-projects/02-saucedemo-ui/tests/test_inventory.py` 中新增 `test_inventory_list_is_complete`。测试登录标准用户后，使用 `to_have_count` 验证 6 个商品卡片；使用 `set(actual_names) == expected_names` 验证名称集合；再按商品名称定位唯一商品，逐项验证价格、图片可见性以及 `alt/src` 非空。预期商品名称和价格在 `EXPECTED_PRODUCTS` 中独立定义。

### 知识验收

1. 为什么数量为 6 仍不能排除重复商品？
2. 数量、集合和逐项字段断言分别证明什么？
3. 今天代码中的集合断言为什么使用 `set`，而不是直接依赖有序列表？

### 关联产出

- 目标文件：`test-projects/02-saucedemo-ui/tests/test_inventory.py`
- 验证命令：`pytest test-projects/02-saucedemo-ui/tests/test_inventory.py -q`
- 验证结果：`1 passed in 7.11s`
- 验证证据：`artifacts/day-018/verification.md`
- 当天记录：`daily-log/day-018.md`

---

## Day 19：商品详情

### 核心知识点

列表到详情的导航验证（navigation validation）要验证的不只是 URL 变化，还要证明点击的商品身份正确、关键字段在两个页面之间一致，并且返回操作恢复了列表页面。

### 它解决的问题

如果测试只断言进入 `/inventory-item.html`，任何商品详情页都可能让测试通过；如果只验证商品名称，价格等关键数据仍可能错配；如果只验证返回 URL，列表页面也可能没有真正渲染恢复。分层验证可以把导航、身份、数据和页面恢复分别证据化。

### 理论基础

#### 1. 四层证据模型

| 层次 | 典型断言 | 证明什么 |
| --- | --- | --- |
| 导航目的地 | `/inventory-item.html?id=...` | 浏览器进入了带商品标识的详情路由 |
| 商品身份 | 详情名称为 `Sauce Labs Backpack` | 详情页对应刚才选择的目标商品 |
| 数据一致性 | 详情价格等于列表预期价格 | 关键字段没有在列表和详情之间错配 |
| 返回状态 | `/inventory.html` 与 `Products` 标题 | 返回了商品列表路由且列表 UI 重新出现 |

URL 证明“去了哪里”，名称证明“去的是谁”，价格证明“关键数据是否一致”；这些断言不能互相完全替代。

#### 2. 列表到详情再返回的执行链

```text
登录并进入商品列表
    ↓
定位唯一目标商品
    ↓
记录或确认独立的预期名称和价格
    ↓
点击列表中的真实商品元素
    ↓
验证详情 URL、名称和价格
    ↓
点击返回商品列表
    ↓
验证列表 URL 和页面标题
```

测试必须点击列表中的真实元素，而不是直接拼接或访问详情 URL。否则测试绕过了用户实际操作，无法验证列表链接是否把用户带到了正确商品。

#### 3. 最小代码骨架

```python
expected_name = "Sauce Labs Backpack"
expected_price = "$29.99"

inventory_item = page.locator(".inventory_item").filter(
    has_text=expected_name
)
expect(inventory_item).to_have_count(1)
expect(inventory_item.locator(".inventory_item_price")).to_have_text(
    expected_price
)

inventory_item.locator(".inventory_item_name").click()

expect(page).to_have_url(
    re.compile(r"/inventory-item\.html\?id=\d+$")
)
expect(page.locator(".inventory_details_name")).to_have_text(expected_name)
expect(page.locator(".inventory_details_price")).to_have_text(expected_price)

page.get_by_role("button", name="Back to products").click()
expect(page).to_have_url(re.compile(r"/inventory\.html$"))
expect(page.locator(".title")).to_have_text("Products")
```

今天使用独立预期值先验证列表，再验证详情。这与直接从列表 DOM 读取值并把它当作预期不同：后者只能证明两个页面彼此相同，不能单独证明列表数据本身正确。Day 18 的列表完整性测试负责覆盖商品列表的独立正确性，Day 19 负责跨页面一致性。

#### 4. 适用场景与边界

适合在商品、订单、用户或搜索结果等“列表项进入详情”的业务流中使用。至少选择一个有明确业务预期的实体，验证真实点击、详情身份和关键字段。今天只覆盖一个商品和名称/价格，不扩展到所有商品参数化、购物车或结账流程；多商品覆盖可作为后续扩展。

#### 5. 常见错误、反例与假通过

1. 只断言详情 URL：可能打开了错误商品。
2. 直接访问详情 URL：绕过了列表到详情的真实导航链路。
3. 只验证名称不验证价格：商品身份正确但价格仍可能错配。
4. 使用过于宽泛的文本定位：可能点击到错误元素或多个商品。
5. 直接读取列表 DOM 作为唯一预期：列表和详情同时错误时仍可能通过。
6. 返回后只验证 URL：列表页面可能空白或关键 UI 没有恢复。

### 记忆要点

**URL 证明去了哪里，名称证明去的是谁，价格证明数据一致，返回后的 UI 证明业务闭环恢复。**

### 代码落地

Day 19 在 `test-projects/02-saucedemo-ui/tests/test_product_detail.py` 中新增 `test_product_detail_matches_inventory_and_returns`。测试登录标准用户后定位唯一的 `Sauce Labs Backpack`，先验证列表名称和价格，再点击商品名称，验证带 id 的详情路由、详情名称和价格，最后点击 `Back to products` 并验证商品列表 URL 和 `Products` 标题。

### 知识验收

1. 为什么只断言 `/inventory-item.html` 不能证明商品身份正确？
2. 名称断言和价格断言分别证明什么？
3. 为什么返回后要同时验证 URL 和页面标题？
4. 为什么不能把页面实时读出的值无条件当作测试预期？

### 关联产出

- 目标文件：`test-projects/02-saucedemo-ui/tests/test_product_detail.py`
- 验证命令：`pytest test-projects/02-saucedemo-ui/tests/test_product_detail.py -q`
- 验证结果：`1 passed in 4.04s`
- 验证证据：`artifacts/day-019/verification.md`
- 当天记录：`daily-log/day-019.md`

---

## Day 20：商品排序

### 核心知识点

排序验证要从页面提取有序数据，用独立规则计算期望顺序，再比较操作后的实际列表。验证对象是“成员、重复数量和先后顺序”，因此不能把列表转换成集合。

### 它解决的问题

排序控件显示正确选项并不代表商品真正重排；名称正序和倒序包含相同成员，集合比较会让错误顺序通过；价格是业务数值，直接按文本比较会得到错误顺序。完整测试需要同时验证控件状态和数据状态。

### 理论基础

#### 1. 列表与集合的验证边界

```python
expected = ["A", "B", "C"]
actual = ["C", "B", "A"]

assert set(actual) == set(expected)  # 会通过，但顺序错误
assert actual == expected            # 正确发现排序错误
```

`set` 只适合验证成员集合，还会去掉重复项；排序测试必须保留 `list`，让顺序和重复数量都参与比较。

#### 2. 独立计算排序期望

```text
提取原始页面数据
    ↓
测试代码独立计算升序或降序期望
    ↓
选择排序选项
    ↓
等待页面完成重排
    ↓
重新提取实际列表并比较
```

Day 18 已负责验证商品成员和值的正确性；Day 20 以相同数据集为基准，专门验证排序转换。职责拆分可以避免一条测试承担过多失败原因。

#### 3. 价格需要按数值排序

```python
from decimal import Decimal


def parse_price(price_text: str) -> Decimal:
    return Decimal(price_text.strip().removeprefix("$"))


expected_prices = sorted(
    original_prices,
    key=parse_price,
)
```

`key=parse_price` 把函数本身交给 `sorted`，让每个价格文本先转换成 `Decimal` 再比较。货币适合使用十进制精确类型，避免二进制浮点表示带来的精度语义问题。

#### 4. 参数化覆盖四条业务规则

| 选项值 | 字段 | 方向 | 业务规则 |
| --- | --- | --- | --- |
| `az` | 名称 | 升序 | Name A to Z |
| `za` | 名称 | 降序 | Name Z to A |
| `lohi` | 价格 | 升序 | Price low to high |
| `hilo` | 价格 | 降序 | Price high to low |

参数化把数据差异放入测试参数，登录、提取、操作和断言流程只保留一份。pytest 的 `4 passed` 表示四组参数分别通过，不代表整个商品模块没有其他风险。

#### 5. 控件状态与业务数据状态

```python
sort_control.select_option("za")
expect(sort_control).to_have_value("za")
expect(product_names).to_have_text(descending_names)
```

`to_have_value` 证明下拉框选择成功，列表文本断言证明排序业务真正生效。A→Z 是默认状态，因此测试先切换并验证 Z→A 列表，再切回 A→Z；只验证中间控件值仍可能让不重排的列表假通过。

#### 6. 为什么运行测试时可能看不到网页

pytest 只负责组织测试、执行断言并汇总通过或失败；是否打开网页由测试依赖和调用决定：

| 测试类型 | 典型行为 | 是否需要浏览器 |
| --- | --- | --- |
| 纯逻辑/单元测试 | 调用函数并比较返回值 | 否 |
| API 测试 | 发送 HTTP 请求并断言响应 | 否 |
| UI/端到端测试 | 打开页面、定位元素、点击并断言 DOM | 是 |

本项目 `browser` fixture 使用 `playwright.chromium.launch(headless=True)`。因此 SauceDemo UI 测试会在后台启动无头浏览器并执行真实页面操作，只是不会显示可见窗口。调试时可以临时使用 headed 模式观察过程，但稳定自动化执行通常使用 headless。单纯输出 `PASS` 不等于测试成功；必须有断言，并由 pytest 退出状态报告结果。

#### 7. 常见错误、反例与假通过

1. 使用 `set` 比较排序结果，导致顺序和重复项丢失。
2. 把价格字符串直接交给 `sorted`，得到字符顺序而不是金额顺序。
3. 只验证下拉框选项值，不验证商品列表。
4. 对默认 A→Z 状态只做一次无变化选择，排序逻辑损坏也可能通过。
5. 从排序后的页面生成同一份期望，没有独立规则作为判断依据。
6. 看到终端打印 `PASS` 就认为测试有效，但代码没有业务断言。

### 记忆要点

**排序测试要保留列表顺序；名称按文本规则，价格按 `Decimal` 数值；控件值证明选择，列表顺序证明业务生效；看不到窗口不代表没有运行浏览器。**

### 代码落地

Day 20 在 `test-projects/02-saucedemo-ui/tests/test_sorting.py` 中新增参数化测试，使用 `az`、`za`、`lohi`、`hilo` 四组参数覆盖名称和价格升降序。测试提取商品名称与价格，通过字符串排序或 `Decimal` 排序键计算期望，选择排序选项后同时断言控件值和完整列表顺序。知识验收发现 A→Z 场景缺少中间降序列表断言，补充后复验四组用例通过。

### 知识验收

1. 为什么排序测试不能使用 `set`？
2. `key=parse_price` 如何改变价格比较语义？
3. 控件值断言和列表顺序断言分别证明什么？
4. 为什么 Day 20 测试看不到浏览器窗口，却仍然属于 UI 测试？

### 关联产出

- 目标文件：`test-projects/02-saucedemo-ui/tests/test_sorting.py`
- 验证命令：`pytest test-projects/02-saucedemo-ui/tests/test_sorting.py -q`
- 最终验证结果：`4 passed in 10.45s`
- 验证证据：`artifacts/day-020/verification.md`
- 当天记录：`daily-log/day-020.md`

---

## Day 21：加入购物车

### 核心知识点

跨页面状态断言（cross-page state assertion）验证一次操作产生的状态是否在不同页面和组件中保持一致。加入购物车不能只证明按钮被点击，还要验证徽标数量、购物车内部条目、商品身份和关键字段。

### 它解决的问题

点击没有报错不代表商品成功加入；徽标为 1 不代表加入的是目标商品；购物车只有一项也不代表名称和价格正确。组合多个相互独立的观察点，才能证明完整业务状态。

### 理论基础

#### 1. 跨页面状态证据链

```text
列表页确认目标商品和价格
    ↓
在目标商品卡片内点击 Add to cart
    ↓
徽标变成 1
    ↓
进入购物车页面
    ↓
购物车只有一项
    ↓
名称和价格符合独立预期
```

每一层断言回答的问题不同，不能只用一条断言推断整个链路正确。

#### 2. 数量、身份和数据的职责

| 断言 | 证明什么 | 不能单独证明什么 |
| --- | --- | --- |
| 徽标文本为 `1` | 全局购物车数量提示已更新 | 商品身份和购物车内部内容 |
| `.cart_item` 数量为 1 | 购物车内容区域有一个条目 | 这个条目是否是目标商品 |
| 名称为 Backpack | 商品身份正确 | 价格是否正确 |
| 价格为 `$29.99` | 关键业务数据正确 | 购物车是否包含额外商品 |

组合断言才能同时回答“多少”“是谁”和“数据是否正确”。

#### 3. 先定位业务对象，再定位操作

```python
inventory_item = page.locator(".inventory_item").filter(
    has_text=expected_name
)
expect(inventory_item).to_have_count(1)
inventory_item.get_by_role("button", name="Add to cart").click()
```

按钮定位被限制在 Backpack 商品卡片内部，表达的是“给 Backpack 加购”，而不是“点击页面第一个加购按钮”。这能抵抗商品排序和页面位置变化。

#### 4. 独立预期值与跨页面一致性

```python
expected_name = "Sauce Labs Backpack"
expected_price = "$29.99"
```

列表页和购物车页都分别与独立预期比较。若直接读取列表页错误价格并把它当作购物车预期，只能证明两个页面彼此相同，不能证明它们符合业务规则。测试不能让 Actual Result 自己生成唯一的 Expected Result。

#### 5. Browser Context 与状态隔离

本项目每条测试使用新的 Browser Context。Cookie、localStorage、sessionStorage 和登录/购物车浏览状态不会从上一条测试直接继承，因此 `badge == 1` 表达的是当前测试从干净状态加入一件商品，而不是历史购物车数量叠加后的结果。

```text
Test A → Context A → 购物车 0 → 1 → 关闭
Test B → Context B → 购物车 0 → 1 → 关闭
```

如果复用污染状态，第二条测试可能从 1 开始变成 2，失败原因会变成测试之间互相影响，而不是被测功能本身。

#### 6. 最小代码骨架

```python
inventory_item.get_by_role("button", name="Add to cart").click()
expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")

page.locator('[data-test="shopping-cart-link"]').click()
expect(page.locator(".cart_item")).to_have_count(1)

cart_item = page.locator(".cart_item").filter(has_text=expected_name)
expect(cart_item).to_have_count(1)
expect(cart_item.locator(".inventory_item_name")).to_have_text(expected_name)
expect(cart_item.locator(".inventory_item_price")).to_have_text(expected_price)
```

#### 7. 常见错误、反例与假通过

1. 只点击按钮，不验证任何业务结果。
2. 只验证徽标为 1，错误商品也可能通过。
3. 只验证商品项数量，不验证名称和价格。
4. 使用 `.first` 或 `.nth(0)` 点击按钮，使测试依赖页面顺序。
5. 用列表页实时值作为唯一预期，列表和购物车同时错误时仍可能通过。
6. 测试之间复用购物车状态，数量断言被历史数据污染。

### 记忆要点

**徽标证明外部数量，商品项证明内部数量，名称证明是谁，价格证明数据；独立 Context 证明结果只由当前测试产生。**

### 代码落地

Day 21 在 `test-projects/02-saucedemo-ui/tests/test_cart.py` 中新增 `test_add_one_item`。测试使用独立预期名称和价格定位 Backpack 商品卡片，在卡片内部点击 `Add to cart`，验证徽标为 1；进入购物车后验证只有一个商品项，并断言名称为 Backpack、价格为 `$29.99`。

### 知识验收

1. 徽标数量和购物车商品项数量分别证明什么？
2. 为什么两个数量都是 1 仍不能证明加入了正确商品？
3. 为什么不能直接信任列表页实时值作为唯一预期？
4. Browser Context 隔离如何保护购物车数量断言？

### 关联产出

- 目标文件：`test-projects/02-saucedemo-ui/tests/test_cart.py`
- 验证命令：`pytest test-projects/02-saucedemo-ui/tests/test_cart.py::test_add_one_item -q`
- 验证结果：`1 passed in 3.48s`
- 验证证据：`artifacts/day-021/verification.md`
- 当天记录：`daily-log/day-021.md`

---

## Day 22：多商品购物车

### 核心知识点

多商品购物车验证需要同时检查集合数量、商品成员和字段关联。把每件商品表示为 `(名称, 价格)` 元组，可以在验证集合时保留“哪个价格属于哪件商品”的业务关系；使用 `Decimal` 计算合计，为后续结账金额验证准备可靠基准。

### 它解决的问题

只验证徽标和 `.cart_item` 数量，可能让重复或错误商品通过；分别验证名称集合和价格集合，又可能漏掉价格在商品之间串位。测试还需要明确展示顺序是否属于业务契约，避免制造不必要的脆弱断言。

### 理论基础

#### 1. 数量与集合的互补

```python
expect(cart_items).to_have_count(len(selected_products))
assert set(actual_items) == expected_items
```

数量断言证明条目总数，集合断言证明成员及字段关联。集合会去重，因此不能替代数量断言；数量也不能证明具体商品身份。

#### 2. 为什么使用 `(名称, 价格)` 元组

分别比较名称和价格集合会丢失对应关系：

```text
预期：Backpack → $29.99，Bike Light → $9.99
实际：Backpack → $9.99，Bike Light → $29.99
```

两个独立集合可能都相等，但元组集合会发现：

```python
expected_items = {
    ("Sauce Labs Backpack", "$29.99"),
    ("Sauce Labs Bike Light", "$9.99"),
}
```

它把名称和价格绑定成同一个业务记录，能发现字段串位。

#### 3. 合计准备与 Decimal

```python
expected_subtotal = sum(
    parse_price(price)
    for _, price in selected_products
)

actual_subtotal = sum(
    parse_price(price)
    for _, price in actual_items
)

assert actual_subtotal == expected_subtotal
```

今天购物车页面没有验证结账页金额，但合计断言已经证明购物车中的商品价格汇总与选择集合一致，并为后续 Checkout Overview 的金额验证准备了基准。变量本身只是数据准备，`assert` 才把它变成测试证据。

#### 4. 展示顺序的需求边界

如果需求只规定购物车成员和价格，不规定展示顺序，就使用集合比较：

```python
assert set(actual_items) == expected_items
```

如果需求明确规定加入顺序或排序顺序，才保留列表并进行有序比较：

```python
assert actual_items == expected_items_in_order
```

测试应严格验证业务规则，但不应把未定义的实现细节写成失败条件。

#### 5. 最小代码骨架

```python
selected_products = (
    ("Sauce Labs Backpack", "$29.99"),
    ("Sauce Labs Bike Light", "$9.99"),
    ("Sauce Labs Onesie", "$7.99"),
)

for product_name, expected_price in selected_products:
    item = page.locator(".inventory_item").filter(
        has_text=product_name
    )
    item.get_by_role("button", name="Add to cart").click()

cart_items = page.locator(".cart_item")
expect(cart_items).to_have_count(len(selected_products))

actual_items = []
for index in range(cart_items.count()):
    item = cart_items.nth(index)
    actual_items.append((
        item.locator(".inventory_item_name").inner_text(),
        item.locator(".inventory_item_price").inner_text(),
    ))

assert set(actual_items) == set(selected_products)
```

#### 6. 常见错误、反例与假通过

1. 只验证徽标为 3：重复或错误商品仍可能通过。
2. 只验证 `.cart_item` 数量：只能证明有几条，不能证明是哪几条。
3. 分别比较名称集合和价格集合：名称和价格可能在不同商品之间串位。
4. 只比较元组集合不比较数量：重复记录可能被集合去重。
5. 定义 subtotal 但不做断言：准备的数据没有形成测试证据。
6. 没有业务要求却强制展示顺序：导致无意义的脆弱失败。

### 记忆要点

**数量证明多少，元组集合证明是谁及其字段关联，Decimal 合计证明金额汇总；顺序只有在需求要求时才验证。**

### 代码落地

Day 22 在 `test-projects/02-saucedemo-ui/tests/test_cart.py` 中保留 Day 21 单商品测试，并新增 `test_add_multiple_items_and_verify_cart`。测试加入 Backpack、Bike Light 和 Onesie，验证徽标为 3、购物车条目为 3，将实际名称和价格组装成元组集合与预期集合比较，并用 `Decimal` 断言实际合计等于预期合计。

### 知识验收

1. 为什么数量和元组集合必须组合使用？
2. 价格互换时，哪条断言可以发现字段串位？
3. 为什么合计变量必须配合 `assert` 才有测试价值？
4. 什么情况下才应该把购物车展示顺序作为断言？

### 关联产出

- 目标文件：`test-projects/02-saucedemo-ui/tests/test_cart.py`
- 验证命令：`pytest test-projects/02-saucedemo-ui/tests/test_cart.py -q`
- 验证结果：`2 passed in 8.43s`
- 验证证据：`artifacts/day-022/verification.md`
- 当天记录：`daily-log/day-022.md`

---

## Day 23：移除商品

### 核心知识点

移除测试要验证状态回退（state rollback），而不是只验证 Remove 按钮被点击。商品应从“未加入”进入“已加入”，再经过移除回到“未加入”；列表页按钮、购物车徽标和购物车实际条目应共同反映这个最终状态。幂等思路（idempotency）要求重复表达同一个移除意图时，最终状态仍保持为“商品不在购物车”，但 SauceDemo UI 在第一次移除后会把 Remove 变为 Add to cart，因此不能把连续点击同一个 Remove 按钮当作有效的 UI 幂等测试。

### 它解决的问题

只断言 `click()` 不报错，最多证明操作找到了按钮并完成了交互，不能证明业务状态已经改变。只检查列表按钮、只检查徽标或只检查购物车条目，也可能遗漏局部状态与全局状态不同步的问题。状态回退测试通过多个观察点确认：商品 UI 状态、购物车计数和购物车内容共同回到空购物车状态。

### 理论基础

#### 1. 状态转换与后置条件

```text
未加入
  ↓ Add to cart
已加入：按钮 Remove，徽标 1，购物车有 1 条
  ↓ Remove
已移除：按钮 Add to cart，徽标消失，购物车有 0 条
```

测试的核心是最后一个状态，而不是中间的点击动作。每个后置条件证明的层面不同：

| 观察点 | 断言 | 证明什么 | 不能单独证明什么 |
| --- | --- | --- | --- |
| 商品卡片 | `Remove` → `Add to cart` | 当前商品的列表页状态回退 | 购物车实际内容一定为空 |
| 购物车徽标 | `1` → 不存在/`0` | 全局计数回退 | 具体商品一定已消失 |
| 购物车条目 | `.cart_item` 为 `0` | 购物车内容为空 | 列表页按钮一定同步恢复 |

把三类断言组合起来，才有较完整的跨页面状态证据。

#### 2. 操作成功与业务结果成功

```python
cart_item.get_by_role("button", name="Remove").click()

expect(page.locator(".cart_item")).to_have_count(0)
expect(
    page.locator('[data-test="shopping-cart-badge"]')
).to_have_count(0)
```

第一行是动作（action），后两行是结果（result）。Playwright 的点击没有抛出异常，只说明元素可定位并完成了点击；只有后置断言通过，才说明移除后的业务状态符合预期。

#### 3. 幂等思路的适用边界

幂等操作的重点是：第一次执行改变状态，之后再次表达同一意图不会继续破坏系统，最终状态保持稳定。例如 API 的 `DELETE /cart/items/{id}` 通常可以重复调用而仍然得到“该商品不存在”。

在本日 UI 中，第一次移除后按钮变为 `Add to cart`，页面不再提供第二个 Remove 操作。因此本日通过两个不同的移除入口验证相同的最终状态，不把不存在的第二次 Remove 点击硬塞进测试。若要直接验证重复删除，应在有明确接口契约时补充 API 测试，或先定义 UI 对“已移除商品再次移除”的业务交互。

#### 4. 最小代码骨架

```python
item = page.locator(".inventory_item").filter(
    has_text="Sauce Labs Backpack"
)
item.get_by_role("button", name="Add to cart").click()

item.get_by_role("button", name="Remove").click()

expect(item.get_by_role("button", name="Add to cart")).to_be_visible()
expect(
    page.locator('[data-test="shopping-cart-badge"]')
).to_have_count(0)
```

#### 5. 适用场景与边界

- 适用：加入/移除购物车、启用/禁用、收藏/取消收藏、提交/撤销等有明确前后状态的业务操作。
- 适用：同一业务状态可从多个页面入口改变时，用跨入口测试检查状态一致性。
- 不适用：没有定义最终状态的纯装饰性交互；不要把点击次数或 DOM 瞬间变化当成业务契约。
- 对幂等性的验证应依据产品契约选择 UI 或 API 层，不要假设所有 UI 按钮都能安全重复点击。

#### 6. 常见错误、反例与假通过

1. 只写 `remove_button.click()`：没有业务结果断言，移除失败也可能通过。
2. 只检查徽标消失：计数归零不等于能证明具体商品已从内容中消失。
3. 只检查列表按钮恢复：局部 UI 可能恢复，但购物车数据仍可能残留。
4. 连续点击同一个 Remove 按钮测试幂等：SauceDemo 第一次移除后该按钮已不存在，测试前提不成立。
5. 复用上一条测试的购物车状态：没有独立 Browser Context 时，数量变化可能来自历史数据污染。

### 记忆要点

**点击是动作，状态断言才是证据；移除测试要证明商品、徽标和购物车内容同步回退，幂等测试必须服从真实的 UI 或 API 契约。**

### 代码落地

Day 23 新增 `test_cart_remove.py`，使用同一个标准用户 fixture 隔离两条测试。第一条从商品列表加入并移除 Backpack，验证卡片按钮恢复、徽标消失和购物车为空；第二条从购物车移除 Backpack，验证商品名称与价格、购物车条目归零、徽标消失，并返回列表确认按钮恢复为 `Add to cart`。两个入口都落实了“未加入 → 已加入 → 已移除”的状态回退。

### 知识验收

1. 为什么按钮、徽标和 `.cart_item` 数量需要组合验证？
2. 为什么 `click()` 没有报错不能证明移除成功？
3. 今天两个测试分别从哪里移除商品？它们共同验证了什么状态转换？
4. 为什么本日没有连续点击同一个 Remove 按钮来声称验证幂等性？

### 关联产出

- 目标文件：`test-projects/02-saucedemo-ui/tests/test_cart_remove.py`
- 验证命令：`pytest test-projects/02-saucedemo-ui/tests/test_cart_remove.py -q`
- 验证结果：`2 passed in 25.68s`
- 验证证据：`artifacts/day-023/verification.md`
- 当天记录：`daily-log/day-023.md`

---

## Day 24：结算校验

### 核心知识点

表单验证与字段组合（form validation and field combinations）要求把“哪个字段缺失”“应该返回什么提示”和“失败后页面是否保持在当前表单”作为一个输入—结果契约来验证。对多个必填字段，使用单变量隔离（one-variable-at-a-time）：每个用例只清空一个字段，其余字段保持有效。

### 它解决的问题

如果同时清空姓名、姓氏和邮编，页面通常只显示第一个失败规则。测试即使通过，也只能证明某个校验顺序被触发，不能证明三个字段各自的规则都正确。只断言错误容器可见或 URL 没变，也可能让错误提示错位、错误类型错误或意外导航的假通过漏过去。

### 理论基础

#### 1. 单变量隔离与字段—错误映射

对三个必填字段分别构造独立输入：

| 用例 | firstName | lastName | postalCode | 预期错误 |
| --- | --- | --- | --- | --- |
| 缺失姓名 | 空 | 有效 | 有效 | `Error: First Name is required` |
| 缺失姓氏 | 有效 | 空 | 有效 | `Error: Last Name is required` |
| 缺失邮编 | 有效 | 有效 | 空 | `Error: Postal Code is required` |

这种设计把失败原因归因到一个字段。参数化（parameterization）可以复用同一套动作和断言，但每行数据必须同时保存字段定位和预期错误，不能只保存一组空值。

#### 2. 三层结果证据

点击 Continue 是动作，不是业务结果。一次必填校验至少应组合三层证据：

1. 字段输入层：目标字段为空，其余字段是有效值，证明测试前置符合意图。
2. 反馈层：错误容器精确等于目标字段的错误文案，证明规则映射正确。
3. 流程层：页面仍在 `/checkout-step-one.html`，证明校验失败阻止了进入下一步。

精确错误文案能证明“系统指出了哪个原因”，但不能单独证明没有发生导航；URL 不变能证明流程停留，但不能证明提示内容正确。两者需要组合。

#### 3. 校验失败与认证失败的边界

必填校验通常发生在已经登录并进入结算表单之后；错误密码则属于认证失败，发生在登录阶段。测试前置和断言应把两种失败分开，否则同一个“没有进入下一页”可能被错误归因到错误的业务层。

#### 4. 最小代码骨架

```python
CASES = [
    ("firstName", "Error: First Name is required"),
    ("lastName", "Error: Last Name is required"),
    ("postalCode", "Error: Postal Code is required"),
]

@pytest.mark.parametrize("missing_field, expected_error", CASES)
def test_required_field(page, missing_field, expected_error):
    for field_name, valid_value in VALID_VALUES.items():
        page.locator(f'[data-test="{field_name}"]').fill(
            "" if field_name == missing_field else valid_value
        )

    page.get_by_role("button", name="Continue").click()
    expect(page.locator('[data-test="error"]')).to_have_text(expected_error)
    expect(page).to_have_url(re.compile(r"/checkout-step-one\.html$"))
```

#### 5. 适用场景与边界

- 适用：姓名、地址、支付信息等多个独立必填字段；每个字段有明确错误文案的表单。
- 适用：希望用少量参数化代码覆盖同一规则族，同时保留每个字段的可读失败 ID。
- 不适用：字段之间存在真实组合规则时强行单变量隔离；例如“结束日期必须晚于开始日期”需要专门的跨字段组合用例。
- 不适用：没有稳定错误契约的页面只做精确文案断言；应先确认产品允许的语义或使用更稳定的错误标识。

#### 6. 常见错误、反例与假通过

1. 三个字段全部留空：通常只暴露第一个错误，后续字段没有被独立验证。
2. 只断言错误容器可见：任意错误都可能通过，字段映射错位不会被发现。
3. 只断言 URL 没变：能证明没有前进，但不能证明提示说明了正确原因。
4. 从页面当前文本生成 Expected：页面和预期可能一起错误，形成自证式假通过。
5. 复用上一条测试的表单或购物车状态：上下文污染会让字段校验结果失去可归因性。

### 记忆要点

**一个用例只缺一个字段；精确提示证明原因，未导航证明流程被拦截，二者组合才是可靠的必填校验证据。**

### 代码落地

Day 24 在 `test-projects/02-saucedemo-ui/tests/test_checkout_validation.py` 中用 `open_checkout_form` 统一登录、加购 Backpack 并进入结算信息页；用 `CHECKOUT_REQUIRED_FIELD_CASES` 参数化三个字段—错误映射；每条用例先填充 `VALID_CHECKOUT_VALUES`，只清空目标字段，点击 Continue 后断言精确错误文案和 `checkout-step-one.html` URL。

### 知识验收

1. 为什么三个字段同时为空不能证明三个必填规则都正确？
2. 单变量隔离在本日的代码中对应哪一段逻辑？
3. 精确错误文案和未导航断言分别证明什么，为什么需要组合？
4. 必填校验与错误密码登录分别属于哪个业务层？

### 关联产出

- 目标文件：`test-projects/02-saucedemo-ui/tests/test_checkout_validation.py`
- 验证命令：`pytest test-projects/02-saucedemo-ui/tests/test_checkout_validation.py -q`
- 验证结果：`3 passed in 17.74s`
- 验证证据：`artifacts/day-024/verification.md`
- 当天记录：`daily-log/day-024.md`

---

## Day 25：结算概览

### 核心知识点

金额与业务计算断言（money and business-calculation assertions）要求先把页面货币文本解析为精确的 `Decimal`，再用独立预期和业务不变量验证小计、税费与总价。金额不是普通字符串，也不适合优先使用二进制浮点数进行精确相等比较。

### 它解决的问题

直接对 `"$29.99"` 和 `"$2.40"` 做运算会得到字符串拼接；使用 `float` 可能因为二进制近似产生 `0.30000000000000004` 一类误差。只断言金额文本存在，或只复制页面实际值生成 Expected，也无法证明业务计算正确。

### 理论基础

#### 1. 金额解析与 Decimal

页面展示文本通常包含货币符号和标签，例如 `Item total: $29.99`。测试需要先提取货币值，再构造 `Decimal`：

```python
from decimal import Decimal
import re

MONEY_PATTERN = re.compile(r"\$([0-9]+(?:\.[0-9]{2})?)")

def parse_money(text: str) -> Decimal:
    match = MONEY_PATTERN.search(text)
    if match is None:
        raise ValueError(f"金额文本缺少货币值: {text!r}")
    return Decimal(match.group(1))
```

`Decimal("0.1") + Decimal("0.2")` 保留十进制金额语义；不要先转成 `float` 再转回 `Decimal`，否则近似误差已经进入结果。

#### 2. 独立预期与业务不变量

本日的最小证据链是：

```text
独立商品价格预期 → 预期小计
页面小计、税费、总价 → Decimal
总价 == 小计 + 税费
```

小计要与独立的商品价格预期比较，防止页面错误值同时成为 Expected。税费至少应是可解析的正金额；税率只有在产品规则明确时才适合写成固定断言。总价不变量验证的是金额关系，而不是某个页面文案是否存在。

| 断言 | 证明什么 | 不能单独证明什么 |
| --- | --- | --- |
| 实际小计等于独立预期 | 购物车商品金额汇总与选择一致 | 税费和总价计算正确 |
| 税费可解析且为正 | 页面提供了有效收费金额 | 税率一定符合某个固定百分比 |
| 总价等于小计加税费 | 结算金额的加法关系成立 | 商品身份或小计来源正确 |

#### 3. 定位器也属于金额证据的一部分

金额断言之前必须定位到正确的业务元素。SauceDemo 概览页使用 `.summary_subtotal_label`、`.summary_tax_label` 和 `.summary_total_label`，文本还包含 `Item total:`、`Tax:`、`Total:` 标签。定位器错误会在金额逻辑执行前超时；解析函数也必须适配真实文本格式。

#### 4. 适用场景与边界

- 适用：商品小计、税费、折扣、运费、订单总价等十进制金额关系。
- 适用：页面展示文本带货币符号或说明标签，需要统一提取金额。
- 适用：产品规则明确时，使用 `Decimal` 验证固定税率、折扣或四舍五入规则。
- 不适用：用 `float` 做金额精确相等断言；应改为 `Decimal` 或明确的量化比较规则。
- 不适用：没有独立业务预期时把页面实际值复制为 Expected；这会失去发现数据错误的能力。

#### 5. 常见错误、反例与假通过

1. `"$29.99" + "$2.40"`：得到字符串拼接，不是金额加法。
2. `0.1 + 0.2 == 0.3`：二进制浮点近似可能导致精确比较失败。
3. 只断言金额文本非空：无法证明数值可以计算或关系正确。
4. 用页面实际小计计算 Expected 总价：页面全错时测试可能一起通过。
5. 使用错误的 `.summary_subtotal` 定位器：测试在业务断言前超时，根因是 DOM 契约不匹配而不是金额业务失败。

### 记忆要点

**金额先解析为 Decimal，预期来自独立数据，最后用小计、税费和总价的不变量证明业务计算关系。**

### 代码落地

Day 25 在 `test-projects/02-saucedemo-ui/tests/test_checkout_summary.py` 中新增 `parse_money` 和 `open_checkout_summary`，登录并加入 Backpack 后进入订单概览页。测试使用独立 `$29.99` 预期验证小计，读取带标签的实际小计、税费和总价并转成 `Decimal`，断言税费为正且 `total == subtotal + tax`。首次运行发现概览页实际类名带 `_label` 且文本有标签前缀，修复定位器和金额提取后复验通过。

### 知识验收

1. 为什么金额不能直接按字符串相加，也不应优先用 `float` 精确比较？
2. 为什么小计的 Expected 必须来自独立商品数据？
3. `total == subtotal + tax` 证明了什么，不能证明什么？
4. 本日首次失败的根因是什么，修复了哪两个层面？

### 关联产出

- 目标文件：`test-projects/02-saucedemo-ui/tests/test_checkout_summary.py`
- 验证命令：`pytest test-projects/02-saucedemo-ui/tests/test_checkout_summary.py -q`
- 验证结果：首次 `1 failed in 34.10s`；修复后 `1 passed in 4.67s`
- 验证证据：`artifacts/day-025/verification.md`
- 当天记录：`daily-log/day-025.md`

---

## Day 26：完整下单

### 核心知识点

关键端到端业务流（critical end-to-end business flow）要围绕用户目标串联多个页面和状态转换，并在关键节点验证业务结果。完整下单不是只检查最后一个 URL，而是证明“登录成功 → 商品进入购物车 → 结算数据提交 → 订单完成 → 购物车清空”这条链路贯通。

### 它解决的问题

单页测试可以证明局部功能，但无法发现跨页面状态没有传递、结算对象错位、订单完成后购物车未清理等集成问题。只断言 Finish 点击不报错或只断言 `/checkout-complete.html`，也可能让导航假通过而漏掉实际业务状态错误。

### 理论基础

#### 1. 业务状态转换与检查点

```text
登录页
  ↓ Login
商品列表：标准用户已登录
  ↓ Add to cart
购物车：Backpack、徽标 1、实际条目 1
  ↓ Checkout + 填写信息
订单概览：商品和金额可观察
  ↓ Finish
订单完成：标题和成功文案正确
  ↓ 检查购物车
购物车为空：徽标消失、.cart_item 为 0
```

每个检查点都应回答“当前业务状态是什么”，而不是只回答“点击是否完成”：

| 检查点 | 主要断言 | 证明什么 |
| --- | --- | --- |
| 登录后 | inventory URL、Products 标题 | 身份验证后进入商品业务 |
| 加购后 | 商品作用域、徽标、购物车条目 | 指定商品真的进入购物车 |
| 结算概览 | checkout-step-two URL、页面标题 | 购物车成功进入结算流程 |
| 完成后 | 完成 URL、标题、成功文案 | 订单完成状态在页面上可观察 |
| 清理后 | 徽标不存在、`.cart_item` 为 0 | 完成订单后的购物车业务状态已清空 |

#### 2. 导航证据与业务证据

URL 证明“到了哪里”，页面标题和成功文案证明“页面呈现了什么”，购物车徽标和实际条目证明“跨页面业务状态是什么”。它们的证明范围不同，不能互相替代：

```python
expect(page).to_have_url(COMPLETE_URL)
expect(page.locator(".title")).to_have_text("Checkout: Complete!")
expect(page.locator(".complete-header")).to_have_text(
    "Thank you for your order!"
)
expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_count(0)
```

#### 3. E2E 与局部测试的边界

E2E 测试应覆盖一条高价值代表性路径和少量关键检查点；字段必填、金额解析、购物车移除等细节由更聚焦的测试承担。E2E 不需要重复所有边界数据，否则失败定位和维护成本都会变差。它的价值在于验证模块之间的连接和最终业务结果。

#### 4. 隔离与可归因性

每条 E2E 用例使用独立 Browser Context，从登录页开始建立购物车状态。不能依赖上一条测试残留的商品或徽标，否则即使本条流程没有正确加购，测试也可能因为历史状态而通过。前置 helper 可以减少重复，但最终测试仍应保留清晰的业务检查点。

#### 5. 适用场景与边界

- 适用：登录—购买、注册—激活、搜索—下单、支付—回执等跨页面核心路径。
- 适用：需要验证多个模块之间状态传递和最终业务后置条件的场景。
- 不适用：把所有输入边界、错误组合都塞进一条 E2E；这些应由更快、更聚焦的测试覆盖。
- 不适用：没有明确业务终态的纯 UI 装饰交互；应先定义成功和失败后置条件。
- 当外部支付、邮件或第三方服务不稳定时，应通过契约测试、模拟或分层测试补充，不把不可控依赖全部压在 E2E 上。

#### 6. 常见错误、反例与假通过

1. 只断言 `/checkout-complete.html`：只能证明导航，不能证明成功文案或购物车清理。
2. 只断言 Finish 点击没有异常：没有业务结果证据。
3. 只检查购物车徽标：数量归零不等于实际条目已经清空。
4. 复用上一条测试的购物车：历史状态污染当前业务链路。
5. 在 E2E 中重复所有单字段和金额边界：测试目标不清晰，失败定位困难。
6. 前置步骤完全没有检查点：最终失败只能知道链路某处断裂，不能定位阶段。

### 记忆要点

**E2E 证明的是用户目标贯通；URL 证明导航，页面文案证明可观察结果，跨页面后置断言证明业务状态。**

### 代码落地

Day 26 在 `test-projects/02-saucedemo-ui/tests/test_checkout_e2e.py` 中新增 `open_order_summary` 前置，独立完成登录、Backpack 加购、购物车确认、结算信息填写和订单概览检查。`test_complete_checkout_order` 点击 Finish 后验证完成页 URL、标题、`Thank you for your order!` 成功文案，并进入购物车确认徽标消失且 `.cart_item` 数量为 0。

### 知识验收

1. 为什么只断言完成页 URL 不能充分证明订单成功？
2. 加购后为什么要同时检查商品身份、徽标和购物车条目？
3. 订单完成后为什么还要验证购物车状态？
4. 哪些细节适合放在局部测试，而不应全部重复到 E2E？

### 关联产出

- 目标文件：`test-projects/02-saucedemo-ui/tests/test_checkout_e2e.py`
- 验证命令：`pytest test-projects/02-saucedemo-ui/tests/test_checkout_e2e.py -q`
- 验证结果：`1 passed in 4.47s`
- 验证证据：`artifacts/day-026/verification.md`
- 当天记录：`daily-log/day-026.md`

---

## Day 27：登出和会话

### 核心知识点

认证状态和直接访问（authentication state and direct access）要求把“页面看起来退出了”和“受保护资源真的拒绝了无会话访问”分开验证。登出测试不仅要检查回到登录页，还要在会话失效后直接访问受保护的 `/inventory.html`，确认系统重新要求认证。

### 它解决的问题

只断言 Logout 后回到登录页，最多证明一次页面导航；Cookie、localStorage 或服务端会话可能仍然有效，用户手动输入受保护 URL 仍可能看到商品页。直接访问检查可以发现 UI 已退出但权限没有撤销的安全和业务缺陷。

### 理论基础

#### 1. 认证状态转换

```text
未认证
  ↓ Login
已认证：inventory.html 可访问
  ↓ Logout
未认证：登录页可见
  ↓ 直接访问 inventory.html
仍未认证：被重定向到登录页，商品页不可见
```

两个后置条件的证明范围不同：

| 检查点 | 断言 | 证明什么 |
| --- | --- | --- |
| Logout 后 | 根路径、登录表单可见 | 页面退出行为和登录入口恢复 |
| 直接访问受保护 URL | 仍在登录页、登录表单可见 | 会话失效且访问控制生效 |

两者必须组合；前者不能替代后者。

#### 2. 页面状态与权限状态

页面跳转是可观察的 UI 结果，认证状态则可能存储在 Cookie、localStorage、sessionStorage 或服务端会话中。测试不需要直接读取所有存储实现，而是通过访问控制的外部行为验证最终契约：无认证状态不能访问受保护商品页。

#### 3. 直接访问不是绕过测试

`page.goto(".../inventory.html")` 模拟用户在地址栏输入受保护 URL 或从书签打开页面。它与点击导航不同，专门覆盖“没有经过登录入口，系统是否仍检查权限”的边界。若应用返回登录页并显示登录表单，说明保护规则在直接访问路径上生效。

#### 4. 最小代码骨架

```python
page.get_by_role("button", name="Open Menu").click()
page.get_by_role("link", name="Logout").click()

expect(page).to_have_url(LOGIN_URL)
expect(page.get_by_placeholder("Username")).to_be_visible()

protected_url = page.url.rstrip("/") + "/inventory.html"
page.goto(protected_url)

expect(page).to_have_url(LOGIN_URL)
expect(page.get_by_placeholder("Username")).to_be_visible()
```

#### 5. 适用场景与边界

- 适用：登出、会话过期、刷新 Token 失败、角色降权和受保护页面直接访问。
- 适用：需要验证 UI 退出动作与实际访问控制同时成立的 Web 应用。
- 不适用：只依赖前端路由隐藏页面的应用；还应在 API 或服务端层验证未授权响应。
- 不适用：没有定义受保护资源和未认证目标状态的场景；应先明确访问控制契约。
- 多标签页、刷新、过期时间和跨域 SSO 可能有额外会话边界，应按产品契约增加独立场景。

#### 6. 常见错误、反例与假通过

1. 只检查 Logout 后 URL：页面跳转成功不等于会话失效。
2. 只检查登录表单可见：前端界面可能显示登录页，但直接访问仍能读取受保护数据。
3. 不做直接访问：遗漏地址栏、书签和刷新等受保护路由入口。
4. 复用其他测试的登录状态：当前测试可能一开始就已认证，无法证明 Logout 的真实效果。
5. 只验证 URL，不验证登录表单或商品内容：错误重定向或空白页也可能让 URL 断言通过。

### 记忆要点

**登出不仅要看起来回到登录页，还要证明失效会话无法直接访问受保护资源；页面行为和访问控制必须分层验证。**

### 代码落地

Day 27 在 `test-projects/02-saucedemo-ui/tests/test_session.py` 中用 `login_as_standard_user` 建立统一已认证前置；测试执行 Logout 后验证登录表单恢复，再用当前根 URL 构造 `/inventory.html` 直接访问，验证仍被重定向到登录页。每条测试使用独立 Browser Context，避免会话历史污染。

### 知识验收

1. 回到登录页和直接访问受保护 URL 分别证明什么？
2. 为什么只验证 Logout 后 URL 会产生假通过？
3. 直接访问 `/inventory.html` 覆盖了哪种用户行为边界？
4. 为什么会话测试需要独立 Browser Context？

### 关联产出

- 目标文件：`test-projects/02-saucedemo-ui/tests/test_session.py`
- 验证命令：`pytest test-projects/02-saucedemo-ui/tests/test_session.py -q`
- 验证结果：`1 passed in 5.39s`
- 验证证据：`artifacts/day-027/verification.md`
- 当天记录：`daily-log/day-027.md`

---

## Day 28：Page Object 登录页

### 核心知识点

页面对象（Page Object）是页面操作接口：集中封装页面 locator 和 UI 动作，让测试文件保留场景、数据和业务结果断言。今天的边界是“Page Object 负责怎么操作，测试负责验证什么”。

### 它解决的问题

如果每个测试都直接查找用户名框、密码框和登录按钮，页面结构变化会导致重复修改，测试主体也会被操作细节淹没。把这些变化点集中到 `LoginPage`，可以减少重复并保持业务意图可读；同时把断言留在测试中，避免一个登录动作强制假设所有用户都应该成功进入商品页。

### 理论基础

#### 1. 页面对象与测试的职责边界

| 层次 | 负责内容 | 不负责内容 |
| --- | --- | --- |
| `LoginPage` | locator、输入、点击、读取页面元素 | 决定某个测试场景是否成功 |
| `test_login.py` | 测试数据、场景编排、URL/文案/状态断言 | 重复实现登录页的机械操作 |

测试可以读成：

```text
给定登录页和账号数据
    当调用 LoginPage.login(username, password)
    那么测试验证该场景的业务结果
```

#### 2. 最小代码骨架

```python
from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error_message = page.locator('[data-test="error"]')

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
```

测试调用页面对象后，仍然表达业务预期：

```python
login_page.login(username, password)
expect(page).to_have_url(re.compile(r"/inventory\.html$"))
```

这里的 URL 断言证明导航结果，不能单独证明所有商品页内容；错误密码场景则应断言精确错误文案和未进入商品页。

#### 3. 断言为什么留在测试中

`login()` 是可复用动作，不能假定调用者一定是标准用户。若把“必须出现 Products”写入动作，错误密码、锁定用户和其他负向场景就无法复用同一个动作。测试保留 `expect()`，可以让每个场景明确表达自己的预期，并在失败时显示对应业务上下文。

#### 4. 适用场景与边界

- 适用：多个测试共享同一页面的定位器和机械操作，且页面结构变化需要集中维护。
- 适用：登录、商品列表、购物车和结算等具有清晰页面职责的对象。
- 不适用：把整个业务流程和所有断言塞进一个“上帝对象”；跨页面流程仍应由测试或更高层业务流程编排。
- 不适用：为了抽象而抽象只有一次使用的简单操作；抽象必须降低重复或提高可读性。
- 页面对象可以提供页面元素和动作，但业务规则、测试数据和场景结论应保持在测试层。

#### 5. 常见错误、反例与假通过

1. 把对象初始化写进函数参数列表：fixture 参数只能声明依赖，页面对象必须在函数体内创建。
2. 在页面对象中硬编码成功断言：负向账号无法复用同一个登录动作。
3. 测试仍直接使用登录 locator：页面对象没有真正成为唯一操作入口。
4. 从错误的工作目录运行：模块搜索路径不含项目目录时会出现 `ModuleNotFoundError`，这不是业务断言失败。
5. 把 Playwright `WinError 5` 当成产品缺陷：应先分层确认代码解析、模块导入和浏览器进程权限。

### 记忆要点

**Page Object 封装“怎么做”，测试文件保留“做什么和应该得到什么”；动作可复用，业务断言按场景决定。**

### 代码落地

Day 28 在 `test-projects/02-saucedemo-ui/pages/login_page.py` 中集中定义用户名、密码、登录按钮和错误提示 locator，并提供 `login(username, password)`。`test_login.py` 的标准登录、错误密码和空用户名场景都通过 `LoginPage` 操作，继续在测试中断言 URL、标题、错误文案和未导航状态。

### 知识验收

1. `LoginPage` 应负责什么，`test_login.py` 应保留什么？
2. 为什么 `login()` 不应强制断言 Products 页面？
3. 语法错误、`pages` 导入错误和 Playwright `WinError 5` 分别属于哪一层？
4. 如何按“代码解析 → 模块导入 → 测试环境 → 测试步骤 → 业务断言”排查失败？

### 关联产出

- 目标文件：`test-projects/02-saucedemo-ui/pages/login_page.py`、`test-projects/02-saucedemo-ui/tests/test_login.py`
- 验证命令：`pytest test-projects/02-saucedemo-ui/tests/test_login.py -q`
- 验证结果：项目目录运行 `3 passed`；按仓库根目录路径临时设置项目模块路径后 `3 passed`；清理注释后复验 `3 passed`。
- 验证证据：`artifacts/day-028/verification.md`
- 当天记录：`daily-log/day-028.md`

---

## Day 29：Page Object 商品页

### 核心知识点

减少重复选择器和操作，要求把同一页面反复出现的 locator、页面动作和数据读取集中到有明确职责的 Page Object，同时让测试保留测试数据、业务流程和断言。

### 它解决的问题

商品列表和购物车测试如果各自重复 `.inventory_item`、`.cart_item`、商品名称/价格和购物车入口 locator，页面结构变化时容易漏改，多个测试也可能使用不一致的操作。集中抽取可以降低维护成本，但不能把所有业务规则塞进页面对象。

### 理论基础

#### 1. 页面职责与抽取边界

| 页面对象 | 负责内容 | 不负责内容 |
| --- | --- | --- |
| `InventoryPage` | 商品卡片、商品名称/价格/图片、加购、徽标、购物车入口、页面数据读取 | 商品集合是否完整、价格是否正确等业务结论 |
| `CartPage` | 购物车条目、名称/价格读取、名称—价格记录提取 | Expected 商品集合、金额合计和断言结果 |

测试可以表达为：

```text
给定独立的商品 Expected
    当通过 InventoryPage 加购并通过 CartPage 读取 actual
    那么测试比较数量、集合、字段关联和金额业务规则
```

#### 2. Page Object 提供 actual，测试决定 expected

`CartPage.item_records()` 只负责从 UI 读取当前显示的名称—价格记录：

```python
actual_records = cart_page.item_records()
assert set(actual_records) == expected_records
```

页面对象不应保存某个测试专用的 Expected，也不应在读取方法内部执行集合或金额断言。这样同一个读取动作才能复用于单商品、多商品、删除后状态等不同场景。

#### 3. 最小代码骨架

```python
class InventoryPage:
    def item(self, product_name: str) -> Locator:
        return self.items.filter(has_text=product_name)

    def add_item(self, product_name: str) -> None:
        self.item(product_name).get_by_role(
            "button", name="Add to cart"
        ).click()


class CartPage:
    def item_records(self) -> list[tuple[str, str]]:
        return [
            (self.item_name(item).inner_text(), self.item_price(item).inner_text())
            for item in self.items.all()
        ]
```

上面的对象提供定位、动作和读取；测试仍负责 `expected_items`、数量、集合和 `Decimal` 合计。

#### 4. 适用场景与边界

- 适用：多个测试共享页面结构和机械动作，页面变化需要集中维护的场景。
- 适用：商品列表、购物车、结算等职责清晰的页面对象。
- 不适用：创建一个包含所有页面和所有业务流程的万能 `BasePage`；跨页面流程仍应由测试编排。
- 不适用：把一次性操作过度抽象，抽象应减少重复或提高可读性。
- 页面对象可以返回 locator 或 actual 数据，但业务 Expected 和场景结论应留在测试层。

#### 5. 常见错误、反例与假通过

1. 抽取页面操作时顺手删除测试 Expected，导致 `NameError` 或失去独立预期。
2. 新方法已经读取数据，旧提取循环仍保留，造成重复追加和结果错误。
3. 只看到测试通过就认为重复已消失；还需要静态搜索关键 locator。
4. 在 Page Object 内硬编码商品集合或金额预期，使对象无法复用于其他场景。
5. 过度封装跨页面业务流程，导致测试无法清楚表达每个状态转换和断言。

### 记忆要点

**页面对象集中“怎么找、怎么操作、怎么读取”；测试保留 Expected、业务规则和 actual/expected 比较。**

### 代码落地

Day 29 创建 `InventoryPage` 和 `CartPage`，重构 `test_inventory.py` 与 `test_cart.py`。登录复用 Day 28 的 `LoginPage`；目标测试不再直接使用商品卡片、购物车条目或关键入口 locator，测试仍保留集合、价格、图片和 Decimal 合计断言。

### 知识验收

1. `InventoryPage` 和 `CartPage` 分别抽取了哪些重复内容？
2. 为什么 `item_records()` 可以读取 actual，却不能替测试比较 Expected？
3. `NameError` 和旧循环重复追加分别如何排查？
4. 除了测试通过，还应如何证明关键 locator 已从测试中抽走？

### 关联产出

- 目标文件：`test-projects/02-saucedemo-ui/pages/inventory_page.py`、`test-projects/02-saucedemo-ui/pages/cart_page.py`、`test-projects/02-saucedemo-ui/tests/test_inventory.py`、`test-projects/02-saucedemo-ui/tests/test_cart.py`
- 验证命令：`pytest test-projects/02-saucedemo-ui/tests/test_inventory.py test-projects/02-saucedemo-ui/tests/test_cart.py -q`
- 验证结果：`3 passed in 12.86s`；目标测试静态扫描无直接页面结构 locator。
- 验证证据：`artifacts/day-029/verification.md`
- 当天记录：`daily-log/day-029.md`

---

## Day 30：结算页面对象

### 核心知识点

组织多页面业务流程，要求让每个 Page Object 负责自己的页面边界，再由测试按业务目标编排多个页面对象。页面对象负责当前页面怎么定位、怎么操作和怎么读取；测试负责跨页面步骤、Expected 和业务结果断言。

### 它解决的问题

完整下单 E2E 会经过登录、商品、购物车、结算信息、概览和完成页。如果这些步骤都塞进一个 `open_order_summary()` 或万能 helper，页面结构、状态转换和失败位置会被隐藏，维护和诊断成本都会上升。

### 理论基础

#### 1. 页面边界与动作归属

动作发生在哪个页面，就由哪个页面对象封装：

| 页面对象 | 负责内容 | 不负责内容 |
| --- | --- | --- |
| `CartPage` | 读取购物车、点击 Checkout、打开购物车入口 | 填写结算字段、判断订单成功 |
| `CheckoutPage` | 填写姓名/姓氏/邮编、Continue、Finish、读取完成页元素 | 决定订单是否成功 |
| E2E 测试 | 编排页面转换、保留 Expected、验证 URL/文案/后置状态 | 重复实现页面 locator |

#### 2. 多页面业务流程模型

```text
LoginPage.login()
    ↓ 登录成功
InventoryPage.add_item()
    ↓ 商品进入购物车
CartPage.open_checkout()
    ↓ 进入结算信息
CheckoutPage.fill_customer_info()
CheckoutPage.continue_to_overview()
    ↓ 概览页
CheckoutPage.finish_checkout()
    ↓ 完成页
测试断言 URL、标题、成功文案和购物车清空
```

每个状态转换都可以保留局部检查点，失败时能区分登录、加购、购物车、表单和完成页问题。

#### 3. 最小代码骨架

```python
login_page.login(username, password)
inventory_page.add_item(product_name)
inventory_page.open_cart()
cart_page.open_checkout()
checkout_page.fill_customer_info(first_name, last_name, postal_code)
checkout_page.continue_to_overview()
checkout_page.finish_checkout()

expect(page).to_have_url(COMPLETE_URL)
expect(checkout_page.complete_header).to_have_text(
    "Thank you for your order!"
)
```

`finish_checkout()` 只执行点击；完成页 URL、成功文案和购物车清空分别由测试断言，因为它们证明的是当前 E2E 的业务结果，而不是页面对象的固定结论。

#### 4. 适用场景与边界

- 适用：登录、购物车、结算等多个页面组成的关键业务链路。
- 适用：需要在状态转换处保留可读检查点、并希望失败能快速归因的 E2E。
- 不适用：用一个万能 Page Object 包含所有页面、流程和业务断言。
- 不适用：为了减少行数而隐藏所有状态转换；E2E 仍应能读出用户目标和关键后置条件。
- 跨页面编排属于测试或更高层业务流程；单个 Page Object 不应跨越多个页面职责。

#### 5. 常见错误、反例与假通过

1. 新页面对象流程加入后仍保留旧万能 helper，导致重复实现和直接 locator 残留。
2. 把购物车的 Checkout 按钮放进 `CheckoutPage`，违反动作发生页面边界。
3. 在 `finish_checkout()` 内硬编码成功 URL、感谢文案或购物车清空断言，导致负向和变体场景无法复用。
4. 只运行 `1 passed` 就认为 Page Object 重构正确；还需要扫描测试中的关键 locator 和旧 helper。
5. 让测试只调用一个高层“完成订单”方法，隐藏登录、加购和状态转换，失败时无法定位阶段。

### 记忆要点

**页面对象负责当前页面的动作，测试负责跨页面流程和业务结论；E2E 既要跑通，也要读得出状态转换。**

### 代码落地

Day 30 创建 `CheckoutPage`，扩展 `CartPage.open_checkout()`，并删除 `open_order_summary()`。`test_checkout_e2e.py` 现在直接按 Login → Inventory → Cart → Checkout → Complete 的业务顺序调用页面对象，在关键转换处断言 URL、标题、成功文案和购物车清空。

### 知识验收

1. 为什么 `CartPage` 负责 `open_checkout()`，而 `CheckoutPage` 负责填写字段和 Finish？
2. 为什么完成页 URL、成功文案和购物车清空断言应留在测试中？
3. 删除万能 helper 解决了什么维护问题？
4. 如何分别用运行证据和结构证据证明 E2E 重构正确？

### 关联产出

- 目标文件：`test-projects/02-saucedemo-ui/pages/checkout_page.py`、`test-projects/02-saucedemo-ui/pages/cart_page.py`、`test-projects/02-saucedemo-ui/tests/test_checkout_e2e.py`
- 验证命令：`pytest test-projects/02-saucedemo-ui/tests/test_checkout_e2e.py -q`
- 验证结果：`1 passed in 2.68s`；静态扫描无旧 helper 和结算直接 locator。
- 验证证据：`artifacts/day-030/verification.md`
- 当天记录：`daily-log/day-030.md`

---

## Day 31：测试数据模型

### 核心知识点

测试数据模块负责集中管理可复用的业务事实，例如账号、结算地址、商品名称和价格；测试文件负责选择测试场景、组织参数组合、调用页面动作并验证业务结果。数据抽取的目标不是让所有变量都离开测试，而是让变化数据只有一个事实来源。

### 它解决的问题

当同一个商品、账号或地址在多个测试中重复出现时，数据变更需要逐个文件搜索，容易遗漏并造成测试之间的不一致。集中数据后，测试主体可以更清楚地表达“选择什么场景”和“验证什么行为”，维护成本也更低。

### 理论基础

#### 1. 数据事实与测试场景的边界

| 内容 | 适合放置 | 原因 |
| --- | --- | --- |
| 用户名、默认密码、顾客地址 | `test_data.py` 或环境配置 | 是可复用的测试事实；密码仍应允许环境变量覆盖 |
| 商品名称、价格、完整商品目录 | `test_data.py` | 多个列表、详情、购物车和结算测试共享 |
| `selected_products` | 测试文件 | 表达本测试要覆盖的商品组合 |
| `CHECKOUT_REQUIRED_FIELD_CASES` | 测试文件 | 表达参数化场景与预期错误 |
| URL、错误文案、金额不变量 | 测试文件 | 属于当前测试的验证规则和业务结论 |

#### 2. 共享事实与本地语义别名

```python
from test_data import BACKPACK

expected_name = BACKPACK["name"]
expected_price = BACKPACK["price"]
```

`BACKPACK` 是事实数据；`expected_name` 和 `expected_price` 是测试中的语义角色。局部别名不构成第二份数据源，因为它们没有再次硬编码具体值。

#### 3. 页面字段映射

业务数据字段可以使用稳定、易读的 Python 命名；页面定位字段可以保留页面契约要求的名称：

```python
CHECKOUT_CUSTOMER = {
    "first_name": "Ada",
    "last_name": "Lovelace",
    "postal_code": "10001",
}

valid_values = {
    "firstName": CHECKOUT_CUSTOMER["first_name"],
    "lastName": CHECKOUT_CUSTOMER["last_name"],
    "postalCode": CHECKOUT_CUSTOMER["postal_code"],
}
```

这样不会把 `data-test` 等 UI 细节反向污染通用业务数据模型。

#### 4. 商品目录与测试选择

```python
PRODUCT_CATALOG = (
    BACKPACK,
    BIKE_LIGHT,
    BOLT_T_SHIRT,
    FLEECE_JACKET,
    ONESIE,
    RED_T_SHIRT,
)

selected_products = (BACKPACK, BIKE_LIGHT, ONESIE)
```

完整目录是共享事实；三商品组合是某个购物车场景的选择。购物车测试可以把字典转换为名称—价格元组，和页面提取结果进行集合比较，同时保留商品与价格的绑定关系。

### 适用场景与边界

- 适用：同一账号、地址、商品或业务常量被多个测试共享。
- 适用：需要一次修改即可同步多个测试的稳定测试数据。
- 不适用：把页面 locator、URL、错误文案和业务断言全部塞进数据模块。
- 不适用：把每个测试的场景组合都做成全局数据，导致测试意图变得不清楚。
- 安全边界：公开训练账号可以有默认值；真实凭据应由环境变量或安全配置注入。

### 常见错误、反例与假通过

1. 只抽取一个文件中的常量，却不扫描其他测试，导致重复数据仍然存在。
2. 把 `selected_products` 也放进全局模块，读者看不出当前测试为什么选择这三个商品。
3. 直接使用同一页面提取出的价格作为 Expected，形成“自己证明自己”的假通过。
4. 用 `CHECKOUT_CUSTOMER` 直接替代页面字段映射，混淆业务字段名和 UI 字段名。
5. 只看到单个测试通过就认为重构安全；必须结合静态扫描、目标测试和完整回归证据。
6. 从错误工作目录运行项目测试，导致模块导入失败；运行命令应明确项目模块边界。

### 记忆要点

**数据模块提供可复用事实，测试文件表达场景和结论；抽取数据不等于抽取测试意图。**

### 代码落地

Day 31 创建 `test_data.py`，集中账号、顾客地址、六个商品和 `PRODUCT_CATALOG`，并迁移 SauceDemo 的登录、特殊用户、库存、详情、购物车和结算测试。测试保留场景组合、字段映射、URL/错误规则和业务断言。

### 知识验收

1. 为什么商品、用户和地址适合放进 `test_data.py`？
2. 为什么 `CHECKOUT_REQUIRED_FIELD_CASES` 仍然留在测试文件？
3. 为什么多商品测试中的 `selected_products` 仍由测试自己选择？
4. 如何用静态扫描和完整回归分别证明数据已集中且行为未改变？

### 关联产出

- 目标文件：`test-projects/02-saucedemo-ui/test_data.py` 及其使用方测试
- 验证命令：`python -m pytest tests -q`（在 `test-projects/02-saucedemo-ui` 目录执行）
- 验证结果：`21 passed in 51.03s`
- 验证证据：`artifacts/day-031/verification.md`、`artifacts/day-031/pytest-full.txt`
- 当天记录：`daily-log/day-031.md`

## Day 32：环境配置

### 核心知识点

环境配置的目标是让测试逻辑与被测系统地址解耦。一个可维护的 `base_url` 解析器应定义清晰的来源优先级、校验输入，并把最终结果通过 fixture 注入测试；页面对象或 `page.goto()` 不应自行决定环境。

### 它解决的问题

如果 URL 直接写在 fixture 或每个测试里，切换本地、测试和演示环境需要修改代码，错误地址也可能直到浏览器导航时才暴露。集中解析后，命令行可以临时覆盖环境变量，非法配置会在测试准备阶段明确失败。

### 理论基础

#### 1. 配置来源优先级

```text
--base-url > SAUCEDEMO_URL > DEFAULT_BASE_URL
```

命令行适合单次运行覆盖，环境变量适合机器或 CI 配置，代码默认值只作为开发兜底。优先级必须写进代码和验证证据，而不是依赖使用者猜测。

#### 2. 配置解析与页面准备分层

```python
def resolve_base_url(cli_value: str | None = None) -> str:
    candidate = cli_value or os.getenv("SAUCEDEMO_URL") or DEFAULT_BASE_URL
    parsed = urlparse(candidate)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("base_url 必须是完整的 http(s) URL")
    return candidate.rstrip("/") + "/"
```

```python
@pytest.fixture
def saucedemo_base_url(pytestconfig):
    return resolve_base_url(pytestconfig.getoption("--base-url"))

@pytest.fixture
def saucedemo_page(page, saucedemo_base_url):
    page.goto(saucedemo_base_url)
    yield page
```

`resolve_base_url()` 决定“去哪儿”，fixture 决定“怎么准备页面”，`page.goto()` 只执行“去”。

#### 3. 错误配置应尽早失败

合法 URL 的 smoke 通过证明配置可以驱动真实页面；非法 URL 的 `ValueError` 证明错误不会静默进入浏览器。两类证据都需要保留，不能只记录绿色测试。

### 适用场景与边界

- 适用：本地、测试、预发布等环境需要复用同一套自动化脚本。
- 适用：CI 需要通过环境变量或命令行注入目标地址。
- 不适用：把真实密码等敏感信息写入普通配置文件；凭据应继续由安全环境变量注入。
- 不适用：让页面对象内部自行读取环境变量，导致配置来源分散、测试难以覆盖。
- 安全边界：性能和破坏性测试仍必须指向明确授权的本地或测试目标。

### 常见错误、反例与假通过

1. 只支持环境变量，不支持单次命令行覆盖，临时验证需要修改 shell 状态。
2. 不校验 URL，把 `not-a-url` 交给浏览器，错误信息变成难以定位的导航异常。
3. 在多个 fixture 或测试中重复读取 `SAUCEDEMO_URL`，优先级不一致。
4. 把 `page.goto()`、URL 解析、环境选择和浏览器准备全部塞进一个万能 fixture。
5. 只验证默认 URL，不验证非法值；配置错误路径没有证据。
6. 把浏览器启动权限错误误判为 URL 配置错误；应根据失败发生的 fixture 阶段分层诊断。

### 记忆要点

**配置先解析和校验，fixture 再准备页面，导航动作最后执行；命令行覆盖环境变量，环境变量覆盖默认值。**

### 代码落地

Day 32 创建 `config.py`，实现 `resolve_base_url()`；在 pytest 中注册 `--base-url`，通过 `saucedemo_base_url` 注入 `saucedemo_page`。合法 URL 的 smoke 通过，非法 URL 在 setup 阶段返回明确 `ValueError`。

### 知识验收

1. `--base-url`、`SAUCEDEMO_URL` 和默认 URL 的优先级是什么？
2. 为什么 `resolve_base_url()` 负责“去哪儿”，fixture 负责“怎么准备页面”，而 `page.goto()` 只负责“去”？
3. 为什么非法 URL 应在 fixture 阶段失败，而不是依赖浏览器返回模糊的导航错误？
4. 如何区分配置错误与 Playwright 浏览器进程权限错误？

### 关联产出

- 目标文件：`test-projects/02-saucedemo-ui/config.py`、`test-projects/02-saucedemo-ui/tests/conftest.py`
- 验证命令：`python -m pytest tests -m smoke -q --base-url=...`（在 `test-projects/02-saucedemo-ui` 目录执行）
- 验证结果：合法 URL `1 passed, 20 deselected`；非法 URL `ValueError`、退出码 `1`
- 验证证据：`artifacts/day-032/smoke-valid.txt`、`artifacts/day-032/smoke-invalid.txt`、`artifacts/day-032/verification.md`
- 当天记录：`daily-log/day-032.md`

## Day 33：多浏览器

### 核心知识点

兼容性矩阵描述“哪些浏览器运行哪些测试”，执行成本则描述每个组合需要多少时间、资源和维护成本。矩阵的目标不是盲目增加浏览器数量，而是根据用户风险、浏览器使用占比、变更范围和测试价值选择覆盖。

### 它解决的问题

只在 Chromium 运行测试可能漏掉 Firefox 的兼容性问题；在所有浏览器上重复完整回归又会放大运行时间和维护成本。把关键路径 smoke 放到多个高价值浏览器上，可以用较低成本获得早期信号，再把完整回归集中在主浏览器或高风险变更范围。

### 理论基础

#### 1. 兼容性矩阵

```text
                 smoke       full regression
Chromium           通过            按风险
Firefox            通过            按风险
WebKit             未纳入          未纳入
```

矩阵的每一格都应有明确的选择理由。今天只建立 Chromium × smoke 和 Firefox × smoke 两格，不把 WebKit 或移动视口扩展到当前目标之外。

#### 2. 浏览器选择与 fixture

```python
parser.addoption(
    "--browser",
    action="store",
    choices=("chromium", "firefox"),
    default="chromium",
)

browser_types = {
    "chromium": playwright.chromium,
    "firefox": playwright.firefox,
}
browser = browser_types[browser_name].launch(headless=True)
```

浏览器选择由命令行控制，测试主体不需要知道当前使用哪一个浏览器；同一套 smoke 逻辑才能进行有意义的横向比较。

#### 3. 成本记录

```text
Chromium smoke: 1 passed, 2.73s
Firefox smoke:  1 passed, 5.01s
```

通过状态说明功能信号一致，耗时差异说明执行成本不同。后续可以据此决定哪些浏览器进入每次提交、夜间回归或发布前验证。

### 适用场景与边界

- 适用：面向不同浏览器用户、使用跨浏览器渲染或交互能力的 Web 产品。
- 适用：关键路径需要多个浏览器的快速回归信号。
- 不适用：没有用户风险或产品需求依据时机械增加浏览器数量。
- 不适用：只比较通过/失败而不记录浏览器版本、执行时间和环境依赖。
- 边界：浏览器二进制包是 Playwright 库之外的独立依赖，需要单独安装和记录。

### 常见错误、反例与假通过

1. 只把浏览器名写进报告，却没有真正用不同浏览器启动测试。
2. 在不同浏览器运行不同测试集合，导致结果无法比较。
3. 只看绿色结果，不记录 Firefox 等浏览器的额外执行成本。
4. 浏览器未安装时把启动错误误判为兼容性缺陷。
5. 为了追求矩阵数量加入 WebKit、移动视口和完整回归，超出当天风险与时间范围。
6. 把浏览器选择逻辑散落在每个测试中，导致测试主体与环境耦合。

### 记忆要点

**矩阵按风险选格子，smoke 先跨浏览器守关键路径，完整回归按成本和变更范围扩展。**

### 代码落地

Day 33 在 pytest 中增加 `--browser` 选项，session browser fixture 支持 Chromium 与 Firefox；同一个 smoke 集合在两个浏览器中均通过，并记录了执行时间差异。

### 知识验收

1. 为什么兼容性矩阵不是浏览器越多、测试越多越好？
2. 为什么今天选择在 Chromium 和 Firefox 运行 smoke，而不是立即运行两个浏览器的完整回归？
3. Firefox 用时更高时，如何使用矩阵决定后续覆盖范围？
4. 如何区分浏览器未安装、浏览器进程权限错误和真实兼容性失败？

### 关联产出

- 目标文件：`test-projects/02-saucedemo-ui/tests/conftest.py`、`test-projects/02-saucedemo-ui/pytest.ini`
- 验证命令：`python -m pytest tests -m smoke -q --browser=chromium|firefox --base-url=...`
- 验证结果：Chromium `1 passed, 20 deselected in 2.73s`；Firefox `1 passed, 20 deselected in 5.01s`
- 验证证据：`artifacts/day-033/smoke-chromium.txt`、`artifacts/day-033/smoke-firefox.txt`、`artifacts/day-033/verification.md`
- 当天记录：`daily-log/day-033.md`

## Day 34：报告与 flaky 分析

### 核心知识点

测试失败首先是一个现象，不是根因。区分产品缺陷、脚本缺陷和环境问题，需要把自动采集的客观证据与人工归因分开：hook 记录“发生了什么”，人根据需求、代码和环境证据判断“为什么发生”，报告保存本次确认后的结论。

flaky 也不是任意偶发失败的同义词。只有在代码、数据和环境条件保持一致时重复执行，结果仍在通过与失败之间波动，才有证据将它作为 flaky 问题继续分析。

### 它解决的问题

如果看到 `AssertionError`、元素找不到或超时就直接创建产品缺陷，测试团队会把错误预期、失效 locator、浏览器权限和网络问题错误地归给产品；如果所有失败都先重跑，也会掩盖真实缺陷并让不稳定脚本长期存在。

报告与分类机制把步骤、堆栈、URL、截图、实际值和环境错误组织在一起，使结论可以被复核。它还保留“未分类”状态：证据不足时不猜测责任归属。

### 理论基础

#### 1. 现象、证据与结论是三层信息

| 层次 | 示例 | 能否直接定责 |
| --- | --- | --- |
| 失败现象 | 标题断言失败、找不到登录按钮、导航超时 | 不能 |
| 客观证据 | URL、DOM、实际文本、截图、调用日志、网络或权限错误 | 仍需结合正确预期分析 |
| 分类结论 | 产品缺陷、脚本缺陷、环境问题 | 必须说明证据链和排除理由 |

`AssertionError` 只说明自动化预期与实际结果不一致。正确预期来自需求、产品规则或可靠对照；断言类型本身无法判断是产品实现错误还是测试 expected 值错误。

#### 2. 三类问题的证据标准

| 分类 | 判断条件 | 典型证据 |
| --- | --- | --- |
| 产品缺陷 | 测试步骤、预期和环境正常，但产品实际行为仍错误 | 正确页面已加载、locator 有效、人工可复现、截图或接口响应显示错误产品状态 |
| 脚本缺陷 | 产品行为正常，但测试实现、数据、等待或预期错误 | DOM 中目标存在、actual 符合产品规则、locator 失效、expected 写错、修正脚本后稳定通过 |
| 环境问题 | 产品逻辑与测试实现没有相应异常，运行条件阻断执行 | 浏览器启动失败、`WinError 5`、DNS/网络超时、服务不可达、环境变量或版本差异 |

分类还要看问题落点。同一个错误路径若只是在终端临时输入，是操作错误；若被写入 README 或 CI 脚本，则成为文档或自动化脚本缺陷。

#### 3. 证据采集与人工归因的执行链

```text
测试执行
  → STEP 日志记录业务进度
  → pytest/Playwright 保存堆栈、expected、actual 和调用日志
  → 失败 hook 在页面仍可用时截取 PNG
  → 初次报告保持未分类
  → 人工结合需求、脚本和环境分析
  → 通过显式元数据写入分类与理由
  → 恢复或修复后运行完整回归
```

自动化可以可靠判断“测试在哪个阶段失败”“页面当时是什么样”，但不能凭异常类自动理解产品需求。将分类作为显式元数据，既避免机器猜测，也让报告中的结论可追溯。

#### 4. 最小报告 hook 骨架

```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    extras = list(getattr(report, "extras", []))
    page = item.funcargs.get("saucedemo_page")
    if page is not None:
        extras.append(capture_page_as_png_extra(page))

    category = item.config.getoption("--failure-category")
    reason = item.config.getoption("--failure-reason")
    if category is not None:
        extras.append(classification_text_extra(category, reason))

    report.extras = extras
```

截图失败必须被隔离，不能覆盖原始测试失败。分类参数未提供时不应生成猜测性结论。页面在 fixture setup 前尚未创建时，也不能强求截图，应转而依赖权限、进程、网络和配置证据。

#### 5. 确定性失败与 flaky 的区别

本日把 `Products` 的正确预期临时改为 `Products-INTENTIONAL-FAILURE`。相同代码每次都会在同一断言失败，这是可重复的脚本缺陷，不是 flaky。

判断 flaky 至少需要控制代码版本、测试数据、浏览器和目标环境，并保存多次运行的结果与时间。如果结果波动，再比较失败步骤、截图、网络、资源负载和环境差异，寻找与失败相关的变量。单纯“重跑后通过”只能增加怀疑，不能完成根因分析。

#### 6. 适用场景与边界

- 适用：UI 回归、CI 失败诊断、需要跨环境复核的自动化报告；
- 适用：产品、测试和环境责任容易混淆的失败；
- 不适用：证据不足时强行选择分类；
- 不适用：把重试当作默认修复；
- 边界：self-contained HTML 适合单次报告和附件携带，但不自动提供历史趋势；
- 边界：当前 hook 只覆盖已有 `saucedemo_page` 的 call 阶段失败。

#### 7. 常见错误、反例与假通过

1. 看到 `AssertionError` 就归为产品缺陷，忽略 expected 可能写错。
2. 根据一次本地通过、一次 CI 失败就宣布 flaky，没有控制变量或重复数据。
3. hook 自动根据异常类型定责，把证据采集器变成不可靠的缺陷分类器。
4. 截图代码抛异常并覆盖原始失败，导致关键证据丢失。
5. 使用相对报告路径却忽略当前工作目录，使证据写入错误位置。
6. 报告只写“FAILED”，没有步骤、actual、截图、URL 和分类理由。

#### 8. 记忆要点

**先分离现象、证据和结论：hook 记录发生了什么，人判断为什么发生；一次失败不等于 flaky，一次重跑通过也不等于根因消失。**

### 代码落地

Day 34 接入 `pytest-html`，在登录测试中使用 `STEP:` INFO 日志记录登录、URL 验证和标题验证；`pytest_runtest_makereport` 在 call 阶段失败时把 Playwright 截图编码为 self-contained PNG 附件，并通过 `--failure-category`、`--failure-reason` 接收人工分类。

受控失败报告保存了 `Products-INTENTIONAL-FAILURE` 与实际 `Products`、三条步骤、失败堆栈、页面截图和“脚本缺陷”结论。断言恢复为 `Products` 后，完整回归 21 条通过。`pytest.ini` 同时加入项目 `pythonpath`，避免从仓库根目录运行时同名 `config/` 遮蔽 SauceDemo 的 `config.py`。

### 知识验收

1. 为什么 `AssertionError` 不能自动分类为产品缺陷或脚本缺陷？
2. 产品缺陷、脚本缺陷和环境问题分别需要哪些支持证据？
3. 为什么 hook 应采集客观证据，而分类应通过显式元数据写入？
4. 本次 `Products` 受控失败为什么是确定性脚本缺陷，而不是 flaky？
5. setup 阶段浏览器启动失败为什么可能没有截图，应查看哪些替代证据？

### 关联产出

- 目标文件：`test-projects/02-saucedemo-ui/README.md`
- 代码文件：`test-projects/02-saucedemo-ui/tests/conftest.py`、`test-projects/02-saucedemo-ui/tests/test_login.py`
- 依赖与配置：`test-projects/02-saucedemo-ui/requirements.txt`、`test-projects/02-saucedemo-ui/pytest.ini`
- 验证命令：`python -m pytest test-projects/02-saucedemo-ui/tests -q`
- 验证结果：恢复受控断言后 `21 passed in 73.87s`
- 验证证据：`artifacts/day-034/verification.md`；本地 HTML 为 `artifacts/day-034/day34-classified-failure.html`
- 当天记录：`daily-log/day-034.md`

## Day 35：阶段验收

### 核心知识点

框架可维护性是指需求或页面发生变化时，自动化代码能够以较小改动范围继续演进，同时保持测试意图清楚、失败容易定位、既有回归不被破坏。独立开发能力则表现为能够根据职责边界判断“复用什么、扩展什么、断言放哪里”，并用目标测试和完整回归证明改动安全。

### 它解决的问题

测试全部通过只能证明当前行为满足断言，不能单独证明框架容易维护。如果新增一条跨页面场景就要复制大量 locator、修改多个无关文件，或者把业务断言藏进 Page Object，框架仍然会随着场景增加而快速失控。

明确维护性标准后，可以在新增场景时控制改动范围，避免重复页面结构和万能 helper，同时让测试继续直接表达业务风险。

### 理论基础

#### 1. 可维护性的五个观察维度

| 维度 | 应观察的信号 |
| --- | --- |
| 改动局部性 | 页面结构变化主要影响对应 Page Object，而不是所有测试 |
| 复用边界 | 相同页面操作通过稳定接口复用，不复制 locator |
| 意图可见性 | 测试主体能够直接读出业务流程、预期和关键断言 |
| 失败可诊断性 | 失败位置能区分页面操作、数据、业务断言和环境问题 |
| 回归安全性 | 新场景目标测试通过，完整回归也保持通过 |

这些维度需要同时满足。只减少代码行数可能隐藏意图；只保留直白测试又可能复制页面结构；只运行新测试则无法证明没有回归影响。

#### 2. 各层职责模型

| 层次 | 负责 | 不负责 |
| --- | --- | --- |
| Page Object | 页面 locator、页面内操作、页面数据读取 | 业务 expected、跨页面流程结论、业务通过条件 |
| 测试 | 场景编排、预期构造、比较规则、业务断言 | 重复描述 DOM 结构 |
| `test_data.py` | 用户、地址、商品等共享事实 | 决定当前场景验证哪些业务规则 |
| fixture/config | 环境、浏览器、页面生命周期和运行配置 | 隐藏测试主体的业务步骤 |

判断一个逻辑放在哪里，可以先问：它是“页面如何操作或读取”，还是“业务结果是否正确”？前者通常属于 Page Object，后者属于测试。

#### 3. 新增场景时的决策顺序

```text
明确业务风险和关键断言
  → 检查现有 Page Object 是否已有所需能力
  → 缺少页面能力时，只增加最小页面接口
  → 从共享数据构造 expected
  → 在测试中编排跨页面流程并比较 actual 与 expected
  → 运行目标测试
  → 运行完整回归并保存证据
```

这个顺序先确定验证目标，再决定抽象，不会为了“看起来像框架”而提前制造无实际复用价值的层次。

#### 4. 最小代码骨架

```python
class CheckoutPage:
    def overview_item_records(self) -> list[tuple[str, str]]:
        return [
            (
                item.locator(".inventory_item_name").inner_text(),
                item.locator(".inventory_item_price").inner_text(),
            )
            for item in self.overview_items.all()
        ]


def test_checkout_preserves_product_records(...):
    expected = {
        (BACKPACK["name"], BACKPACK["price"]),
        (BIKE_LIGHT["name"], BIKE_LIGHT["price"]),
    }

    # 测试负责跨页面编排。
    actual = checkout_page.overview_item_records()

    # 比较规则和业务断言保留在测试层。
    assert set(actual) == expected
```

页面对象返回实际观察值，不知道哪些商品“应该”存在。测试使用独立的商品数据构造预期集合，并选择集合比较，因为本场景关心成员与价格完整性，不关心展示顺序。

#### 5. 适用场景与边界

- 适用：页面结构相对稳定、多个测试需要复用页面操作的 UI 自动化项目；
- 适用：新增跨页面场景时评估现有框架是否需要最小扩展；
- 不适用：把每一次点击都包装成没有业务意义的方法；
- 不适用：为了消除少量重复而建立跨多个页面的万能对象；
- 边界：Page Object 能降低页面变化成本，但不能替代正确的业务预期；
- 边界：一次完整回归通过能证明当前改动没有触发已覆盖的回归，但不能证明所有未知风险都不存在。

#### 6. 常见错误、反例与假通过

1. 在新测试中重新写 `.cart_item` 等 locator，绕过已有页面对象。
2. 把 `expected_records` 和集合比较放进 Page Object，使页面对象同时承担业务规则。
3. 创建一个跨登录、商品、购物车和结算的万能 helper，隐藏关键状态转换。
4. 只验证最终成功文案，不验证商品数据在跨页面过程中是否保持一致。
5. 只运行新增测试，不执行完整回归，却声称改动安全。
6. 把运行耗时和当天复盘堆进项目 README，混淆稳定文档、学习记录和验证证据。

#### 7. 记忆要点

**页面对象回答“页面怎么操作和读取”，测试回答“业务结果是否正确”；可维护性要同时看改动范围、意图可见性、失败定位和完整回归。**

### 代码落地

Day 35 在 `CheckoutPage` 增加结算概览商品记录读取能力，并新增双商品跨页面回归场景。测试从 `test_data.py` 构造名称—价格预期集合，在购物车和结算概览分别比较记录，最后验证订单完成和购物车清空。

项目 README 只保留稳定的分层职责与运行方式；目标测试、完整回归和整理后复验结果保存到 Day 35 验证证据。目标场景通过，完整回归从 21 条增加到 22 条且全部通过。

### 知识验收

1. 为什么页面 locator 和读取逻辑适合放在 Page Object，而 expected 和比较规则应留在测试？
2. 新增场景通过为什么不能单独证明框架改动安全？
3. 哪些信号说明一个 Page Object 已经演变成万能 helper？
4. 为什么本场景使用集合比较，什么情况下应改用顺序比较？
5. 项目 README、daily-log、LEARNING-NOTES 和 artifacts 各自保存什么内容？

### 关联产出

- 页面对象：`test-projects/02-saucedemo-ui/pages/checkout_page.py`
- 跨页面测试：`test-projects/02-saucedemo-ui/tests/test_portfolio_scenario.py`
- 架构说明：`test-projects/02-saucedemo-ui/README.md`
- 验证命令：`python -m pytest tests/test_portfolio_scenario.py -q`；`python -m pytest tests -q`
- 验证结果：目标场景整理后复验 `1 passed in 5.36s`；完整回归 `22 passed in 74.70s`
- 验证证据：`artifacts/day-035/verification.md`
- 当天记录：`daily-log/day-035.md`

## Day 36：HTTP 与健康检查

### 核心知识点

健康检查不是“请求没有抛异常”或“状态码属于 2xx”这么简单。测试应依据接口契约同时验证状态码、响应体和响应耗时；请求客户端还要设置独立的超时保护，避免服务无响应时测试无限等待。

### 它解决的问题

只断言状态码可能把错误的业务响应当成健康；只断言响应体可能忽略 HTTP 层契约；没有耗时约束则无法发现服务在可用但过慢的状态。把这些证据分开，还能在失败时区分功能、脚本、依赖和运行环境问题。

### 理论基础

#### 定义与关键概念

| 检查 | 证明什么 | 不能单独证明什么 |
| --- | --- | --- |
| 状态码 | HTTP 结果是否符合接口契约，例如本接口要求 `201` | 不能证明响应体语义正确或响应足够快 |
| 响应体 | 服务返回的内容是否符合健康检查语义，例如 `Created` | 不能证明所有 HTTP 头或性能约束正确 |
| 请求超时 | 客户端是否在规定等待窗口后停止阻塞 | 不是服务性能 SLA；超时只说明本次请求未及时完成 |
| 响应耗时 | 从发起请求到收到响应的端到端时间是否低于项目阈值 | 公网测量还包含 DNS、TLS、线路和服务负载，不能单独证明产品性能缺陷 |

本日的接口契约是 `GET /ping` 返回 `201 Created`。`1.0s` 是测试项目定义的性能阈值，不应写成 Restful Booker 官方 SLA；`3.0s` 是客户端请求超时保护。

#### 心智模型或执行链

```text
解析目标 URL
  → 以 timeout 发起 GET /ping
  → 记录响应状态、响应体和端到端耗时
  → 分别与契约和项目阈值比较
  → 失败时保留客观证据，再判断产品 / 脚本 / 环境归属
```

失败分析也要遵循“现象 → 证据 → 分类 → 修复 → 复验”：`AssertionError` 只是现象，不能自动等同于产品缺陷。

#### 最小代码骨架

```python
import os
import time

import requests


base_url = os.getenv("RESTFUL_BOOKER_URL", "http://127.0.0.1:3001").rstrip("/")
response_started = time.perf_counter()
response = requests.get(f"{base_url}/ping", timeout=3.0)
elapsed = time.perf_counter() - response_started

assert response.status_code == 201
assert response.text.strip() == "Created"
assert elapsed <= 1.0  # 项目性能阈值，不等于官方 SLA
```

#### 断言、数据或状态的含义

`requests.get(..., timeout=3.0)` 防止请求无限等待；`perf_counter()` 测量本次端到端调用耗时。两者职责不同，不能用 `timeout` 代替性能断言，也不能把一次性能超限直接解释成产品缺陷。

#### 适用场景与边界

- 适用：本地或受控测试环境中的轻量健康检查、接口冒烟和可用性门槛。
- 适用：需要同时验证 HTTP 契约和最小响应时间的服务入口。
- 边界：公共网络上的单次耗时不能代表服务端 SLA；应重复执行并记录环境条件。
- 边界：健康检查只能证明一个很小的接口切片，不能替代 CRUD、鉴权、Schema 和业务流程测试。

#### 常见错误、反例与假通过

1. 把所有 2xx 都当成健康成功，忽略接口规定的具体状态码和响应体。
2. 只设置请求超时，不断言项目性能阈值；这样服务可能很慢却仍然通过。
3. 把本地目标配置解析出来后，又用第二次硬编码赋值覆盖 URL；本日的失败就是该脚本缺陷。
4. 在公网服务上使用严格的本地性能阈值，并把网络波动误报为产品缺陷。
5. 缺少 `requests` 时直接运行测试；依赖声明应与测试代码一起维护。

#### 记忆要点

**状态码看 HTTP 契约，响应体看业务语义，timeout 防止无限等待，耗时断言检查项目性能门槛；分类结论必须建立在证据上。**

### 代码落地

本日初始化 `test_health.py`，声明 `pytest` 和 `requests` 依赖，使用 `RESTFUL_BOOKER_URL` 加本地默认地址访问 `GET /ping`，并断言 `201`、`Created` 和 `1.0s` 阈值。验证过程中，公共地址连续 5 次耗时为 1.817s、1.616s、1.638s、1.402s、1.567s，切换到本地服务后健康接口返回 `201 Created`，完整测试 `1 passed in 0.08s`。

失败链条也被保留：错误路径导致收集不到测试；缺少 `requests` 导致收集阶段导入失败；公共地址耗时超限属于测量环境不匹配；重复 URL 赋值则是脚本缺陷。删除覆盖赋值并使用本地目标后复验通过。

### 知识验收

1. 为什么 `201` 不能因为属于 2xx 就自动视为健康通过？
2. `requests` 的 timeout 和 `elapsed <= 1.0` 分别证明什么？
3. 为什么公共地址连续 5 次超过 1 秒，仍不能直接判定产品性能缺陷？
4. 为什么重复的 `HEALTH_URL` 赋值属于脚本缺陷？
5. 如何用“现象 → 证据 → 分类 → 修复 → 复验”分析一次 API 测试失败？

### 关联产出

- 测试文件：`test-projects/03-restful-booker-api/tests/test_health.py`
- 依赖文件：`test-projects/03-restful-booker-api/requirements.txt`
- 目标配置：`config/targets.json` 中的 `RESTFUL_BOOKER_URL` 和本地默认地址
- 验证命令：`python -m pytest test-projects/03-restful-booker-api/tests -q`
- 验证结果：本地服务 `1 passed in 0.08s`
- 验证证据：`artifacts/day-036/verification.md`
- 当天记录：`daily-log/day-036.md`

## Day 37：查询列表

### 核心知识点

集合接口测试应把 HTTP 成功和响应数据契约分层验证。`200` 只能说明请求在 HTTP 层返回了预期状态；还需要确认响应是合法 JSON、顶层是列表、每个元素是对象，并且包含接口要求的必需字段。

### 它解决的问题

如果只断言 `status_code == 200`，服务可能返回错误的 JSON 对象、空结构或缺少关键字段，测试仍会假通过。分层断言可以把失败定位到 HTTP 状态、JSON 解析、顶层集合、元素类型或字段结构，报告也能保留实际索引和数据。

### 理论基础

#### 定义与关键概念

| 检查层 | 断言示例 | 证明什么 |
| --- | --- | --- |
| HTTP 状态 | `response.status_code == 200` | 请求在 HTTP 层返回了接口预期状态 |
| JSON 解析 | `response.json()` 成功 | 响应体可以按 JSON 解释 |
| 顶层集合 | `isinstance(data, list)` | 响应符合列表接口的顶层结构 |
| 元素类型 | `isinstance(item, dict)` | 每个列表项是可读取字段的对象 |
| 必需字段 | `"bookingid" in item` | 每个元素包含接口契约要求的身份字段 |

这些层次必须同时满足。状态码正确不等于业务数据正确；结构错误首先是契约不符合的现象，最终产品、脚本还是环境归属仍要结合可靠契约和运行证据判断。

#### 心智模型或执行链

```text
以 RESTFUL_BOOKER_URL 解析目标
  → GET /booking 并设置请求 timeout
  → 验证 HTTP 状态
  → 解析 JSON
  → 验证顶层 list
  → 遍历元素验证 dict 和 bookingid
  → 用索引、实际类型和实际数据输出可定位失败信息
```

#### 最小代码骨架

```python
response = requests.get(bookings_url, timeout=3.0)
assert response.status_code == 200

data = response.json()
assert isinstance(data, list)

for index, booking in enumerate(data):
    assert isinstance(booking, dict)
    assert "bookingid" in booking, (
        f"Item {index} is missing 'bookingid': {booking}"
    )
```

#### 断言、数据或状态的含义

`status_code == 200` 只证明 HTTP 层成功；`response.json()` 失败说明响应无法按 JSON 解析；列表和元素断言证明数据形状；`bookingid` 断言证明每个条目具备后续关联所需的身份字段。失败消息中的索引和实际对象是定位集合中单个坏元素的关键证据。

#### 适用场景与边界

- 适用：返回资源集合、ID 列表或分页结果的 GET 接口。
- 适用：需要在后续接口关联前确认集合形状和最小身份字段的 API 测试。
- 边界：本日只验证列表结构，不证明每个 booking 的完整详情字段、排序、分页或业务内容正确。
- 边界：空列表是否允许要由接口契约决定；本日完成标准不强制要求列表非空。

#### 常见错误、反例与假通过

1. 只断言 `200`，把错误的 JSON 对象当成成功响应。
2. 只断言列表长度，不验证元素类型和身份字段，无法发现坏元素或缺字段。
3. 直接访问固定 `localhost`，忽略仓库的 `RESTFUL_BOOKER_URL` 环境配置。
4. 遇到 `bookingid` 缺失就直接创建产品缺陷，没有先确认接口契约和测试预期。
5. 在失败消息中不带元素索引和实际对象，导致集合失败难以定位。

#### 记忆要点

**200 只证明 HTTP 成功；集合接口还要证明 JSON、列表、元素类型和必需字段，断言信息必须能定位具体坏元素。**

### 代码落地

本日新增 `test_get_bookings.py`，通过 `RESTFUL_BOOKER_URL` 和本地默认地址构造 `/booking`，设置 `3.0s` 请求超时，依次验证 `200`、列表类型、元素对象类型和 `bookingid` 字段。目标测试通过 `1 passed in 0.13s`，与 Day 36 健康检查合并后的 API 测试通过 `2 passed in 0.11s`。

代码中的错误消息使用元素索引、实际类型和实际对象。例如，若第二个元素缺少字段，示例证据应类似 `Item 1 is missing 'bookingid': {'id': 2}`；这只是失败信息设计示例，不是本次真实失败结果。

### 知识验收

1. 为什么 `200` 不能单独证明 `/booking` 响应正确？
2. 顶层列表、元素对象和 `bookingid` 字段分别证明什么？
3. 为什么空列表是否通过要由接口契约决定，而不是测试作者凭感觉决定？
4. 如果只有一个元素缺少 `bookingid`，失败消息应包含哪些定位证据？
5. 响应结构失败为什么仍不能自动归因于产品缺陷？

### 关联产出

- 测试文件：`test-projects/03-restful-booker-api/tests/test_get_bookings.py`
- 依赖文件：`test-projects/03-restful-booker-api/requirements.txt`
- 验证命令：`python -m pytest test-projects/03-restful-booker-api/tests/test_get_bookings.py -q`；`python -m pytest test-projects/03-restful-booker-api/tests -q`
- 验证结果：目标测试 `1 passed in 0.13s`；API 全量 `2 passed in 0.11s`
- 验证证据：`artifacts/day-037/verification.md`
- 当天记录：`daily-log/day-037.md`

## Day 38：创建预订

### 核心知识点

POST 测试不能只验证成功状态码。应明确构造 JSON 请求体，验证服务返回有效资源 ID，并比较响应中的资源字段与请求数据一致；如果要证明数据已经持久化，还需要在后续用动态 ID 查询该资源。

### 它解决的问题

只断言 `200` 可能把 `{\"message\": \"success\"}` 之类没有资源结果的响应误判为创建成功。只断言 `bookingid` 又可能漏掉服务忽略或错误改写请求字段。请求体、资源 ID、返回对象和字段一致性组合起来，才能证明本次创建响应满足基本契约。

### 理论基础

#### 定义与关键概念

| 检查层 | 断言示例 | 证明什么 |
| --- | --- | --- |
| 请求 JSON | `requests.post(..., json=payload)` | Python 数据按 JSON 发送，避免手动拼接字符串 |
| HTTP 状态 | `response.status_code == 200` | 创建请求在 HTTP 层返回接口预期状态 |
| 资源标识 | `bookingid` 存在且为整数 | 服务返回了可用于后续关联的资源 ID |
| 返回对象 | `booking` 存在且为对象 | 响应包含创建资源的结构化表示 |
| 字段一致性 | 返回字段逐项等于 payload | 创建结果与本次请求数据一致 |
| 持久化回查 | `GET /booking/{bookingid}` | 进一步证明资源可被后续请求查询，超出本日最小范围 |

#### 心智模型或执行链

```text
定义可辨识的 payload
  → 用 json=payload 发送 POST /booking
  → 验证 HTTP 状态
  → 解析 JSON 响应
  → 验证 bookingid 和 booking 对象
  → 逐项比较返回字段与 payload
  → 如需证明持久化，再用动态 bookingid GET 回查
```

#### 最小代码骨架

```python
response = requests.post(booking_url, json=payload, timeout=3.0)
assert response.status_code == 200

data = response.json()
assert isinstance(data["bookingid"], int)
assert isinstance(data["booking"], dict)

for field, expected in payload.items():
    actual = data["booking"].get(field)
    assert actual == expected, (
        f"Field {field!r} mismatch: expected {expected!r}, got {actual!r}"
    )
```

#### 断言、数据或状态的含义

`json=payload` 让 `requests` 负责 JSON 序列化和请求头处理；状态码证明 HTTP 层结果；`bookingid` 证明服务返回资源身份；字段比较证明返回的创建内容没有偏离请求。上述响应仍可能只是服务端返回的表示，不能单独证明数据已经持久化到可查询状态。

#### 适用场景与边界

- 适用：创建资源、提交表单、写入订单或生成任务的 API 测试。
- 适用：需要把请求数据与响应资源建立对应关系的接口。
- 边界：本日只验证创建响应，不覆盖用 ID 查询、更新、删除和数据清理。
- 边界：每次运行都会创建 booking，长期回归需要数据隔离或清理策略。

#### 常见错误、反例与假通过

1. 使用 `data=payload` 或手动拼 JSON，导致 Content-Type 或序列化行为不符合契约。
2. 只断言 `200`，没有证明资源 ID 和返回资源内容存在。
3. 只断言 `bookingid` 存在，不比较响应字段，无法发现服务错误地使用默认值或旧数据。
4. 硬编码目标 URL，绕过 `RESTFUL_BOOKER_URL` 环境切换。
5. 把响应回显当作持久化证明；真正的持久化需要后续 GET 回查。
6. 不记录每次创建的动态 ID，也没有清理策略，导致测试环境数据不断累积。

#### 记忆要点

**POST 用 JSON 发送意图，状态码证明请求结果，ID 证明资源身份，字段比较证明创建内容；持久化要靠后续查询证据。**

### 代码落地

本日新增 `test_create_booking.py`，通过 `RESTFUL_BOOKER_URL` 和本地默认地址向 `/booking` 发送包含姓名、价格、押金状态、日期和附加需求的 JSON payload。测试验证 `200`、整数 `bookingid`、`booking` 对象，并逐项比较返回字段与 payload。目标测试通过 `1 passed in 0.12s`，与健康检查和列表查询合并后的 API 全量回归通过 `3 passed in 0.10s`。

代码审查曾发现并修正 URL 配置、`os` 导入和响应字段比较遗漏；本次没有把 GET 回查和清理提前塞入最小目标，作为后续动态 ID 关联与数据治理风险保留。

### 知识验收

1. 为什么 `200` 不能单独证明 booking 创建成功？
2. `bookingid` 和返回字段逐项比较分别证明什么？
3. 为什么 `json=payload` 比手动拼 JSON 更适合当前测试？
4. 为什么响应字段与 payload 一致仍不能完全证明数据已持久化？
5. 每次创建 booking 却没有清理，会给后续回归带来什么风险？

### 关联产出

- 测试文件：`test-projects/03-restful-booker-api/tests/test_create_booking.py`
- 依赖文件：`test-projects/03-restful-booker-api/requirements.txt`
- 验证命令：`python -m pytest test-projects/03-restful-booker-api/tests/test_create_booking.py -q`；`python -m pytest test-projects/03-restful-booker-api/tests -q`
- 验证结果：目标测试 `1 passed in 0.12s`；API 全量 `3 passed in 0.10s`
- 验证证据：`artifacts/day-038/verification.md`
- 当天记录：`daily-log/day-038.md`

## Day 39：查询单条

### 核心知识点

接口关联（API chaining）是把前一个请求的真实输出作为后一个请求的输入。创建资源后，测试应读取本次 POST 返回的动态 `bookingid`，再用这个 ID 查询详情，并将查询结果与原始 payload 比较，才能验证创建结果可以被后续接口访问且内容一致。

### 它解决的问题

写死详情 ID 可能命中不存在、过期或属于其他测试的 booking；只检查 GET 的 `200` 也可能把错误资源误判为本次创建结果。动态 ID 让请求之间建立可复现的因果关系，字段比较则避免“查询成功但数据错误”的假通过。

### 理论基础

#### 定义与关键概念

| 检查层 | 证据 | 证明什么 |
| --- | --- | --- |
| 创建状态 | POST 返回 `200` | 创建请求在 HTTP 层得到预期结果 |
| 动态身份 | 读取本次响应的 `bookingid` | 后续查询指向本次创建的资源，而不是固定历史数据 |
| 查询状态 | GET `/booking/{bookingid}` 返回 `200` | 该资源可以被后续请求访问 |
| 查询结构 | GET 响应是对象 | 响应具备读取 booking 字段的结构 |
| 数据一致性 | 查询字段与原始 payload 相等 | 创建、持久化和查询链路返回了预期内容 |

#### 心智模型或执行链

```text
准备唯一可辨识的 payload
  → POST /booking
  → 读取本次响应的 bookingid
  → GET /booking/{动态 bookingid}
  → 验证 HTTP 状态和对象结构
  → 比较查询字段与原始 payload
  → 根据证据区分脚本、环境和产品数据一致性问题
```

#### 最小代码骨架

```python
create_response = requests.post(booking_url, json=payload, timeout=3.0)
assert create_response.status_code == 200

booking_id = create_response.json()["bookingid"]

get_response = requests.get(
    f"{booking_url}/{booking_id}",
    timeout=3.0,
)
assert get_response.status_code == 200

booking = get_response.json()
assert booking["firstname"] == payload["firstname"]
assert booking["bookingdates"] == payload["bookingdates"]
```

#### 断言、数据或状态的含义

动态 ID 断言证明测试没有把查询目标写死，但它本身不能证明资源已经正确保存。GET 的 `200` 证明查询请求在 HTTP 层成功，但不能证明查到的就是本次资源。字段一致性断言把查询结果和创建意图绑定起来；若字段不一致，应先检查 ID 获取、URL 拼接、字段比较和环境数据，再判断是否存在产品持久化或查询缺陷。

#### 适用场景与边界

- 适用：POST 创建后需要 GET 回查的资源接口，以及订单、任务、用户等多接口业务链路。
- 适用：需要验证创建结果可见性、持久化和读写一致性的 API 测试。
- 边界：一次成功回查只能证明本次运行中的可见性，不能替代并发、重试、事务隔离或长期一致性测试。
- 边界：测试仍会创建 booking；长期回归需要数据隔离、清理或专用测试环境。

#### 常见错误、反例与假通过

1. 写死 `booking_id = 123`，误把历史资源当成本次创建结果。
2. POST 后直接查询固定 ID，测试之间互相污染，失败原因难以复现。
3. 只断言 GET `200`，不比较字段，无法发现查到错误资源。
4. 忘记定义 `BOOKING_URL` 等脚本变量，测试在执行阶段触发 `NameError`。
5. 字段不一致时立即提交产品缺陷，没有先排除脚本取错 ID、环境数据污染或契约理解错误。

#### 记忆要点

**用 POST 的动态输出驱动 GET，才能证明“这一次创建的资源可被查询”；`200` 证明请求成功，字段一致才证明数据链路正确。**

### 代码落地

本日新增 `test_booking_flow.py`。测试通过 `RESTFUL_BOOKER_URL` 构造 `/booking`，发送与 Day 38 相同的 JSON payload，读取 POST 返回的动态 `bookingid`，再 GET 同一 ID；随后验证 GET 返回 `200`、对象结构以及姓名、价格、押金状态、日期和附加需求与 payload 一致。

代码审查在执行前发现 `BOOKING_URL` 被使用但未定义，属于脚本缺陷风险；补充 `BOOKING_URL = f"{BASE_URL}/booking"` 后，目标测试通过。这个修复不改变产品，只修正测试执行配置。

### 知识验收

1. 为什么创建后查询必须使用本次 POST 返回的动态 `bookingid`？
2. GET 返回 `200` 和字段与 payload 一致分别证明什么？
3. 如果字段不一致，为什么不能立刻判定为产品缺陷？
4. 哪些证据可以帮助区分取错 ID、环境污染和服务端数据一致性问题？
5. 重复运行创建—查询测试时，为什么仍需要考虑测试数据清理？

### 关联产出

- 测试文件：`test-projects/03-restful-booker-api/tests/test_booking_flow.py`
- 验证命令：`python -m pytest test-projects/03-restful-booker-api/tests/test_booking_flow.py -q`
- 验证结果：目标测试 `1 passed in 0.16s`
- 验证范围：本次创建资源的动态 ID 回查与字段一致性
- 代码审查问题：缺少 `BOOKING_URL` 定义；修正后复验通过
- 证据目录：`artifacts/day-039/`
- 当天记录：`daily-log/day-039.md`

## Day 40：过滤查询

### 核心知识点

查询参数（query parameters）用于在不改变资源路径的情况下表达过滤条件。过滤测试不能只验证 `200`，还要验证查询参数确实发送、响应结构可解析，并且每个返回资源的真实详情满足过滤语义；不同字段可能有不同的比较关系，例如姓名等值匹配、日期边界匹配。

### 它解决的问题

手动拼接 URL 容易漏掉 `?`、`&` 或特殊字符编码；只看列表接口的状态码和 `bookingid` 又可能把不符合条件的资源误判为过滤成功。把查询列表和动态详情核对结合起来，才能证明过滤结果的业务含义，而不是只证明服务器返回了一个响应。

### 理论基础

#### 定义与关键概念

| 检查层 | 代码证据 | 证明什么 |
| --- | --- | --- |
| 参数构造 | `requests.get(url, params=params)` | 参数由 HTTP 客户端编码并进入实际请求 URL |
| HTTP 状态 | `response.status_code == 200` | 过滤请求在 HTTP 层成功 |
| 集合结构 | `isinstance(data, list)` | 返回体符合 ID 集合接口结构 |
| 资源身份 | 每项包含 `bookingid` | 每个过滤结果可继续查询详情 |
| 详情语义 | 动态 GET 后字段比较 | 返回资源真正满足过滤条件 |

#### 心智模型或执行链

```text
准备过滤参数和比较规则
  → 使用 params=发送 GET /booking
  → 验证状态码和列表结构
  → 读取每个返回的 bookingid
  → GET /booking/{bookingid} 查询真实详情
  → 按字段语义执行 equals 或 after 比较
  → 记录实际 URL、ID、预期值和实际值
```

#### 最小代码骨架

```python
FILTER_CASES = [
    ({"firstname": "Jim"}, ("firstname",), "Jim", "equals"),
    ({"checkin": "2015-01-01"}, ("bookingdates", "checkin"), "2015-01-01", "after"),
]

response = requests.get(booking_url, params=params, timeout=3.0)
assert response.status_code == 200

for summary in response.json():
    detail = requests.get(
        f"{booking_url}/{summary['bookingid']}",
        timeout=3.0,
    ).json()
    actual = read_nested_value(detail, detail_path)
    assert actual == expected if comparison == "equals" else actual > expected
```

#### 断言、数据或状态的含义

`params=` 证明测试把参数交给客户端编码；`200` 只证明 HTTP 成功；列表和 `bookingid` 证明结果可继续关联；详情字段断言才证明过滤语义。姓名过滤通常是 `actual == expected`。本地 Restful Booker 的 `checkin` 实现按边界之后筛选，因此用 `actual > boundary` 验证；如果产品契约要求包含边界，应另写等于边界的契约测试，不应默默混用两种语义。

#### 适用场景与边界

- 适用：姓名、日期、状态、分页和组合条件等 GET 集合过滤。
- 适用：列表响应只返回 ID，需要回查资源详情才能验证业务字段的接口。
- 边界：过滤测试依赖可用数据；任意写死一个未来日期可能得到空列表，空列表不能自动算通过。
- 边界：测试应使用 `conftest.py` 提供的环境 URL 和超时 fixture，不应把共享配置隐藏在业务断言中。

#### 常见错误、反例与假通过

1. 手动拼接 `?firstname=...`，导致编码、分隔符或参数复用错误。
2. 只断言 `200`、列表和 `bookingid`，没有回查详情字段。
3. 把所有字段都使用同一种比较：姓名应等值，日期可能是边界比较。
4. 使用不存在的日期并看到 `200 + []`，就直接提交产品过滤缺陷。
5. 为了让测试变绿删除 `assert data`，把没有任何匹配数据误判为过滤通过。
6. 使用 PowerShell 手工查询详情时未设置 `Accept: application/json`，把本地服务的 `418` 误判成接口详情缺陷。
7. 直接 `from conftest import ...`，而不是让 pytest 注入 fixture，导致配置发现和测试职责混乱。

#### 记忆要点

**过滤测试要证明“参数发对了、结构拿到了、每条真实资源都满足过滤语义”；`200` 和空列表都不是业务正确性的充分证据。**

### 代码落地

本日新增 `conftest.py`，集中提供 `booking_url` 和 `request_timeout_seconds` fixture；`test_filters.py` 使用参数化覆盖 `firstname=Jim`、`lastname=Brown` 和 `checkin=2015-01-01`。测试对姓名执行 `equals`，对日期执行 `after`，并通过动态 `bookingid` 查询详情后比较字段路径。

初次日期用例使用 `checkin=2026-08-25`，实际得到 `200 + []`；检查本地数据后确认该日期不是稳定的已有数据。手工详情查询还因 PowerShell `Accept` 头缺失得到 `418`，补充 `Accept: application/json` 后确认详情接口可用。修正边界和比较规则后目标测试 3 条通过，API 全量回归 7 条通过。

### 知识验收

1. 为什么 `params=` 比手动拼接查询字符串更适合参数化过滤？
2. 哪个断言真正证明返回 booking 满足过滤条件？
3. 为什么 `200 + []` 不能直接判定过滤接口有缺陷？
4. 姓名过滤和日期过滤为什么需要不同的比较规则？
5. 如何记录实际 URL、booking ID、详情字段和环境证据来支持失败归因？

### 关联产出

- 测试配置：`test-projects/03-restful-booker-api/tests/conftest.py`
- 测试文件：`test-projects/03-restful-booker-api/tests/test_filters.py`
- 验证命令：`python -m pytest test-projects/03-restful-booker-api/tests/test_filters.py -q`；`python -m pytest test-projects/03-restful-booker-api/tests -q`
- 验证结果：目标测试 `3 passed in 0.28s`；API 全量 `7 passed in 0.28s`
- 证据目录：`artifacts/day-040/`
- 当天记录：`daily-log/day-040.md`

## Day 41：Token 鉴权

### 核心知识点

认证测试要区分 HTTP 层结果和业务层认证结果。HTTP 状态码说明请求是否被接口处理，响应体中的 `token` 或 `reason` 才说明凭据是否认证成功。本地 Restful Booker 的 `POST /auth` 对有效和无效凭据都返回 `200`，因此不能把 `200` 直接等同于登录成功。

### 它解决的问题

只断言 `status_code == 200` 会产生认证假通过：错误密码也可能被测试判定为成功。通过同时检查响应结构、非空 Token 和明确失败原因，测试才能证明认证业务结果。

### 理论基础

| 检查层 | 代码证据 | 证明什么 |
| --- | --- | --- |
| 请求构造 | `requests.post(url, json=payload, timeout=...)` | 凭据以 JSON 发送，并受超时保护 |
| HTTP 状态 | `response.status_code == 200` | 认证请求在 HTTP 层被正常处理 |
| 响应结构 | `isinstance(data, dict)` | 响应符合认证接口对象结构 |
| 成功语义 | 非空字符串 `data["token"]` | 有效凭据确实产生了可用 Token |
| 失败语义 | `data["reason"] == "Bad credentials"` | 无效凭据被明确拒绝，且没有 Token |

认证接口的测试链可以概括为：

```text
准备环境凭据
  → POST /auth
  → 验证 HTTP 状态和 JSON 结构
  → 成功路径断言非空 token
  → 失败路径断言 reason 且不包含 token
```

### 配置与安全边界

`conftest.py` 适合提供 pytest fixture，不应被测试文件当作普通配置模块直接导入。`api_base_url`、`request_timeout_seconds` 和 `auth_credentials` 通过 fixture 注入，URL、超时和账号可由环境变量覆盖。Token 只用于断言存在性和非空，不打印到日志、测试报告或错误消息中。当前本地演示账号的默认值是测试目标的公开样例凭据；真实环境不应把真实密码写入仓库。

### 常见错误、反例与假通过

1. 只断言 `200`，没有检查 `token` 或 `reason`。
2. 假设无效凭据一定返回 `401`，忽略具体 API 契约。
3. 直接 `from conftest import ...`，导致不存在的常量在收集阶段报错。
4. 重复定义同名测试函数，后一个定义会覆盖前一个定义。
5. 在日志中打印 Token 或把完整凭据放入失败消息。

### 代码落地

本日新增 `test_auth.py`，使用 pytest 参数化覆盖有效和无效凭据。共享配置通过 `api_base_url`、`request_timeout_seconds` 和 `auth_credentials` fixture 注入，保留了原有 `booking_url` fixture 的行为。有效凭据断言非空 Token；无效凭据断言 `Bad credentials` 且响应不包含 Token。

初版问题是从 `conftest.py` 导入不存在的 `REQUEST_TIMEOUT_SECONDS` 和 `RESTFUL_BOOKER_URL`，并曾重复追加测试函数。改为 fixture 注入并删除重复代码后，目标测试 2 条通过，API 全量回归 9 条通过。

### 知识验收

1. 为什么无效凭据不能只根据 HTTP 状态码判断？
2. 哪个字段证明有效凭据真正生成了 Token？
3. 为什么测试代码应使用 fixture 注入，而不是直接导入 `conftest.py`？
4. 为什么 Token 不能直接打印到日志？

### 关联产出

- 测试配置：`test-projects/03-restful-booker-api/tests/conftest.py`
- 测试文件：`test-projects/03-restful-booker-api/tests/test_auth.py`
- 验证命令：`.\\.venv\\Scripts\\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_auth.py -q`；`.\\.venv\\Scripts\\python.exe -m pytest test-projects/03-restful-booker-api/tests -q`
- 验证结果：目标测试 `2 passed in 0.10s`；API 全量 `9 passed in 0.44s`
- 证据目录：`artifacts/day-041/`
- 当天记录：`daily-log/day-041.md`

## Day 42：完整更新 PUT

### 核心知识点

PUT（资源替换）用于用一个完整表示替换已有资源。对需要认证的更新接口，测试必须同时验证认证头、完整请求体、PUT 即时响应和后续 GET 查询结果；只看到 `200` 不足以证明资源已正确更新。

### 它解决的问题

如果只断言 PUT 返回 `200` 或只检查响应体，测试可能漏掉服务端未持久化、部分字段被重置、认证头没有真正生效等问题。创建后使用动态 ID，再用 GET 回查，可以把“请求成功”和“状态已保存”分成两条证据链。

### 理论基础

| 检查层 | 代码证据 | 证明什么 |
| --- | --- | --- |
| 资源身份 | POST 返回的整数 `bookingid` | 本次测试操作的是自己创建的资源，而不是固定共享数据 |
| 认证 | `Cookie: token=<token>` | 更新请求携带了接口要求的认证凭据 |
| 请求完整性 | `json=UPDATE_PAYLOAD` 包含全部 booking 字段 | PUT 发送的是完整替换表示，而不是半截数据 |
| 即时响应 | PUT 返回 `200` 且响应体等于更新 payload | 服务端接受了更新并返回了预期表示 |
| 持久化结果 | 同一 ID 的 GET 等于更新 payload | 更新结果可再次读取，形成持久化证据 |
| 访问控制 | 无 Token 的 PUT 返回 `403` | 未认证调用不能执行受保护的更新 |

典型执行链：

```text
POST /booking
  → 读取动态 bookingid
  → POST /auth 获取 Token
  → PUT /booking/{id} + Cookie token + 完整 JSON
  → 验证 PUT 状态和响应体
  → GET /booking/{id}
  → 验证持久化资源与更新 payload 一致
```

### 认证头与请求体

本地 Restful Booker 接受 `Cookie: token=<token>` 作为 PUT 认证方式，也支持 Basic Auth。当前测试使用前一步 `/auth` 返回的动态 Token，避免把认证凭据重新编码或硬编码到更新请求中。`requests.put(..., json=payload)` 负责发送 JSON 请求体；`Accept: application/json` 表示期望 JSON 响应。

### 适用场景与边界

- 适用：资源需要整体替换，且接口契约要求更新对象包含全部字段。
- 适用：需要验证认证头、更新响应和服务端持久化的 CRUD 回归测试。
- 边界：如果业务只允许修改部分字段，应使用 PATCH 语义或明确的部分更新契约，不能用 PUT 测试代替。
- 边界：创建资源后要规划清理策略；本日测试产生的 booking 暂未删除，属于后续数据隔离与清理任务。
- 边界：不要固定使用 `/booking/1`，共享环境中的固定 ID 可能不存在、被其他测试修改或造成顺序依赖。

### 常见错误、反例与假通过

1. 只断言 PUT 返回 `200`，不比较响应体。
2. 只比较 PUT 响应，不做二次 GET，无法证明服务端已持久化。
3. PUT 只发送修改字段，却把它当成 PATCH 使用。
4. 忘记认证头，或把 Token 错放在 URL、普通请求体中。
5. 使用固定 booking ID，导致测试数据冲突和顺序依赖。
6. 把无 Token 的 `403` 误认为环境失败；对于受保护更新接口，这正是访问控制预期。
7. 测试创建数据后不清理，长期运行会污染环境并影响过滤、列表数量等其他测试。

### 记忆要点

**PUT 测试要证明四件事：ID 对、认证对、替换内容对、再次读取仍然对。**

### 代码落地

本日新增 `test_update_booking.py`。主测试创建 booking 并读取动态 ID，使用 `auth_credentials` 获取 Token，通过 Cookie 认证发送完整更新 payload，验证 PUT 响应后再 GET 回查。可选测试验证无 Token 时返回 `403`。

目标测试 2 条通过，API 全量回归 11 条通过。测试创建的数据尚未清理，已记录为后续 fixture 生命周期和 DELETE 清理策略的风险。

### 知识验收

1. 为什么 PUT 需要发送完整资源表示？
2. `Cookie: token=<token>` 在本日测试中证明什么？
3. 为什么二次 GET 是 PUT 测试的重要证据？
4. 为什么应该使用动态 `bookingid` 而不是固定 ID？
5. PUT 和 PATCH 的适用边界有什么不同？

### 关联产出

- 测试配置：`test-projects/03-restful-booker-api/tests/conftest.py`
- 测试文件：`test-projects/03-restful-booker-api/tests/test_update_booking.py`
- 验证命令：`.\\.venv\\Scripts\\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_update_booking.py -q`；`.\\.venv\\Scripts\\python.exe -m pytest test-projects/03-restful-booker-api/tests -q`
- 验证结果：目标测试 `2 passed in 0.18s`；API 全量 `11 passed in 0.31s`
- 证据目录：`artifacts/day-042/`
- 当天记录：`daily-log/day-042.md`

## Day 43：部分更新 PATCH

### 核心知识点

PATCH（部分更新）用于只修改资源中请求指定的字段，未指定字段应保持原值。它与 PUT 的区别不是“请求方法名称不同”这么简单，而是更新语义不同：PUT 通常提交完整资源表示，PATCH 只提交变化部分。

### 它解决的问题

当用户只想修改价格或附加需求时，使用部分更新可以减少请求数据和意外覆盖范围。测试如果只检查目标字段，很可能漏掉服务端把其他字段清空、重置或错误改写的问题，因此必须保留原始快照并比较完整预期。

### 理论基础

| 检查层 | 代码证据 | 证明什么 |
| --- | --- | --- |
| 资源身份 | 创建响应中的动态 `bookingid` | PATCH 操作的是本次测试创建的资源 |
| 部分请求 | `PATCH_PAYLOAD` 只有 `totalprice`、`additionalneeds` | 测试确实表达了部分更新，而不是完整替换 |
| 认证 | `Cookie: token=<token>` | 调用者有权限修改资源 |
| 目标字段 | PATCH 响应中的两个字段为新值 | 指定字段被正确修改 |
| 未修改字段 | 响应中的其他字段等于创建快照 | 部分更新没有破坏未指定字段 |
| 持久化 | 同一 ID 的 GET 等于合并后的预期 | 修改结果和未修改字段都已保存 |

部分更新的执行链：

```text
创建资源并保存原始快照
  → 获取 Token
  → PATCH /booking/{id}，只发送变化字段
  → 构造 original + patch 的独立预期
  → 验证 PATCH 响应的完整资源
  → GET 同一 ID
  → 验证指定字段已变、其他字段未变且结果已持久化
```

### 最小代码骨架

```python
PATCH_PAYLOAD = {
    "totalprice": 300,
    "additionalneeds": "Dinner",
}

expected_booking = {
    **CREATE_PAYLOAD,
    **PATCH_PAYLOAD,
}

response = requests.patch(
    booking_url,
    json=PATCH_PAYLOAD,
    headers={
        "Accept": "application/json",
        "Cookie": f"token={token}",
    },
    timeout=timeout,
)
assert response.status_code == 200
assert response.json() == expected_booking
```

这里的合并只用于构造独立预期，不是把 PATCH 请求改造成完整请求。请求仍然只包含 `PATCH_PAYLOAD` 中的两个字段。

### 适用场景与边界

- 适用：只修改资源部分字段，且接口契约明确未指定字段保持不变。
- 适用：验证局部修改不会破坏资源其他属性的 API 回归测试。
- 边界：不要根据方法名猜测语义；以实际 API 契约为准。
- 边界：如果接口的 PATCH 响应只返回部分字段，应对响应做局部断言，再用 GET 验证完整资源。
- 边界：创建的测试资源仍需清理；本日产生的数据未自动删除，属于后续生命周期任务。

### 常见错误、反例与假通过

1. PATCH 仍发送完整 `UPDATE_PAYLOAD`，实际测试成了 PUT。
2. 只断言 `totalprice` 和 `additionalneeds`，没有检查未修改字段。
3. 只验证 PATCH 响应，不做二次 GET，无法证明持久化结果。
4. 使用固定 booking ID，导致数据冲突或测试顺序依赖。
5. 忘记认证头，把 `403` 误判为 PATCH 逻辑失败。
6. 从页面或响应实际值反向构造 expected，导致服务端错误被测试接受。

### 记忆要点

**PATCH 测试要证明：只改该改的字段，其他字段不受影响，并且变化已经持久化。**

### 代码落地

本日保留 Day 42 的完整 PUT 和无 Token 403 测试，并在 `test_update_booking.py` 中新增 PATCH 用例。用例创建动态 booking，获取 Token，只发送 `totalprice` 和 `additionalneeds`，通过原始 payload 与 PATCH payload 的合并预期验证完整响应，再用 GET 验证持久化结果。

目标测试 3 条通过，API 全量回归 12 条通过。测试创建的数据尚未自动清理，已记录为后续 fixture 生命周期任务。

### 知识验收

1. PATCH 请求为什么只应包含要修改的字段？
2. 为什么必须断言未指定字段保持原值？
3. `expected_booking = {**CREATE_PAYLOAD, **PATCH_PAYLOAD}` 在测试中证明什么？
4. 为什么 PATCH 后仍然要二次 GET？
5. 什么情况下不能简单假设 PATCH 响应一定包含完整资源？

### 关联产出

- 测试配置：`test-projects/03-restful-booker-api/tests/conftest.py`
- 测试文件：`test-projects/03-restful-booker-api/tests/test_update_booking.py`
- 验证命令：`.\\.venv\\Scripts\\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_update_booking.py -q`；`.\\.venv\\Scripts\\python.exe -m pytest test-projects/03-restful-booker-api/tests -q`
- 验证结果：目标测试 `3 passed in 0.11s`；API 全量 `12 passed in 0.48s`
- 证据目录：`artifacts/day-043/`
- 当天记录：`daily-log/day-043.md`

## Day 44：删除与清理

### 核心知识点

资源生命周期和清理保证要求接口测试关注资源从创建到销毁的完整状态变化。DELETE 的成功状态只证明删除请求被接口接受；使用同一个动态 ID 进行删除后 GET，才能验证资源已经不可读取。

### 它解决的问题

如果测试只断言 DELETE 返回成功，服务端即使没有真正删除资源，测试也可能通过。测试数据如果不清理，还会污染共享环境，影响后续列表、过滤和数量断言。动态创建并删除自己的资源，可以降低固定数据、测试顺序和误删共享资源的风险。

### 理论基础

#### 定义与关键概念

- 资源生命周期（resource lifecycle）：创建、读取或修改、删除，以及删除后的状态确认。
- 清理保证（cleanup guarantee）：测试结束时，测试创建的临时资源已被删除，或失败时有明确的补偿清理策略。
- 动态资源 ID：从本次 POST 响应读取的 `bookingid`，用于后续 DELETE 和 GET，保证操作对象属于当前测试。

#### 心智模型或执行链

```text
POST /booking
  → 读取本次响应的 bookingid
  → POST /auth 获取 Token
  → DELETE /booking/{bookingid} + Cookie token
  → 验证 DELETE 状态码 201
  → GET /booking/{bookingid}
  → 验证资源不存在，状态码 404
```

DELETE 响应是即时证据，删除后 GET 是后置证据；两者共同证明“请求成功”和“资源已不可读取”这两个不同事实。

#### 最小代码骨架

```python
booking_id = create_booking()
token = get_auth_token()
booking_url = f"{base_url}/booking/{booking_id}"

delete_response = requests.delete(
    booking_url,
    headers={"Cookie": f"token={token}"},
    timeout=timeout,
)
assert delete_response.status_code == 201

get_response = requests.get(booking_url, timeout=timeout)
assert get_response.status_code == 404
```

#### 断言、数据或状态的含义

| 检查 | 证明什么 | 不能单独证明什么 |
| --- | --- | --- |
| POST 返回动态 `bookingid` | 后续请求有明确的本次资源身份 | 不能证明删除成功 |
| DELETE 返回 `201` | 本地接口接受并完成了删除操作 | 不能单独证明资源已不可查询 |
| 删除后 GET 返回 `404` | 同一资源已经不再可读取 | 不能证明其他资源未受影响 |
| 重复 DELETE 返回 `405` | 本地契约对已不存在资源有明确处理 | 不应泛化为所有 DELETE 接口的通用规则 |

#### 适用场景与边界

- 适用：API CRUD 测试、临时测试数据、共享测试环境和需要回归执行的资源测试。
- 适用：创建资源后必须由当前测试负责销毁的场景，可用 fixture finalizer 或 `try/finally` 增加失败补偿清理。
- 边界：删除后的状态码、重复删除状态码必须以当前 API 契约为准；本地 Restful Booker 的观察结果是 DELETE `201`、删除后 GET `404`、重复 DELETE `405`。
- 边界：如果删除是异步操作，不能立即假设 GET 一定马上返回 `404`，需要轮询、最终一致性等待或接口提供的任务状态。
- 边界：不要为了“清理”删除共享数据或固定 ID；清理对象必须是本次测试创建并持有的资源。

#### 常见错误、反例与假通过

1. 只断言 DELETE 返回成功，不做删除后 GET，无法证明资源真的消失。
2. 删除后 GET 使用固定 ID，无法证明查询的是刚刚删除的资源。
3. 使用固定 booking ID 作为删除对象，可能误删其他测试或共享环境数据。
4. 创建资源后中途断言失败，没有补偿清理，导致数据泄漏到后续回归。
5. 把 `404` 或 `405` 当成所有 API 的通用 DELETE 规则，忽略具体接口契约。
6. 把“测试方法执行完”误认为“测试数据已经清理”；清理必须有请求和后置断言证据。

#### 记忆要点

**删除测试要证明：删的是自己的资源、DELETE 成功、删后确实查不到；清理是测试结果的一部分，不是附加动作。**

### 代码落地

本日新增 `test_delete_booking.py`。主场景先创建 booking 并读取动态 ID，再获取 Token，通过 Cookie 执行 DELETE，验证 `201`，然后用同一个 ID GET 并验证 `404`。可选挑战在同一动态资源上重复 DELETE，验证本地契约返回 `405`。

目标测试 2 条通过，API 全量回归 14 条通过。测试创建的数据在主流程和挑战流程中都被删除，未留下本日测试资源。

### 知识验收

1. 为什么 DELETE 返回成功后仍然要 GET 同一个动态 ID？
2. 动态 ID 在删除测试中解决了什么数据归属问题？
3. DELETE 的即时响应和删除后 GET 分别证明什么？
4. 为什么测试数据清理属于测试结果的一部分？
5. 如果删除是异步的，为什么不能立即断言 GET 返回 `404`？

### 关联产出

- 测试文件：`test-projects/03-restful-booker-api/tests/test_delete_booking.py`
- 验证命令：`.\\.venv\\Scripts\\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_delete_booking.py -q`；`.\\.venv\\Scripts\\python.exe -m pytest test-projects/03-restful-booker-api/tests -q`
- 验证结果：目标测试 `2 passed in 0.18s`；API 全量 `14 passed in 0.86s`
- 证据目录：`artifacts/day-044/`
- 当天记录：`daily-log/day-044.md`

## Day 45：API Client

### 核心知识点

API Client 是接口测试中的通用传输层（transport layer）边界：集中处理 base URL、timeout、公共 headers、URL 拼接和 HTTP 请求发送，让测试用例专注于业务动作和结果断言。

### 它解决的问题

如果每个测试都重复拼接 URL、设置 timeout 和 headers，配置变化时容易漏改，测试之间也可能出现行为不一致。把这些协议细节集中起来，可以降低维护成本；同时不把业务断言放进 Client，可以避免 Client 用一个固定状态码覆盖成功、鉴权失败、资源不存在等不同场景。

### 理论基础

#### 定义与关键概念

- 通用客户端（API Client）：对 HTTP 库的薄封装，统一请求入口和传输配置。
- 公共配置：base URL、默认 `Accept`、请求 timeout 等所有接口通常共享的配置。
- 业务断言：具体测试场景对状态码、响应字段、数据一致性和业务规则的预期。
- 请求错误上下文：网络异常发生时用于定位的 method、URL、params、timeout 和安全响应摘要。

#### 心智模型或执行链

```text
测试用例：表达业务动作和预期
  → api_client fixture：注入统一配置
  → RestfulBookerClient：拼接 URL、合并 headers、发送请求
  → requests：执行 HTTP
  → Response：返回给测试
  → 测试：断言状态码、响应体和业务结果
```

Client 负责“怎么请求”，测试负责“结果应该是什么”。二者分离后，同一个 Client 可以服务于预期 `200`、`201`、`403`、`404` 或 `405` 的不同测试。

#### 最小代码骨架

```python
class RestfulBookerClient:
    def __init__(self, base_url, timeout):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.default_headers = {"Accept": "application/json"}

    def get(self, path, *, params=None, headers=None, token=None):
        return self._request(
            "GET",
            path,
            params=params,
            headers=headers,
            token=token,
        )
```

`_request()` 统一完成 URL、headers 和 timeout 的处理；HTTP 响应原样返回给测试，不能在这里替测试固定断言状态码。

#### 断言、数据或状态的含义

| 检查 | 证明什么 | 不能单独证明什么 |
| --- | --- | --- |
| Client 统一生成 URL | 请求目标和路径拼接规则集中管理 | 不能证明业务资源内容正确 |
| Client 统一传递 timeout | 请求有一致的阻塞上限 | 不能证明服务端在该时间内返回正确结果 |
| 默认/覆盖 headers 合并 | 公共协议头可复用，场景头仍可覆盖 | 不能证明认证或业务授权成功 |
| Client 返回原始 Response | 测试可以按场景断言 `200`、`403`、`404` 等 | 不能替测试决定某个状态码就是正确结果 |
| 网络异常包含安全上下文 | 能定位方法、URL、params 和 timeout | 不能把网络异常自动归因成产品缺陷 |

#### 适用场景与边界

- 适用：多个接口测试重复使用相同的 base URL、timeout、headers 和 HTTP 发送逻辑。
- 适用：需要在测试环境之间切换地址，或希望统一网络异常格式的回归测试。
- 边界：Client 不应包含具体业务断言、固定资源 ID 或某一个测试场景专属的 expected 值。
- 边界：不要为了统一错误处理而对所有响应调用 `raise_for_status()`；负向测试需要拿到 `403`、`404`、`405` 后自行断言。
- 边界：错误日志可以记录非敏感请求上下文，但必须对 Token、Cookie、密码和可能包含凭据的响应字段脱敏。
- 边界：当前 Client 只抽取通用 HTTP 细节；`create_booking()`、`get_booking()` 等 booking 业务语义适合后续领域客户端继续封装。

#### 常见错误、反例与假通过

1. Client 文件放在测试目录或项目根目录，导致目标模块位置不明确或出现重复实现。
2. 只创建 Client，不让测试通过 Fixture 使用，表面有封装，实际仍重复调用 `requests`。
3. 在 Client 中写 `assert response.status_code == 200`，导致 `403`、`404`、`405` 场景无法复用。
4. 每个测试继续声明自己的 BASE_URL、BOOKING_URL 和 timeout，造成配置漂移。
5. 异常信息只写 `AssertionError`，缺少 method、URL、params 和 timeout，排查成本高。
6. 为了记录响应而直接打印 headers 或完整响应体，泄露 Token、Cookie 或密码。

#### 记忆要点

**Client 负责统一“怎么请求”，测试负责判断“结果是否正确”；封装重复协议细节，但不要封装具体业务预期。**

### 代码落地

本日将 Client 放入 `src/api_client.py`，通过 `tests/conftest.py` 的 `api_client` fixture 注入 base URL 和 timeout。健康检查、查询、创建、过滤、鉴权、PUT、PATCH 和 DELETE 测试均改为调用 `api_client.get/post/put/patch/delete`，直接调用 `requests` 只保留在 Client 内部。

Client 统一生成相对路径对应的完整 URL，合并默认 `Accept` header 和场景 headers，并通过 `token` 参数生成 Cookie。业务状态码、响应字段和资源生命周期断言继续留在测试中；网络异常则包装为带安全上下文的 `ApiRequestError`。

目标范围内的 API 全量回归为 14 条测试，全部通过。

### 知识验收

1. API Client 和测试用例分别负责什么？
2. 为什么 Client 不能统一断言 `response.status_code == 200`？
3. Fixture 在 Client 接入中解决了什么问题？
4. 哪些请求信息应该进入错误上下文，哪些敏感信息必须脱敏？
5. 为什么“创建了 Client”但测试仍直接调用 `requests` 不算完成封装？

### 关联产出

- Client：`test-projects/03-restful-booker-api/src/api_client.py`
- Fixture：`test-projects/03-restful-booker-api/tests/conftest.py`
- 迁移测试：`test-projects/03-restful-booker-api/tests/`
- 验证命令：`.\\.venv\\Scripts\\python.exe -m pytest test-projects/03-restful-booker-api/tests -q`
- 验证结果：API 全量回归 `14 passed in 0.37s`
- 证据目录：`artifacts/day-045/`
- 当天记录：`daily-log/day-045.md`

## Day 46：Booking Client

### 核心知识点

领域客户端（domain client）位于通用 HTTP Client 和测试用例之间，用业务对象和动作封装 endpoint 映射。对本项目而言，`BookingClient` 负责表达 booking 的创建、列表查询、详情查询、整体更新、部分更新和删除；测试继续负责验证 HTTP 状态、响应结构和业务结果。

### 它解决的问题

如果每个测试都知道 `/booking` 路径、HTTP 方法和参数组织方式，接口路径变化时需要批量修改，测试也会被协议细节淹没。领域 Client 可以让测试写出 `booking_client.create_booking(payload)` 这样的业务动作，同时避免把状态码或业务 expected 隐藏在封装内部。

### 理论基础

#### 三层职责模型

| 层次 | 负责什么 | 不负责什么 |
| --- | --- | --- |
| `RestfulBookerClient` | base URL、timeout、headers、HTTP 方法、请求发送、网络异常 | 不知道 booking 业务语义，不决定业务状态码 |
| `BookingClient` | booking endpoint 映射、领域参数组织、Token 传递 | 不断言 `200`、`404` 或响应字段，不吞掉原始响应 |
| 测试用例 | 场景编排、状态码、响应结构、字段和业务规则断言 | 不重复拼接 booking URL，不直接处理通用 HTTP 细节 |

职责边界可以记成：

```text
RestfulBookerClient：怎么发送 HTTP
        ↓
BookingClient：对 booking 做什么
        ↓
测试用例：结果应该是什么
```

#### 领域方法与 endpoint 映射

| 领域方法 | HTTP 请求 | 测试关注点 |
| --- | --- | --- |
| `create_booking(payload)` | `POST /booking` | `200`、bookingid、返回对象和请求字段 |
| `get_bookings(params)` | `GET /booking` | 列表类型、元素结构和过滤结果 |
| `get_booking(booking_id)` | `GET /booking/{id}` | 动态 ID 对应的详情和持久化结果 |
| `update_booking(id, payload, token)` | `PUT /booking/{id}` | 完整替换、认证和响应一致性 |
| `partial_update_booking(id, payload, token)` | `PATCH /booking/{id}` | 指定字段变化和未指定字段保护 |
| `delete_booking(id, token)` | `DELETE /booking/{id}` | 删除状态、删除后查询和重复删除契约 |

#### 为什么返回原始 Response

领域方法当前返回原始 `requests.Response`：

```python
response = booking_client.create_booking(payload)

assert response.status_code == 200
data = response.json()
assert isinstance(data["bookingid"], int)
assert data["booking"] == payload
```

这样测试仍能同时验证 HTTP 层和业务层。如果领域方法只返回 JSON 或 bookingid，可能丢失状态码、headers、错误响应和原始响应结构；直接读取 `bookingid` 还可能把接口错误变成难定位的 `KeyError`。

以后可以增加 `create_booking_id()` 之类的数据准备辅助方法，但它不能替代核心领域方法的原始 Response 返回。

#### 适用场景与边界

- 适用：同一业务资源有多个 CRUD 场景，测试重复出现 endpoint 和参数组织逻辑时。
- 适用：希望测试用例表达业务动作，同时保留底层响应供断言的接口回归框架。
- 边界：不要把所有资源和所有业务规则塞入一个万能 Client；每个领域 Client 应围绕一个资源或有限的业务边界。
- 边界：不要在领域方法中固定断言状态码，否则成功、鉴权失败、资源不存在等场景无法复用。
- 边界：本日只封装 Booking Client，Token 获取仍由通用 `api_client` 完成；独立 `AuthClient` 可以作为后续演进。

#### 常见错误、反例与假通过

1. 新建 `BookingClient` 但测试仍直接调用 `api_client`，造成“有封装、未使用”的假完成。
2. 在 `BookingClient` 中写 `assert response.status_code == 200`，破坏负向测试和不同 endpoint 契约。
3. 领域方法直接返回 `response.json()["bookingid"]`，隐藏状态码和错误响应。
4. 领域 Client 继续让测试传入完整 `/booking/{id}` URL，说明 endpoint 边界没有真正封装。
5. 把鉴权 Token 获取逻辑强行放进 Booking Client，导致 booking 和 auth 两个领域耦合。
6. 为了简化测试而吞掉原始 Response，使测试无法验证 HTTP 状态和 headers。

#### 记忆要点

**通用 Client 处理 HTTP，领域 Client 表达资源动作，测试保留业务验证；领域封装减少重复，但不能隐藏证据。**

### 代码落地

本日新增 `src/booking_client.py` 和 `booking_client` Fixture。Booking 相关测试已经从 `api_client.post("/booking")` 等底层调用迁移为 `booking_client.create_booking()`、`get_booking()`、`update_booking()`、`partial_update_booking()` 和 `delete_booking()`。

领域方法只负责 endpoint 映射、payload 和 Token 传递，并返回原始 Response。健康检查和认证测试仍使用通用 `api_client`，因此三层边界保持清晰。

目标范围内 API 全量回归为 14 条测试，全部通过。

### 知识验收

1. 通用 Client、领域 Client 和测试分别负责什么？
2. 为什么 `BookingClient` 不应该直接断言状态码？
3. 为什么领域方法当前返回原始 Response？
4. `create_booking()` 与 `create_booking_id()` 的职责有什么不同？
5. 为什么本日没有把 Token 获取放进 `BookingClient`？

### 关联产出

- 领域 Client：`test-projects/03-restful-booker-api/src/booking_client.py`
- 通用 Client：`test-projects/03-restful-booker-api/src/api_client.py`
- Fixture：`test-projects/03-restful-booker-api/tests/conftest.py`
- 迁移测试：`test-projects/03-restful-booker-api/tests/`
- 验证命令：`.\\.venv\\Scripts\\python.exe -m pytest test-projects/03-restful-booker-api/tests -q`
- 验证结果：API 全量回归 `14 passed in 0.73s`
- 证据目录：`artifacts/day-046/`
- 当天记录：`daily-log/day-046.md`

## Day 47：Fixture 生命周期

### 核心知识点

`yield fixture` 用于管理测试资源的完整生命周期：`yield` 前属于 setup，负责获取 Token 和创建 booking；`yield` 后属于 teardown，负责回收测试创建的资源。

### 它解决的问题

如果测试各自创建 booking，却没有统一清理，测试运行会污染共享环境，也可能在断言失败后遗留数据。把创建和清理放进同一个 Fixture，可以让测试只关注业务验证，并使资源回收逻辑集中、可复用。

### 理论基础

#### setup、测试和 teardown

```text
Fixture setup：获取 Token → 创建 booking → yield 动态 bookingid
                                      ↓
                                  测试执行
                                      ↓
Fixture teardown：GET 同一 bookingid → 仍存在则 DELETE
```

`yield` 之后的代码会在测试结束时执行，即使测试中的断言失败或测试抛出异常。通常将清理放在 `try/finally` 中，避免测试主体异常时跳过 teardown。

#### 动态资源和清理契约

- 必须使用创建响应中的动态 `bookingid`，确保清理的是本次测试自己的资源。
- 清理前可先 GET：返回 `200` 表示资源仍存在，需要 DELETE；返回 `404` 表示测试本身已经删除，视为清理完成。
- DELETE 成功状态应按接口契约断言；本项目使用 `201`，并将删除竞态下的 `404` 视为幂等清理结果。
- Token 应在创建前获取，避免资源创建成功后鉴权失败而无法回收。

#### 容错、幂等和失败隔离

清理逻辑应尽量幂等：执行一次或重复执行，最终都应达到“资源不存在”的状态。测试本身已经删除资源时，Fixture 不应再次删除并制造假失败。另一方面，teardown 中的错误信息也要清晰，避免清理失败完全掩盖原始测试失败；网络异常、不可预期状态码等策略可按项目需要继续增强。

#### 常见错误、反例与假通过

1. 只定义 `created_booking` Fixture，却没有任何测试使用它，形成“有封装、未生效”的假完成。
2. 把删除写在测试主体末尾，测试中途断言失败时清理代码不会执行。
3. 使用固定 bookingid 清理，可能误删历史数据或删除其他测试的资源。
4. 测试主动删除后，Fixture 无条件再次 DELETE，把正常的 `404` 误判为失败。
5. teardown 直接用严格断言处理所有异常，导致清理问题掩盖原始业务断言失败。
6. 只验证 DELETE 返回成功，不用同一个动态 ID 回查资源是否真的不存在。

#### 记忆要点

**Fixture 管理资源生命周期，`yield` 分隔 setup 和 teardown；清理必须放在 `finally` 思维下设计，并对重复清理保持容错和幂等。**

### 代码落地

本日完善 `tests/conftest.py` 中的 `created_booking` Fixture：统一获取 Token、创建 booking，并将 `booking_id`、Token 和原始 payload 提供给测试；测试结束后通过 `finally` 查询并删除资源。

删除测试和无 Token 更新测试已实际使用该 Fixture。删除测试主动删除资源后，Fixture 收到 `404` 会跳过重复删除；若测试在断言处失败，Fixture 仍会进入 teardown。

### 知识验收

1. 为什么 booking 的创建和删除适合放在同一个 `yield fixture` 中？
2. 测试断言失败时，为什么 `yield` 后的清理代码仍会执行？
3. 为什么要使用本次创建响应中的动态 `bookingid`？
4. 测试本身已删除资源时，Fixture 应如何避免重复删除失败？
5. 为什么资源清理应尽量设计成幂等？

### 关联产出

- Fixture：`test-projects/03-restful-booker-api/tests/conftest.py`
- 使用 Fixture 的删除测试：`test-projects/03-restful-booker-api/tests/test_delete_booking.py`
- 使用 Fixture 的鉴权负向测试：`test-projects/03-restful-booker-api/tests/test_update_booking.py`
- 验证命令：`.\.venv\Scripts\pytest.exe tests -q`
- 验证结果：API 全量回归 `14 passed in 0.56s`
- 证据文件：`artifacts/day-047/verification.md`
- 当天记录：`daily-log/day-047.md`

## Day 48：数据工厂

### 核心知识点

测试数据工厂（data factory）用一个可复用函数集中生成测试数据。它提供完整、合法的默认基线，通过 `overrides` 允许具体测试只修改当前真正关心的字段，并为每次调用生成可区分的数据。

### 它解决的问题

把 payload 直接散落在测试函数中，会导致重复、固定数据冲突和修改成本高。所有测试共用同一个可变字典，还可能因为一个测试修改嵌套字段而污染另一个测试。数据工厂将数据准备与业务验证分离，使测试主体更短、更清楚。

### 理论基础

#### 三个设计原则

| 设计元素 | 作用 | 本项目实现 |
| --- | --- | --- |
| 唯一字段 | 隔离测试数据，减少冲突和相互污染 | 使用 `uuid4` 生成唯一 `firstname` |
| 默认字段 | 提供合法、完整、可直接发送的基线 | 默认价格、押金状态、日期和附加需求 |
| `overrides` | 让场景只改变真正关注的条件 | `build_booking_payload(totalprice=999)` |

可以把数据工厂记成：

```text
合法默认基线 + 唯一标识 + 场景覆盖
                  ↓
         独立、可复用的测试 payload
```

#### 覆盖和嵌套字段

工厂先创建完整默认对象，再应用调用方传入的覆盖值。顶层字段可以直接覆盖；`bookingdates` 等嵌套对象应进行局部合并，避免只覆盖 `checkin` 时丢失默认的 `checkout`。

覆盖操作应使用深拷贝或每次新建对象，不能直接修改共享默认字典。否则测试 A 对 `bookingdates` 的修改可能改变测试 B 后续得到的数据。

#### 唯一性和合法性的边界

唯一不等于随机到不可复现。唯一值应放在不影响业务规则的字段中，并控制长度和格式；日期、价格、布尔字段等仍应遵守 API 合法约束。工厂负责准备数据，不负责发送 HTTP 请求，也不负责断言响应结果。

#### 常见错误、反例与假通过

1. 创建了工厂但没有任何测试调用，形成“有封装、未生效”的假完成。
2. 使用模块级可变 `DEFAULT_PAYLOAD`，测试修改嵌套字段后污染其他测试。
3. 只做浅拷贝，导致顶层字典独立但 `bookingdates` 仍然共享。
4. 只覆盖 `checkin` 却直接替换整个 `bookingdates`，意外丢失 `checkout`。
5. 唯一值过长、格式不合法或放入有业务语义限制的字段，导致数据生成本身制造失败。
6. 把 HTTP 请求、状态码断言或业务规则塞进工厂，混淆数据准备和测试验证职责。

#### 记忆要点

**唯一字段负责隔离，默认字段负责合法基线，`overrides` 负责场景差异；每次调用返回独立数据，工厂只准备数据，不执行请求和断言。**

### 代码落地

本日新增 `tests/factories.py` 中的 `build_booking_payload(**overrides)`：使用 `uuid4` 生成唯一 `firstname`，动态生成未来日期，复制覆盖参数，并对 `bookingdates` 做局部合并。

创建测试、创建后查询流程、PUT/PATCH 测试和 booking Fixture 已迁移到数据工厂；新增工厂行为测试，验证唯一性、默认值保留、覆盖能力和嵌套对象隔离。

### 知识验收

1. 数据工厂中的唯一字段、默认字段和 `overrides` 分别解决什么问题？
2. 为什么每次调用工厂都应返回独立字典？
3. 为什么 `bookingdates` 适合采用局部合并而不是直接整体替换？
4. 数据工厂为什么不应该负责发送 HTTP 请求或业务断言？
5. 如何在保证唯一性的同时维持测试数据的合法性和可维护性？

### 关联产出

- 数据工厂：`test-projects/03-restful-booker-api/tests/factories.py`
- 工厂行为测试：`test-projects/03-restful-booker-api/tests/test_factories.py`
- 接入测试：`test-projects/03-restful-booker-api/tests/test_create_booking.py`、`test_booking_flow.py`、`test_update_booking.py`
- Fixture 接入：`test-projects/03-restful-booker-api/tests/conftest.py`
- 验证证据：`artifacts/day-048/verification.md`
- 当天记录：`daily-log/day-048.md`

## Day 49：参数化边界

### 核心知识点

参数化边界测试把“相同的请求步骤和断言逻辑”与“不同的输入数据和预期结果”分离。`pytest.mark.parametrize` 会将每组参数作为独立测试执行和报告，适合系统覆盖价格、日期、姓名等字段的正常边界、极限边界和非法边界。

### 它解决的问题

如果每个边界都复制一个测试函数，代码重复、维护成本高，也容易只修改了其中一个 case 的断言。参数化把测试流程集中到一个函数，把覆盖范围集中到参数表；新增边界通常只需要增加一行数据，并可通过 `id` 让失败报告直接说明是哪种输入。

### 理论基础

#### 边界数据的三类

| 类型 | 含义 | 例子 | 预期处理 |
| --- | --- | --- | --- |
| 正常边界 | 合法范围的最小、最大或临界值 | `totalprice=0`、单字符姓名 | 按契约成功，并验证响应字段和持久化 |
| 极限边界 | 接近长度、数值或时间范围限制的输入 | 大价格、超长姓名、同日入住退房 | 按明确规则接受或拒绝 |
| 非法边界 | 类型、格式或业务关系不合法 | 负数价格、非法日期、`checkout < checkin` | 通常应返回明确的 4xx，并说明错误 |

设计边界时不能只写“我觉得应该是 400”。状态码、响应体和业务规则要分别记录：接口可能接受请求，但业务上仍然是不应该接受的输入。

#### 参数化的最小结构

```python
BOUNDARY_CASES = [
    pytest.param(
        {"totalprice": 0},
        200,
        {("totalprice",): 0},
        id="price-zero-accepted",
    ),
]


@pytest.mark.parametrize(
    ("overrides", "expected_status", "expected_fields"),
    BOUNDARY_CASES,
)
def test_boundary(overrides, expected_status, expected_fields):
    payload = build_booking_payload(**overrides)
    response = create_booking(payload)

    assert response.status_code == expected_status
```

参数表至少应包含：输入值、HTTP 预期、成功时需要核对的业务字段；测试 ID 应体现边界含义，而不是只使用 `case1`、`case2`。

#### 完整验证链

```text
参数化输入
    ↓
构造合法基线并覆盖指定字段
    ↓
发送请求并验证 HTTP 状态码
    ↓
验证响应字段或错误信息
    ↓
成功时使用动态 ID GET 回查持久化
    ↓
清理本次创建的资源
```

`200` 只说明请求被接口处理，不能单独证明业务规则正确。成功场景要继续检查响应体和 GET 结果；非法场景要把业务预期与接口当前行为对照，避免为了让测试变绿而修改正确预期。

#### 使用 `xfail` 记录已确认的接口缺陷

当业务契约明确要求拒绝某个输入，但当前服务实际返回成功时，可以使用严格的 `xfail` 暂时保留预期：

```python
pytest.param(
    {"totalprice": -1},
    400,
    {},
    marks=pytest.mark.xfail(
        strict=True,
        reason="当前接口接受负数价格，缺少业务校验。",
    ),
    id="price-negative-should-reject",
)
```

`xfail` 不是把缺陷隐藏起来：当前行为不符合预期时报告为 xfailed；接口修复后如果仍保留标记，`strict=True` 会产生 XPASS 并提醒测试维护者删除该标记、恢复正常断言。

### 常见错误、反例与假通过

1. 只断言所有 case 都返回 `200`，没有验证边界值是否被正确保存或转换。
2. 看到接口对非法输入返回 `200`，就把预期偷偷改成 `200`，把业务缺陷伪装成测试通过。
3. 所有参数使用同一个固定 ID，导致边界测试之间互相修改或污染数据。
4. 测试创建资源后不清理，重复执行或全量回归时让数据环境持续膨胀。
5. 参数没有 `id`，失败报告只显示 `case0`，定位具体边界需要重新翻代码。
6. 只覆盖无效值，缺少 0、1、单字符、同日等合法临界值，无法证明接口对合法边界的支持。
7. 将“HTTP 请求被接受”“字段被保存”和“业务规则满足”混成一个断言，无法准确分类问题。

### 记忆要点

**参数化负责扩大输入覆盖，ID 负责解释失败，状态码负责验证接口处理结果，响应体和回查负责验证数据与持久化，业务契约负责判断输入是否应该被接受。**

### 代码落地

本日新增 `tests/test_boundaries.py`，用一套创建、动态 ID 回查和清理流程覆盖价格、日期、姓名共 12 组参数。6 组合法边界正常通过；6 组业务上应拒绝但当前接口接受的场景使用 `strict=True` 标记为 xfailed，明确保留校验缺陷证据。

受控探测确认当前接口会接受负数价格、字符串价格、空或纯空格姓名、日期倒置和非法日期；其中部分值会被转换后保存。这些现象不能仅凭 `200` 判定为业务正确。

### 知识验收

1. 参数化测试解决了什么重复问题？参数表至少需要包含哪些信息？
2. 为什么 `200` 不能单独证明边界输入符合业务规则？
3. 正常边界、极限边界和非法边界如何区分？
4. 什么时候可以使用严格 `xfail`？接口修复后如何避免遗留标记？
5. 为什么边界测试成功创建后仍要使用动态 ID 回查并清理？

### 关联产出

- 参数化边界测试：`test-projects/03-restful-booker-api/tests/test_boundaries.py`
- 数据工厂：`test-projects/03-restful-booker-api/tests/factories.py`
- 验证命令：`.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q`
- 验证结果：目标测试 `6 passed, 6 xfailed`；API 全量回归 `22 passed, 6 xfailed`
- 验证证据：`artifacts/day-049/verification.md`
- 当天记录：`daily-log/day-049.md`

## Day 50：缺失字段

### 核心知识点

API 负向测试验证接口收到缺失、错误、越界或不符合业务规则的请求时，是否能够正确拒绝、返回可理解的错误，并且不产生错误数据。它不只是验证“请求失败”，还要验证失败的 HTTP 状态、错误信息、数据状态和后续影响。

### 它解决的问题

只覆盖正常请求，只能证明合法输入在一个路径上可用，不能证明接口足够健壮。缺失必填字段可能导致 500、脏数据、异常资源或不明确错误，进而影响后续查询、更新、统计和其他测试。负向测试将这些输入边界固化为可重复回归的契约。

### 理论基础

#### 缺失字段测试矩阵

对于 booking，核心必填字段包括：

```text
firstname
lastname
totalprice
depositpaid
bookingdates
    checkin
    checkout
```

`additionalneeds` 更适合作为可选字段。逐个删除字段时，应保留其他字段合法，确保失败原因只来自当前被删除的字段。

| 缺失字段 | 业务预期 | 需要观察的实际行为 |
| --- | --- | --- |
| `firstname` | `400`，说明必填 | 是否返回 400、500 或错误创建 |
| `lastname` | `400`，说明必填 | 是否返回明确错误 |
| `totalprice` | `400`，说明必填 | 是否发生服务端异常 |
| `depositpaid` | `400`，说明必填 | 是否被错误设置默认值 |
| `bookingdates` | `400`，说明必填 | 是否返回结构性错误 |
| `bookingdates.checkin` | `400`，说明必填 | 是否错误接受不完整嵌套对象 |
| `bookingdates.checkout` | `400`，说明必填 | 是否错误接受不完整嵌套对象 |

业务预期和当前实现必须分开：如果契约要求 400，而服务实际返回 500，应记录为错误处理缺陷；不能为了让测试通过而把 `expected_status` 改成 500。

#### 负向测试的验证层次

```text
构造合法完整基线
    ↓
只删除一个目标字段
    ↓
验证 HTTP 状态码
    ↓
验证错误信息或响应结构
    ↓
确认没有创建错误资源
    ↓
如果错误创建，使用动态 ID 清理
```

状态码验证接口如何处理请求，响应体验证错误是否可解释，业务契约验证拒绝是否符合要求。三者不能混成一个“不是 200 就算通过”的断言。

#### 断言失败后的资源清理

负向测试本身也要考虑被测服务出错的情况。如果接口本应返回 400，却错误地返回 200 并创建 booking，那么断言必须失败，但测试仍要清理资源：

```python
booking_id = None

try:
    response = booking_client.create_booking(invalid_payload)
    booking_id = extract_booking_id(response)

    assert response.status_code == 400
finally:
    cleanup_booking(booking_id, token)
```

把清理写在断言之后是不安全的，因为断言一旦失败，后续清理语句不会执行。`try/finally` 确保测试结论和资源回收彼此独立。

#### 使用严格 `xfail` 留存已确认缺陷

当合理业务预期已经明确，但当前服务的行为不符合预期时，可以对参数化 case 使用：

```python
pytest.param(
    "firstname",
    400,
    marks=pytest.mark.xfail(
        strict=True,
        reason="当前接口缺少 firstname 时返回 500，应返回 400。",
    ),
    id="missing-firstname",
)
```

这表示“测试预期仍然是 400，当前服务缺陷已知且可复现”，而不是把 500 认定为正确。`strict=True` 还能在服务修复后产生 XPASS，提醒维护者移除临时标记、恢复正常通过断言。

### 常见错误、反例与假通过

1. 只断言请求没有返回 200，不区分合理的 400、错误的 500 和其他异常状态。
2. 当前服务返回 500，就把预期改为 500，导致测试失去需求约束。
3. 一次删除多个字段，无法判断到底是哪一个字段触发了行为。
4. 只验证状态码，不验证错误信息、响应结构和是否创建了资源。
5. 把清理放在断言之后，断言失败时留下接口错误创建的 booking。
6. 复用并原地修改同一个 payload，使后面的缺失字段 case 受到前一个 case 影响。
7. 把可选字段当成必填字段，造成错误的产品缺陷记录。

### 记忆要点

**负向测试要验证拒绝方式，不是只验证失败；一次只缺失一个字段，预期不能迎合实现，断言失败也必须清理异常资源。**

### 代码落地

本日新增 `tests/test_invalid_payloads.py`，使用 `pytest.mark.parametrize` 覆盖 7 个 booking 必填字段缺失场景。每个 case 从数据工厂生成独立合法基线，再按点号路径删除一个字段，预期统一为 `400 Bad Request`。

本地接口对 7 组场景均返回 `500 Internal Server Error`，因此测试以 `strict=True xfail` 留证。测试还会提取错误返回 `200` 时的动态 `bookingid`，在 `finally` 中清理，避免负向测试污染环境。

### 知识验收

1. API 负向测试除了验证失败，还应验证哪些方面？
2. 为什么缺失字段必须一次只删除一个？
3. 业务预期为 400、实际返回 500 时，测试和缺陷应该如何记录？
4. 为什么异常资源清理必须放进 `finally`？
5. `strict=True xfail` 在当前接口缺陷被修复后有什么作用？

### 关联产出

- 缺失字段负向测试：`test-projects/03-restful-booker-api/tests/test_invalid_payloads.py`
- 数据工厂：`test-projects/03-restful-booker-api/tests/factories.py`
- 领域 Client：`test-projects/03-restful-booker-api/src/booking_client.py`
- 验证命令：`.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q`
- 验证结果：目标测试 `7 xfailed`；API 全量回归 `22 passed, 13 xfailed`
- 验证证据：`artifacts/day-050/verification.md`
- 当天记录：`daily-log/day-050.md`

## Day 51：类型错误

### 核心知识点

API 输入类型边界（input type boundary）验证请求中的 JSON 值是否使用契约规定的数据类型。一个值看起来能够被转换成正确含义，不代表它符合接口契约；服务端静默转换错误类型会掩盖调用方缺陷，并可能把非规范数据写入系统。

### 它解决的问题

只测试合法 payload，无法证明接口能安全拒绝错误类型。只要服务端恰好能把 `"200"` 转成 `200`，一个只看 200 响应的测试就会假通过。类型负向测试明确区分“请求符合契约”和“实现碰巧容忍请求”，用于发现校验缺失、隐式转换、500 异常以及错误资源持久化风险。

### 理论基础

#### JSON 类型与格式是两层约束

JSON 的 number、string、boolean、object、array 和 null 是不同类型。字段契约通常先约束类型，再对类型内部的内容施加格式或业务规则。

| 字段与输入 | JSON 类型 | 结论 |
| --- | --- | --- |
| `totalprice: 200` | number | 类型正确 |
| `totalprice: "200"` | string | 类型错误，即使可以转换成数字 |
| `depositpaid: true` | boolean | 类型正确 |
| `depositpaid: "true"` | string | 类型错误，即使文字含义相似 |
| `checkin: "not-a-date"` | string | 类型正确、日期格式错误 |
| `checkin: 12345` | number | 类型错误，尚未进入格式判断 |
| `checkin: null` | null | 是否允许取决于 nullable 或必填契约，应单独测试 |

因此，类型错误和格式错误不要混成同一个“坏数据”集合。混合后即使测试失败，也难以判断缺失的是 Schema 类型校验还是字段格式校验。

#### 单变量类型错误矩阵

每个负向场景应从完整合法基线出发，一次只替换一个字段：

```text
合法 payload
  → 选择一个字段路径
  → 替换为错误 JSON 类型
  → POST 请求
  → 验证 400 和无资源 ID
  → 若接口错误创建资源，始终清理
```

嵌套字段可以使用元组路径统一表达：

```python
def set_field(payload, field_path, value):
    target = payload
    for key in field_path[:-1]:
        target = target[key]
    target[field_path[-1]] = value


cases = [
    (("totalprice",), "200"),
    (("depositpaid",), "true"),
    (("bookingdates", "checkin"), 12345),
]
```

这套结构把“测试哪个字段、发送什么错误值”和“如何发请求及断言”分开，既支持顶层字段，也支持任意深度的嵌套字段。

#### 预期、观察和假设必须分开

类型负向测试的业务预期是错误请求返回 400 级响应，并且不创建资源。实际实验可能得到不同结果：

- **预期**：三种错误类型均应返回 `400 Bad Request`。
- **观察**：本地接口均返回 200；字符串价格被转换成数字，字符串布尔值被转换成布尔值，数字日期被转换成 `"1970-01-01"`。
- **假设**：数字日期可能经过时间值或时间戳转换，但仅凭响应不能确认具体实现根因。

不能因为实际返回 200 就把测试预期改成 200。也不能把未经源码或日志确认的转换机制写成事实。

#### 错误接受请求时仍要清理

负向请求有可能被接口错误接受并返回动态资源 ID。测试应先安全提取整数 ID，再在 `finally` 中清理，使契约断言失败和环境回收相互独立：

```python
booking_id = None

try:
    response = booking_client.create_booking(invalid_payload)
    booking_id = extract_integer_id(response)
finally:
    if booking_id is not None:
        delete_booking(booking_id)

assert response.status_code == 400
assert booking_id is None
```

使用 `is not None` 比真假判断更精确；只把整数 ID 交给清理函数，可以避免错误响应中的任意字符串被误当作资源标识。

#### 严格 xfail 只应容纳已知缺陷

已确认缺陷可以保留 400 断言，并使用严格 xfail：

```python
pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="接口接受错误类型并返回 200；契约预期为 400。",
)
```

`strict=True` 使接口修复后的正常通过变成 XPASS，从而提醒移除缺陷标记。`raises=AssertionError` 将已知失败限制为契约断言；清理失败使用 `RuntimeError`，不会被当作已知产品缺陷吞掉。若已知行为是 200，还应在断言前拒绝 500 等新状态，否则不同缺陷也可能被宽泛的 xfail 掩盖。

### 适用场景与边界

类型边界测试适用于有明确字段契约的 JSON API，尤其是价格、布尔开关、嵌套对象、数组和标识符字段。它不能代替格式、范围、必填、跨字段业务规则或授权测试；这些约束应各自建立能够准确归因的场景。没有明确规格时，可以记录当前行为和风险建议，但不要擅自把个人偏好写成产品规则。

### 常见错误、反例与假通过

1. 把可转换字符串当作合法数字或布尔值，默认接受服务端隐式转换。
2. 同一个 payload 同时破坏多个字段，导致失败无法归因。
3. 把类型错误、格式错误、null 和缺失字段混在一个参数集合中。
4. 接口实际返回 200 或 500 后，修改期望值迎合实现。
5. 只断言状态码，不检查错误请求是否返回资源 ID 或产生持久化数据。
6. 把清理放在失败断言之后，使异常资源残留在环境中。
7. 使用不受限制的 xfail，把清理异常或新的 500 行为也误记为同一个已知缺陷。
8. 根据一次响应直接断言服务端内部转换机制，没有区分观察事实与根因假设。

### 记忆要点

**先验证 JSON 类型，再验证内容格式；错误类型应被明确拒绝，不能把隐式转换当作契约兼容，契约失败也不能牺牲资源清理。**

### 代码落地

本日新增 `tests/test_invalid_types.py`，使用字段路径参数化覆盖字符串 `totalprice`、字符串 `depositpaid` 和数字 `bookingdates.checkin`。三个场景均保留 400 预期，并以 `strict=True, raises=AssertionError` 的 xfail 记录本地接口返回 200 的已知缺陷。测试还安全提取动态 booking ID，在断言前清理意外资源，并让清理异常或新的状态码真正失败。

### 知识验收

1. 为什么 `200` 和 `"200"` 对 JSON 契约不是相同输入？
2. `"not-a-date"` 与 `12345` 分别属于哪类日期字段错误？
3. 服务端自动把错误类型转成正确类型时，为什么测试仍应失败？
4. 错误请求返回 200 并创建资源时，为什么必须在断言失败后仍能清理？
5. `strict=True`、`raises=AssertionError` 和清理使用 `RuntimeError` 分别保护什么风险？
6. 观察到 `12345` 变成 `1970-01-01` 后，哪些是事实，哪些只能写成假设？

### 关联产出

- 类型错误测试：`test-projects/03-restful-booker-api/tests/test_invalid_types.py`
- 数据工厂：`test-projects/03-restful-booker-api/tests/factories.py`
- 验证命令：`.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_invalid_types.py -q`
- 验证结果：目标测试 `3 xfailed`；API 全量回归 `22 passed, 16 xfailed`
- 验证证据：`artifacts/day-051/verification.md`
- 当天记录：`daily-log/day-051.md`

## 知识主题索引

| 主题 | 首次学习日 | 关联内容 |
| --- | ---: | --- |
| pytest、Playwright、expect 执行链 | Day 1 | 测试组织、浏览器操作、最终状态断言 |
| fixture | Day 1、Day 7 | 页面环境准备、数据准备、作用域与隔离 |
| 状态断言 | Day 2 | checkbox、completed 类、未完成计数 |
| DOM 与业务状态 | Day 3 | 删除后的目标消失、剩余数据和计数 |
| 可见性与集合断言 | Day 4 | 筛选器状态、数量和完整结果集 |
| 等价类与边界值 | Day 5 | 空白、空格、重复、长文本 |
| 断言语义 | Day 5 | textContent 与空白规范化 |
| 参数化 | Day 6 | 多组输入复用同一测试逻辑 |
| 稳定定位 | Day 8 | role、label、text、placeholder 与 CSS 结构作用域 |
| 自动等待与条件等待 | Day 9 | Locator 操作自动等待、`expect` 业务状态等待与固定等待边界 |
| 失败证据 | Day 10 | screenshot、Trace、日志与失败保留策略 |
| 标记与测试套件 | Day 11 | smoke/regression 集合关系、marker 声明与 `-m` 筛选 |
| 测试数据、动作与断言 | Day 12 | helper、fixture 与测试主体的职责边界 |
| 按风险选择回归范围 | Day 13 | smoke/regression 边界、状态联动、失败分层与证据 |
| UI 自动化基础与局限 | Day 14 | 端到端链路、测试层边界、断言语义、flaky 与失败分层 |
| 电商业务流与测试边界 | Day 15 | 登录测试切片、URL/页面断言、fixture、注释与失败分层 |
| 负向场景与错误信息断言 | Day 16 | Authentication 与 Validation、错误提示、成功状态排除与失败分层 |
| 测试账号与风险场景 | Day 17 | 特殊账号业务规则、异常观察、对照证据与 Bug 判断边界 |
| 列表完整性与集合断言 | Day 18 | 数量、成员集合、逐项字段、重复检测与顺序边界 |
| 列表到详情的导航验证 | Day 19 | 导航目的地、商品身份、跨页面字段一致性与返回状态 |
| 页面数据提取与排序验证 | Day 20 | 列表顺序、参数化、Decimal、控件状态与无头 UI 执行 |
| 跨页面状态断言 | Day 21 | 购物车徽标、内容数量、商品身份、独立预期与 Context 隔离 |
| 集合与合计准备 | Day 22 | 多商品数量、名称—价格关联、Decimal 合计与顺序边界 |
| 状态回退与幂等思路 | Day 23 | 移除入口、后置条件、徽标与购物车内容同步、UI/API 边界 |
| 表单验证与字段组合 | Day 24 | 单变量隔离、字段—错误映射、精确提示与未导航断言 |
| 金额与业务计算断言 | Day 25 | Decimal 解析、独立预期、小计税费总价不变量与定位器契约 |
| 关键端到端业务流 | Day 26 | 状态转换检查点、导航与业务证据、订单完成后置条件与 E2E 边界 |
| 登出和会话 | Day 27 | 认证状态转换、直接访问受保护路由、会话失效与访问控制边界 |
| Page Object 职责边界 | Day 28 | 页面操作接口、测试业务断言、可复用动作与分层失败排查 |
| Page Object 商品页 | Day 29 | 重复 locator 抽取、actual/expected 分离、页面数据读取与业务断言边界 |
| 多页面业务流程 | Day 30 | 页面职责边界、跨页面编排、状态转换检查点与万能 helper 风险 |
| 测试数据模型 | Day 31 | 共享事实、场景选择、字段映射、商品目录与数据驱动重构边界 |
| 环境配置 | Day 32 | base_url 优先级、命令行覆盖、URL 校验、fixture 注入与错误分层 |
| 多浏览器 | Day 33 | 兼容性矩阵、smoke 覆盖、浏览器依赖与执行成本取舍 |
| 失败分类与 flaky 分析 | Day 34 | 现象—证据—结论分离、产品/脚本/环境归因、HTML 失败证据与人工分类元数据 |
| 框架可维护性与阶段验收 | Day 35 | 改动局部性、分层职责、最小扩展、意图可见性与完整回归 |
| HTTP 与健康检查 | Day 36 | 状态码、响应体、请求超时、性能阈值、目标配置与失败分类 |
| GET 与集合响应 | Day 37 | HTTP 状态、JSON 列表、元素类型、必需字段与结构失败证据 |
| POST 与 JSON 请求体 | Day 38 | 请求序列化、资源 ID、响应字段一致性、持久化回查边界与清理风险 |
| 创建后查询与动态 ID 关联 | Day 39 | POST 输出驱动 GET、资源可见性、字段一致性和数据链路归因 |
| 查询参数与过滤语义 | Day 40 | params 编码、列表到详情核对、equals/after 比较和数据环境归因 |
| Token 鉴权与凭据管理 | Day 41 | HTTP 与业务认证结果分层、fixture 注入、环境变量和敏感信息脱敏 |
| PUT 完整更新与认证头 | Day 42 | 整体替换、Cookie Token、即时响应、持久化回查、动态 ID 和 403 访问控制 |
| PATCH 部分更新 | Day 43 | 部分 payload、未修改字段保护、认证头、动态 ID 和持久化回查 |
| yield Fixture 生命周期与资源清理 | Day 47 | setup/teardown、`yield`、`try/finally`、动态 ID、幂等清理和失败后回收 |
| 测试数据工厂 | Day 48 | 唯一字段、合法默认值、`overrides`、嵌套字段合并和数据隔离 |
| 参数化边界测试 | Day 49 | 边界分类、参数化 case ID、状态码与业务结果分层、严格 xfail 和动态回查 |
| API 负向测试与缺失字段 | Day 50 | 必填字段矩阵、400/500 预期分离、错误资源清理和严格 xfail 缺陷留证 |
| API 输入类型边界 | Day 51 | JSON 类型与格式分层、单变量错误矩阵、隐式转换风险、安全清理和受限严格 xfail |
| 资源生命周期与清理保证 | Day 44 | 动态资源 ID、DELETE 即时结果、删除后 GET 404、重复删除契约和测试数据隔离 |
| API Client 请求封装边界 | Day 45 | base URL、timeout、公共 headers、通用请求、业务断言分离和敏感信息脱敏 |
| Booking 领域客户端 | Day 46 | 通用 Client 与领域 Client 分层、booking CRUD 方法、原始 Response 和测试断言边界 |

## 每日完结后的知识落盘流程

### 触发条件

只有在学习者明确确认“当天完成”后，才执行知识落盘和当天收尾。未确认时，只检查和指导，不更新学习日志、进度文件或 Git 提交。

### 固定顺序

1. 提取当天知识：从讲解、代码、测试结果和复盘回答中提取真正学到的概念。
2. 写成独立理论：补充定义、解决的问题、心智模型、最小代码骨架、适用边界、常见误区和记忆要点。
3. 写入本文件：在对应 Day 章节中追加或修订内容，不把 daily-log 原文整段复制进来。
4. 做自包含检查：假设几个月后只打开本文件，也能理解知识点；必要的代码示例、术语解释和反例必须直接写在这里。
5. 更新导航：同步目录、知识主题索引和关联产出；关联文件只用于追溯证据，不作为理解知识的前置条件。
6. 做格式检查：确认标题层级、代码围栏、表格、空行和 Markdown 结构一致，并运行 git diff --check。
7. 再完成当天收尾：更新 daily-log/day-XXX.md、progress.json，运行 python tools/validate_repo.py，最后创建本地 Git 提交。

### 落盘前检查清单

- [ ] 能用一句话说明知识点是什么；
- [ ] 能说明它解决什么问题；
- [ ] 有一个不依赖外部文件的心智模型或执行链；
- [ ] 有最小可读的代码或伪代码示例；
- [ ] 写明适用场景和不适用场景；
- [ ] 至少记录一个常见误区或假通过风险；
- [ ] 写明今天的代码如何落实知识；
- [ ] 有知识验收问题和记忆要点；
- [ ] 目录和主题索引已同步；
- [ ] 运行结果和证据路径已在当天日志中记录。

## 落盘文本格式规范

### Day 章节的固定结构

每个学习日尽量使用以下顺序，方便长期复习：

~~~markdown
## Day X：主题

### 核心知识点
用一两句话给出定义和学习目标。

### 它解决的问题
说明没有这个知识时会出现什么测试风险、工程问题或维护成本。

### 理论基础
#### 定义与关键概念
#### 心智模型或执行链
#### 最小代码骨架
#### 断言、数据或状态的含义
#### 适用场景与边界
#### 常见错误、反例与假通过
#### 记忆要点

### 代码落地
说明今天的产出如何具体使用这个知识点。

### 知识验收
给出不看代码也能回答的问题。

### 关联产出
列出目标文件、验证命令和证据路径。
~~~

### 文本写作要求

- 先讲理论，再讲项目中的具体落地；不要只写“今天新增了某个测试”。
- 第一次出现术语时，同时给出中文含义和英文/API 名称，例如“参数化（parameterization）”。
- 每个重要概念至少回答“是什么、为什么、何时使用、何时不要使用”四个问题。
- 代码示例保持最小、完整、可读；示例中的变量名要能表达业务含义。
- 对比多个概念时使用表格；描述执行顺序时使用编号或文本流程图。
- 代码使用 Markdown 代码围栏，并标注语言；普通说明不要伪装成代码。
- 每个断言都说明它证明了什么，以及它不能证明什么。
- 事实、观察结果和假设要分开写；没有产品规格时，不把实验样本写成产品规则。
- 失败经验要记录“现象 → 根因 → 修复或当前假设”，避免只写“已解决”。
- 关联文件放在章节末尾，知识正文必须能够脱离这些文件独立阅读。
- 每个 Day 章节结尾保留一条“记忆要点”，便于很久之后快速恢复上下文。

### 格式检查规则

- 文档只有一个一级标题；每个学习日使用二级标题。
- 理论主题使用三级标题，小节使用四级标题，不跳级。
- 标题前后保留空行，段落之间保留空行。
- 代码块使用成对的代码围栏，围栏内不混入解释性长段落。
- 表格必须有表头和分隔行，列内容保持同一比较维度。
- 不使用无意义的重复段落；如果一个概念在多个 Day 出现，正文解释差异，主题索引负责导航。
- 提交前检查 Markdown 差异和换行，不把临时调试输出写入知识库。

## 后续维护规则

完成新的学习日后，在本文件末尾追加一个 Day 章节，并至少包含：

- 核心知识点；
- 它解决的问题；
- 可复用的原理或代码骨架；
- 当天项目中的具体落地；
- 常见错误或风险；
- 知识验收问题；
- 与目标文件、验证命令和证据的关联。

目录和主题索引也要同步更新。执行记录不要整体复制进本文件，只保留能帮助未来复习的知识和关键经验。
