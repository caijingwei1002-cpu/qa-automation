# Skill、MCP 和插件设计

## 已加入的本地插件

项目内 `.agents/plugins/qa-learning-coach` 提供一个本地插件清单和一个可复用 Skill：`qa-learning-daily`。

这个 Skill 的职责不是替你完成学习，而是让每天的任务保持在合适难度：

- 读取当前阶段、项目和已完成记录；
- 生成当天唯一的最小任务；
- 要求一个可运行脚本和测试证据；
- 在失败时优先定位根因，不用重试掩盖问题；
- 根据结果安排下一天的递进任务；
- 每 7 天做一次阶段复盘，每 28 天生成一次专项建议。

## MCP 设计

插件里包含一个本地 MCP Server 配置，提供四个工具：

- `get_today_plan`：读取当天学习任务；
- `get_progress`：读取完成天数和下一阶段；
- `create_daily_log`：生成当天的记录文件和证据目录；
- `complete_learning_day`：保存结果、复盘和下一步。

MCP 只访问当前本地学习仓库，不连接外部账号，也不会替你对公共网站发起压力测试。需要云端同步时，再按需接入 GitHub、Notion 或 Linear。

## 推荐的可选外部插件

这些不是每日学习的硬依赖，按需要增加：

| 插件 | 用途 |
| --- | --- |
| GitHub | 保存每日提交、Issue、缺陷和 CI 结果 |
| Notion | 把学习记录同步为知识库和周报 |
| Linear | 把阶段任务和缺陷转成可追踪工作项 |
| Sentry | 练习错误监控和线上问题定位 |
| PostHog | 练习用户行为分析与测试数据设计 |

建议先用本地文件坚持两周，再接入一个远程系统。远程工具越多不代表学习效果越好，重点是每天真正产生脚本、证据和复盘。

## 可一起使用的内置能力

- `browser:control-in-app-browser`：检查本地 UI、辅助定位元素和验证页面状态；
- `github:github` / `github:gh-fix-ci`：阅读仓库、Issue 和 CI 失败；
- `visualize:visualize`：把性能结果、容量曲线和测试流程做成可视化；
- `openai-docs`：只有在学习 Codex/OpenAI API 或插件机制时才使用。

## 每日调用方式

进入 `D:\qa-automation-learning` 后，可以直接对 Codex 说：

```text
使用 $qa-learning-daily，读取我的当前进度，给我今天 90 分钟内能完成的任务。
```

完成后说：

```text
使用 $qa-learning-daily，记录我今天完成的脚本、运行结果、问题和明天第一步。
```

如果不使用 MCP，也可以直接运行：

```powershell
python tools/plan_day.py today
python tools/plan_day.py complete 1 --result "完成新增 Todo 脚本并通过" --next-step "增加完成状态场景"
```
