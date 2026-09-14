# Day 65 验证证据

日期：2026-09-14
阶段：Restful Booker 收尾与测试代码质量
项目：test-projects/03-restful-booker-api
主题：测试套件与质量检查

## 目标测试

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -m smoke -q
```

结果：

```text
exit_code=0 (passed)
....                                                                     [100%]
4 passed, 104 deselected in 0.19s
```

## 全量回归

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
exit_code=0 (passed)
............................xxxxxx..x.x...........xxxxxxxxxx............ [ 66%]
....................................                                     [100%]
90 passed, 18 xfailed in 1.07s
```

## 静态检查

Ruff 命令：

```text
.\.venv\Scripts\python.exe -m ruff check test-projects/03-restful-booker-api
.\.venv\Scripts\python.exe -m ruff format --check test-projects/03-restful-booker-api
```

结果：

```text
ruff check: All checks passed!
ruff format --check: 29 files already formatted
```

## 关键验证

- 目标测试退出码：`0`。
- 全量回归退出码：`0`。
- Ruff check 和 Ruff format check：通过。
- 测试命令由本运行脚本绑定到仓库虚拟环境。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 测试解释器：`D:\qa-automation-learning\.venv\Scripts\python.exe`。
- 结论：结果已由命令真实执行并写入本文件；如有失败，应先记录根因再完成当天学习。
- 服务预检：target=restful-booker, state=already-running, health=http://127.0.0.1:3001/ping, http=201
