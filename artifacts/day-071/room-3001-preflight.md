# Day 71：Room 默认 3001 只读 preflight

## 目标

在不结束进程、不修改端口、不修改代码、不启动服务、不发送状态变更请求的前提下，确认 `3001` 当前监听者的身份，并判断 Platform Room 默认端口基线是否具备恢复条件。

## 只读检查设计

| 检查 | 证据 | 结论标准 |
|---|---|---|
| 端口监听 | `3001` 的监听 PID | 能把端口映射到具体进程 |
| 进程身份 | 进程名、可执行路径、命令行、工作目录 | 判断 Node/Java 及所属项目 |
| 启动来源 | 父进程及父进程命令行 | 判断是否来自其他项目或任务 |
| Platform 版本 | 外部源码仓库路径、模块、commit、配置 | 确认目标版本为 `d36bd3f`，默认端口为 `3001` |
| HTTP 行为 | health 与基础 GET | 仅在目标 Room 已运行时判断服务身份；不发送 POST/PUT/DELETE |

## 安全边界

- 本轮不执行 `Stop-Process`、`taskkill` 或任何终止动作。
- 本轮不修改 Node/Room 端口、源码、配置或启动脚本。
- 本轮不启动或重启服务。
- 本轮只读取进程和仓库信息，并对现有服务发送只读 GET 请求。
- 若无法确认停止或迁移安全性，结论停在“环境前置阻塞”，不进入缺陷复现。

## 检查结果

### 端口与进程

只读端口检查记录到：

```text
TCP  0.0.0.0:3001  0.0.0.0:0  LISTENING  29528
TCP  [::]:3001     [::]:0     LISTENING  29528
```

PID `29528` 的进程信息为：

```text
ProcessId         : 29528
Name              : node.exe
ExecutablePath    : C:\Users\htuser\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.19.0-win-x64\node.exe
CommandLine       : node ./bin/www
ParentProcessId   : 19668
ParentName        : node.exe
ParentCommandLine : "node" "D:\qa-automation-targets\restful-booker\node_modules\.bin\\..\cross-env\dist\bin\cross-env.js" SEED=true node ./bin/www
```

这组证据表明 `3001` 当前属于另一个 Node 项目 `D:\qa-automation-targets\restful-booker`，不是 Platform Room 的 Java/Spring Boot 进程。本轮未结束该进程。

### Platform 版本与配置

目标 Platform 源码目录为 `D:\qa-automation-targets\restful-booker-platform`，只读 Git 检查结果为：

```text
commit d36bd3f8647a
server.port = 3001
server.servlet.context-path=/room
```

工作区状态检查没有输出未提交修改；Room 默认配置仍为 `3001` 和 `/room`。

### 只读 HTTP 行为

对现有 `3001` 发送的两个 GET 请求均返回 Express 行为，而不是 Platform Room 行为：

```text
GET /room/actuator/health → HTTP/1.1 404 Not Found
X-Powered-By: Express
Content-Type: text/plain; charset=utf-8
Body: Not Found

GET /room/ → HTTP/1.1 404 Not Found
X-Powered-By: Express
Content-Type: text/plain; charset=utf-8
Body: Not Found
```

### 结论

已确认 `3001` 当前由其他项目的 Node/Express 进程占用，不属于 `restful-booker-platform` 的 Room 服务。Platform Room 默认 `3001` 基线尚未恢复；由于本轮未确认停止或迁移该进程的安全授权，流程停在环境前置阻塞，不进入 Room 业务行为或 DELETE→GET `500` 缺陷复现。

本轮只读检查未结束进程、未修改端口、未修改代码或配置、未启动服务、未发送 POST/PUT/DELETE 请求。
