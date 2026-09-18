# Day 76 验证矩阵：服务身份闸门与只读基线决策

## 产物归属

- 核心矩阵、测试边界、停止条件和不变量：学习者提交。
- 文档目录化与 Markdown 落盘：教练协助。
- 本产物不启动服务、不停止外部进程、不修改产品代码或环境，不执行业务状态变更。

Day 76 的验证矩阵分成两条互不替代的证据链：默认路径负责确认真实环境前置，隔离路径负责验证不依赖真实服务的逻辑。

## 默认路径：真实环境前置

| 用例 | 测试层 | 输入/数据 | 主要断言 | 证据字段 | 停止条件 | 不变量 |
| --- | --- | --- | --- | --- | --- | --- |
| D1 resolved target | 配置/runtime resolution | 默认配置、环境变量、override 状态 | 区分 default、override 和 resolved value；确认最终目标 | `default_target`、`override_value`、`resolved_target`、配置来源 | 无法确定 resolved target，或实际不是 `3001` 时，不把后续证据归到默认 `3001` | 不修改环境变量、配置或启动参数 |
| D2 监听检查 | OS/网络前置 | resolved host:port，例如 `localhost:3001` | 端口是否监听；监听与身份严格分开 | `host`、`port`、`listen_state`、只读可得的 PID | 未监听则停在环境前置；不因此启动服务 | 不 kill、不 restart、不 bind/抢占端口 |
| D3 进程身份 | 进程/服务身份 | PID、命令行、工作目录、启动特征等只读信息 | 能否证明监听进程是预期 Room 服务 | `pid`、`process_name`、`command_line`、`cwd`、`service_identity_result`、`identity_basis` | 身份不符或证据不足，立即停止真实 Room 契约判断 | 不停止、修改或重启进程 |
| D4 只读 health/GET | HTTP 只读探测 | 已确认 target 上允许的 health 或 GET endpoint | 记录实际 `status/body/headers`，不因 `200` 自动判为 Room 正常 | `method`、`url/path`、`status`、安全 body 摘要、非敏感 headers、request id | 身份未确认时，即使 GET 为 `200` 也停在身份层；需要状态变更则不执行 | 只允许 GET/HEAD/health；不 POST/PUT/PATCH/DELETE |

默认路径顺序：

```text
default / override
        ↓
resolved target
        ↓
3001 是否监听
        ↓
监听进程是谁
        ↓
是否能证明是 Room
        ↓
只读 health / GET
        ↓
只有前置成立后，才讨论 Room API
```

核心停止规则：

```text
监听存在 ≠ Room 身份成立
GET 200 ≠ Room 契约通过
```

当前若为 `3001 listening` 且 `service identity = mismatch`，默认路径在身份层停止。后续 GET 即使执行，也只能作为外部 Express 服务的观察结果，不能升级为 Room 缺陷回归证据。

## 隔离路径：不依赖真实服务

| 用例 | 测试层 | 输入/数据 | 主要断言 | 证据字段 | 停止条件 | 不变量 |
| --- | --- | --- | --- | --- | --- | --- |
| I1 配置解析 | 单元测试/配置层 | default、合法 override、非法 override、空值 | `default → override → resolved target` 符合规则；非法配置得到预期错误 | `input_config`、`resolved_target`、`error_type`、错误分类 | 规则不确定时停在配置层，不推断网络/服务问题 | 不访问网络，不修改真实环境配置 |
| I2 服务身份判定 | 纯函数或 Mock 单测 | 模拟进程信息、health body、server header、service marker | Room 特征为 match；其他 Express 为 mismatch；证据不足为 unknown 而非 match | `observed_identity_fields`、`expected_identity`、`identity_result`、`reason` | `mismatch` 或 `unknown` 时不得进入 Room 契约判断 | 不连接真实服务，不把端口可达当身份成立 |
| I3 BFF Mock | BFF route + Mock HTTP client | Mock 200/404/500、ConnectionError、Timeout | BFF 映射、`status/body/headers`、诊断分类和脱敏符合预期 | `bff_status`、`downstream_status`、`exception_category`、route、operation、trace/request id | 只停在 BFF 行为结论，不升级为真实 Room 结果 | 不启动 Room、不访问真实下游、不改业务状态 |
| I4 静态规则 | 静态审查/源码层 | BFF route、配置代码、异常处理、日志调用 | 确认 resolved target、catch-all、下游状态/异常区分和敏感信息风险 | 配置来源、调用路径、异常分支、日志字段、header/body 处理规则 | 静态代码不能证明 runtime 事实时标为设计证据 | 不修改产品代码、不启动服务、不执行请求 |

隔离路径的有效结论可以是“BFF Mock 行为通过”或“身份判定能将非 Room Express 服务识别为 mismatch”，不能是“真实 Room 服务正常”。

## 统一证据字段

```text
evidence_layer
target_source
resolved_target

listen_state
pid / process_identity
service_identity
identity_basis

http_method
request_path
observed_status

bff_status
downstream_status
exception_category

request_id / trace_id

result_classification
stop_reason
```

`result_classification` 使用分层结论，避免模糊的 `PASS/FAIL`：

```text
config_verified
listener_present
service_identity_mismatch
bff_mapping_verified
room_contract_not_reached
```

## Day 76 总不变量

> 只增加证据，不改变环境；一旦服务身份、认证或目标层前置未成立，就停在该层，不把下游未验证事实升级为 Room 契约结论。

## 当前决策

历史检查曾观察到 `3001` 由身份不符的外部 Express 服务占用；本次当前快照为无监听，因此当前服务身份不可判定。BFF Mock 通过不能补足真实 Room 身份。未获得明确授权时，保留环境不变，默认路径停在环境前置，继续隔离 Mock、配置/源码静态审查和其他只读证据收集。

当前结论边界：

```text
resolved_target = :3001
current_listener = absent
current_service_identity = not_established
historical_identity_evidence = mismatch (historical only)
pytest = not_verified if unavailable
ruff = not_verified if unavailable

classification = real_environment_precondition_not_met
room_product_conclusion = NOT_REACHED / NOT_VERIFIED
```

“当前无监听”不等于“Room 服务挂了”；历史身份不符不等于当前仍是错误 Express；pytest/ruff 不可用不等于测试或 Room 产品失败。
