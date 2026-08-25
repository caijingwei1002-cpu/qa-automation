# Day 36 验证证据：HTTP 与健康检查

## 最终验证

验证命令：

```powershell
python -m pytest test-projects\03-restful-booker-api\tests -q
```

实际结果：

```text
1 passed in 0.08s
```

本地被测服务通过 `npm start` 启动，健康接口探测结果为：

```text
201 Created
```

最终测试同时验证：

- 状态码为 `201`；
- 响应体为 `Created`；
- 响应耗时不超过 `1.0s`；
- 请求客户端超时设置为 `3.0s`。

## 失败分析记录

| 现象 | 客观证据 | 分类结论 | 根因或修复 |
| --- | --- | --- | --- |
| 从 SauceDemo 子目录执行时找不到文件 | `no tests ran` / `file or directory not found` | 执行配置问题 | 回到仓库根目录并使用正确路径 |
| 测试收集阶段导入失败 | `ModuleNotFoundError: No module named 'requests'` | 环境/依赖问题 | 为 API 项目声明并安装 `pytest`、`requests` |
| 公共地址耗时超出 1 秒 | 连续 5 次为 `1.817s`、`1.616s`、`1.638s`、`1.402s`、`1.567s` | 测量环境不匹配，不能直接判产品缺陷 | 公共网络不适合作为本地 1 秒性能门槛，切换到本地目标 |
| 本地服务仍然耗时超限 | 测试文件同时存在环境变量解析和第二次 Heroku 硬编码赋值 | 脚本缺陷 | 删除重复硬编码赋值，保留 `RESTFUL_BOOKER_URL` 解析 |

## 结论

状态码和响应体证明本地 `/ping` 功能契约正确；最终本地运行满足性能阈值。失败现象没有被直接当作产品缺陷，而是结合路径、依赖、目标地址和耗时证据逐层分类。
