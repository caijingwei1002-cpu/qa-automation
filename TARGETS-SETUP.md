# 被测项目准备

本文件定义被测项目的来源、外部路径和测试边界。被测项目源码不属于 `D:\qa-automation-learning`，不会上传到你的学习仓库。

## 目标目录

```text
D:\qa-automation-learning       # 你的 Git 仓库：测试资产
D:\qa-automation-targets        # 外部目录：被测项目 clone
```

以下命令仅在进入对应项目、完成资源核对并获得学习者同意后按需执行，已有源码不重复下载：

```powershell
New-Item -ItemType Directory -Force D:\qa-automation-targets

git clone https://github.com/tastejs/todomvc.git `
  D:\qa-automation-targets\todomvc

git clone https://github.com/mwinteringham/restful-booker.git `
  D:\qa-automation-targets\restful-booker

git clone https://github.com/mwinteringham/restful-booker-platform.git `
  D:\qa-automation-targets\restful-booker-platform
```

如果目标目录已经存在，先检查状态，不要直接覆盖本地修改：

```powershell
git -C D:\qa-automation-targets\todomvc status
git -C D:\qa-automation-targets\restful-booker status
git -C D:\qa-automation-targets\restful-booker-platform status
```

## 目标登记

机器可读登记见 [config/targets.json](config/targets.json)。本地 URL 和端口通过 `.env` 提供，模板见 [.env.example](.env.example)。测试代码只读取目标 URL，不依赖第三方源码的绝对路径。

| 测试资产 | 被测目标 | 类型 | 边界 |
| --- | --- | --- | --- |
| `test-projects/01-todomvc-ui` | `D:\qa-automation-targets\todomvc` | 本地 Web | 本地轻量 UI 测试 |
| `test-projects/02-saucedemo-ui` | `https://www.saucedemo.com/` | 在线 Web Demo | 只做功能验证，不做压力测试 |
| `test-projects/03-restful-booker-api` | `D:\qa-automation-targets\restful-booker` | 本地 API | 按其 README 用 npm 或 Docker 启动 |
| `test-projects/04-booker-platform` | `D:\qa-automation-targets\restful-booker-platform` | 本地多服务 | 先确认版本、服务身份与当前课程允许的测试范围 |

Petstore 等后续项目处于待勘察阶段，仅登记在 [路线图](config/project-roadmap.json)。
完成勘察并细化课程后再创建测试资产、加入运行目标登记和配置环境变量。

启动命令以各被测项目当前版本的 README 和配置为准。不要假设第三方仓库的端口永远不变；启动后把实际地址写入 `.env`，不要修改 `config/targets.json` 来保存个人机器状态。

## 安全边界

- SauceDemo 只做正常功能验证，不做压力、峰值或高并发测试。
- 性能、压力、峰值、稳定性和容量测试只对本地或明确授权的服务执行。
- 不提交第三方源码、`.git` 目录、真实账号、Token、密码或本地密钥。
- 被测项目的版本、启动方式和端口变化应记录在学习日志或测试报告中。

tools/run_day_verification.py 会读取目标登记中的 startup 配置执行服务预检。当前 Restful Booker 使用 npm start、/ping 健康端点和最多 30 秒的启动等待；目标已运行时不会重复启动，也不会终止已有进程。若通过环境变量把 URL 指向远程或非本地地址，预检会自动跳过；需要完全手动启动服务时，在命令后加 --skip-service。
