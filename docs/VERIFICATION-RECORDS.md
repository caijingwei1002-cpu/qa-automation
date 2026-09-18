# 运行记录与来源

优先使用 `python tools/run_day_verification.py N`。命令行、工作台和 MCP 都经过此模块，默认每条命令最多等待 300 秒。
验证记录与步骤记录分别保存：测试运行不会自动把学习步骤标成完成。

## 自动执行

`artifacts/day-NNN/run-record.json` 指向最新运行内容；`runs/<run-id>/result.json` 保留每次快照。
`verification.md` 用于阅读与根因说明。每次执行替换机器摘要，保留人工分析；人工结论应随新结果复核。
记录包含 source、day、test_project、run_id、finished_at、project_fingerprint，以及 target/regression 的 planned_command、实际 command、exit_code、output。
代码指纹覆盖执行项目的测试代码和配置；不证明远端服务版本、环境变量或产品状态未变，环境结论仍需人工记录。

## 学习者提供结果

教练先核对学习者粘贴的实际命令、输出及对应代码，再整理 JSON，不要求学习者操作 JSON。
复制已有 run-record 的结构时，必须逐项替换为本次事实；没有自动记录可参考下面结构（示例不可直接作为完成证据）：

```json
{
  "day": 67,
  "test_project": "test-projects/03-restful-booker-api",
  "finished_at": "实际执行时间，含时区",
  "provenance": "学习者在何次对话提供的哪段 PowerShell 输出",
  "project_fingerprint": "确认代码一致后获取的 SHA256",
  "target": {
    "planned_command": "与当前计划 run 完全一致",
    "command": "学习者实际执行的完整命令",
    "exit_code": 0,
    "output": "真实输出"
  },
  "regression": {
    "planned_command": "与当前计划 full_run 完全一致",
    "command": "学习者实际执行的完整命令",
    "exit_code": 0,
    "output": "真实输出"
  }
}
```

可在仓库根目录读取代码指纹：

```powershell
python -c "from pathlib import Path; from tools.learning_workflow import project_fingerprint; print(project_fingerprint(Path.cwd(), 'test-projects/03-restful-booker-api'))"
python tools/run_day_verification.py 67 --import-result artifacts/day-067/learner-result.json
```

导入不会运行测试，来源强制设为 learner，并生成新的运行编号。缺少来源、时间、正确命令或代码指纹时拒绝导入。
无明确退出码时由真实 pytest 汇总和终端信息核实，不能把未知结果写成通过。

## 验收

验证 checkpoint 会绑定当前 run_id。新的运行或测试代码变更会使旧验收不能用于完成当前课。
普通测试失败（退出码 1）必须有根因分析并选择 known_failure 才能继续验收；服务启动失败、超时、中断等情况需继续处理。
程序检查证据结构与一致性，不能证明文字是学习者独立作答；教练仍须依据实际对话判断。
