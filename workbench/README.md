# QA Learning Workbench

这是 `qa-automation-learning` 的本地学习工作台。页面展示当天目标、统一七步学习流程、代码上下文、测试证据和课程进度；PyCharm 继续作为完整 IDE。

## 启动

在 PowerShell 中执行：

```powershell
cd D:\qa-automation-learning
.\workbench\start_workbench.ps1
```

默认地址是 <http://127.0.0.1:8765>，且只监听本机。首次使用时，页面会启动 `codex app-server` 并检查 ChatGPT 登录状态；如果尚未登录，按页面提示完成一次登录即可。

如果 Codex CLI 不在 PATH 中，可以明确传入路径：

```powershell
.\workbench\start_workbench.ps1 -CodexExe "C:\path\to\codex.exe"
```

也可以先设置 `$env:CODEX_EXE`，或直接启动服务：

```powershell
.\.venv\Scripts\python.exe .\workbench\server.py --open --codex-exe "C:\path\to\codex.exe"
```

## 学习会话

- 每个学习日对应一个持久化的 Codex thread，刷新页面后可以继续当天会话。
- 步骤从 `config/learning-workflow.json` 读取；完成状态从 `daily-log/day-NNN.session.json` 读取。刷新后恢复首个未完成步骤；点击导航只选择讨论主题，不会把前面的步骤标成完成。
- Codex 的文字回复、计划、工具调用、命令输出和审批请求会持续更新到页面。
- 文件修改和命令执行仍由 Codex App Server 发起审批，页面只在你明确允许后回传决定。
- App Server 状态只保存在 `artifacts/workbench-state.json`，工作台不会自行修改课程进度文件。

## 代码与测试

- 代码工作区浏览当前项目文件，并支持编辑、版本冲突保护和 Git Diff。
- “在 PyCharm 中继续”会打开同一份本地项目文件，不复制代码。
- “直接运行当天测试”调用与命令行相同的验证入口，执行服务预检、目标与回归，保存 `verification.md`、`run-record.json` 和每次运行快照。
- 工作台不提供任意 Shell 接口，也不会直接改写 `progress.json`、`curriculum.json` 或 `daily-plan.json`。

## 故障排查

先在普通 PowerShell 中确认：

```powershell
codex app-server --help
```

如果工作台提示找不到或无法启动 Codex，请使用 `-CodexExe` 指定可执行文件。PyCharm 同样可以通过 `$env:PYCHARM_EXE` 指定。

## 测试

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m unittest discover -s .\workbench\tests -v
node --check .\workbench\static\app.js
```
