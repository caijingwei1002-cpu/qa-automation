# 被测项目准备

本文件只记录被测项目的来源和本地路径。被测项目源码不属于当前学习仓库。

## 目录约定

```text
D:\qa-automation-learning        # 当前 Git 仓库
D:\qa-automation-targets         # 第三方被测项目
```

在 PowerShell 中创建目标目录并 clone：

```powershell
New-Item -ItemType Directory -Force D:\qa-automation-targets

git clone https://github.com/tastejs/todomvc.git `
  D:\qa-automation-targets\todomvc

git clone https://github.com/mwinteringham/restful-booker.git `
  D:\qa-automation-targets\restful-booker

git clone https://github.com/swagger-api/swagger-petstore.git `
  D:\qa-automation-targets\swagger-petstore
```

如果目录已经存在，先查看状态，不要直接覆盖本地修改：

```powershell
git -C D:\qa-automation-targets\todomvc status
git -C D:\qa-automation-targets\restful-booker status
git -C D:\qa-automation-targets\swagger-petstore status
```

## 四个学习阶段的目标

| 学习目录 | 被测目标 | 使用方式 |
| --- | --- | --- |
| `01-todomvc-ui` | `D:\qa-automation-targets\todomvc` | 启动 TodoMVC 本地页面，编写 UI 自动化 |
| `02-saucedemo-ui` | `https://www.saucedemo.com/` | 直接做轻量 UI 功能测试，不做压力测试 |
| `03-restful-booker-api` | `D:\qa-automation-targets\restful-booker` | 按项目 README 用 npm 或 Docker 启动本地 API |
| `04-petstore-performance` | `D:\qa-automation-targets\swagger-petstore` | 本地启动 API，做接口、契约和授权环境下的性能测试 |

启动命令以各被测项目自己的 README 和当前版本配置为准。测试代码中不要写死本机路径；后续可以通过环境变量配置目标地址，例如 `TODO_MVC_URL`、`RESTFUL_BOOKER_URL` 和 `PETSTORE_URL`。

## 安全边界

- SauceDemo 只做正常功能验证，不做压力或高并发测试。
- 性能、压力、峰值和稳定性测试只对本地或明确授权的环境执行。
- 第三方源码保留在 `D:\qa-automation-targets`，不要复制到当前仓库的练习目录。
