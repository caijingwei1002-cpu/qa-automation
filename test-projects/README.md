# 自动化测试工程

本目录只保存自己编写的自动化测试代码、测试配置、测试数据和项目级测试文档。

被测项目不放在这里。第三方源码统一 clone 到：

```text
D:\qa-automation-targets
```

阶段目录与目标的对应关系：

| 目录 | 目标 |
| --- | --- |
| `01-todomvc-ui` | 本地 TodoMVC |
| `02-saucedemo-ui` | SauceDemo 在线 Demo |
| `03-restful-booker-api` | 本地 Restful Booker |
| `04-petstore-performance` | 本地 Swagger Petstore |

测试代码应通过 `.env` 中的 URL 访问目标，不应依赖目标源码的内部路径。
