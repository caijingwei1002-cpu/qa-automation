# Day 64 验证证据

日期：2026-09-11
阶段：Restful Booker 收尾与测试代码质量
项目：test-projects/03-restful-booker-api
主题：并行隔离

## 目标测试

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_parallel_isolation.py -q
```

结果：

```text
exit_code=0 (passed)
....                                                                     [100%]
4 passed in 0.14s
```

## 并行验证

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_parallel_isolation.py -q -n 2
```

结果：

```text
exit_code=0 (passed)
bringing up nodes...
....                                                                     [100%]
4 passed in 1.19s
```

并行运行使用两个 xdist worker；两个参数化实例和两类隔离测试均通过。

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
90 passed, 18 xfailed in 1.67s
```

## 关键验证

- 目标测试退出码：`0`。
- 并行目标测试退出码：`0`。
- 全量回归退出码：`0`。
- 测试命令由本运行脚本绑定到仓库虚拟环境。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 测试解释器：`D:\qa-automation-learning\.venv\Scripts\python.exe`。
- 结论：结果已由命令真实执行并写入本文件；如有失败，应先记录根因再完成当天学习。
- 服务预检：target=restful-booker, state=already-running, health=http://127.0.0.1:3001/ping, http=201
