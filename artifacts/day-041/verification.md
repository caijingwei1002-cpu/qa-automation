# Day 41 验证证据

日期：2026-08-26
阶段：Restful Booker API
主题：Token 鉴权

## 目标测试

命令：

```powershell
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_auth.py -q
```

结果：

```text
..                                                                       [100%]
2 passed in 0.10s
```

覆盖内容：

- 有效凭据返回 HTTP 200、非空字符串 Token。
- 无效凭据返回 HTTP 200、`reason == "Bad credentials"`。
- 无效凭据响应不包含 Token。
- 测试不打印 Token。

## API 全量回归

命令：

```powershell
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
.........                                                                [100%]
9 passed in 0.44s
```

## 问题与修正

初版在测试收集阶段从 `conftest.py` 导入不存在的常量，并重复定义了同名测试函数。修正为 pytest fixture 注入并删除重复代码后，目标测试和 API 全量回归通过。
