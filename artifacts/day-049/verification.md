# Day 49 验证证据

日期：2026-08-28
阶段：Restful Booker API
项目：test-projects/03-restful-booker-api
主题：参数化边界

## 目标测试

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_boundaries.py -q
```

结果：

```text
exit_code=0 (passed)
......xxxxxx                                                             [100%]
6 passed, 6 xfailed in 0.45s
```

## 全量回归

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
exit_code=0 (passed)
.........xxxxxx.............                                             [100%]
22 passed, 6 xfailed in 1.82s
```

## 关键验证

- 目标测试退出码：`0`。
- 全量回归退出码：`0`。
- 测试命令由本运行脚本绑定到仓库虚拟环境。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 测试解释器：`D:\qa-automation-learning\.venv\Scripts\python.exe`。
- 结论：结果已由命令真实执行并写入本文件；如有失败，应先记录根因再完成当天学习。
