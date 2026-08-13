# Git 工作流

## 仓库职责

`D:\qa-automation-learning` 是你的学习成果 Git 仓库。它只保存 `test-projects/` 下的测试代码、配置、学习记录、精选证据和文档。

第三方被测项目放在仓库外的 `D:\qa-automation-targets`，每个被测项目保留自己的 `.git`。不要把第三方仓库 clone 到 `test-projects/` 下，也不要把第三方源码复制进当前仓库。

## 1. 连接自己的远程仓库

先在 GitHub、GitLab 或 Gitee 创建一个空仓库，然后执行：

```powershell
cd D:\qa-automation-learning
git remote add origin <你的学习仓库地址>
git remote -v
git push -u origin main
```

如果 `origin` 已经存在，使用：

```powershell
git remote set-url origin <你的学习仓库地址>
git push -u origin main
```

## 2. 准备被测项目

```powershell
New-Item -ItemType Directory -Force D:\qa-automation-targets

git clone https://github.com/tastejs/todomvc.git `
  D:\qa-automation-targets\todomvc

git clone https://github.com/mwinteringham/restful-booker.git `
  D:\qa-automation-targets\restful-booker

git clone https://github.com/swagger-api/swagger-petstore.git `
  D:\qa-automation-targets\swagger-petstore
```

SauceDemo 没有需要 clone 的完整官方 Web 源码，直接使用：

```text
https://www.saucedemo.com/
```

clone 后先检查第三方仓库状态：

```powershell
git -C D:\qa-automation-targets\todomvc status
git -C D:\qa-automation-targets\restful-booker status
git -C D:\qa-automation-targets\swagger-petstore status
```

## 3. 编写、验证和提交自己的测试代码

测试代码放在对应的 `test-projects/` 阶段目录：

```powershell
cd D:\qa-automation-learning
python tools/plan_day.py today
git status
git add .
git commit -m "feat: complete day XXX test practice"
git push
```

提交前确认没有加入 `.env`、真实凭据、依赖目录、缓存、完整生成报告或第三方源码。规则见 [.gitignore](.gitignore)。

## 长期维护原则

- 被测项目通过外部路径和环境变量配置，不在测试代码里写死个人机器路径。
- 第三方项目升级时，在 `qa-automation-targets` 中单独查看其 Git 变更，不修改其源码来迁就测试。
- 每次测试代码变更都记录运行命令、目标环境、结果和证据。
- 性能测试脚本默认只允许指向本地或明确授权的目标。
