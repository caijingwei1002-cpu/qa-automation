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
