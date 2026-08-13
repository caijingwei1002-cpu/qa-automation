# Git 工作流

当前目录 `D:\qa-automation-learning` 是你的学习成果仓库。它与 TodoMVC、Restful Booker、Swagger Petstore 等第三方仓库分开管理。

## 1. 连接你的远程学习仓库

先在 GitHub、GitLab 或 Gitee 创建一个空仓库，然后在当前目录执行。把下面的地址替换成你自己的远程地址：

```powershell
cd D:\qa-automation-learning
git remote add origin <你的学习仓库地址>
git remote -v
git push -u origin main
```

如果之前已经配置过 `origin`，不要重复添加，改用：

```powershell
git remote set-url origin <你的学习仓库地址>
git push -u origin main
```

## 2. Clone 本地被测项目

被测项目建议放在当前仓库外的 `D:\qa-automation-targets`：

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

不要把第三方项目 clone 到当前仓库的四个练习目录中，否则会形成嵌套 Git 仓库或把测试代码与被测源码混在一起。

## 3. 开始编写和提交测试代码

先启动本地被测项目，再在当前仓库对应目录编写测试代码：

```powershell
cd D:\qa-automation-learning
git status
git add .
git commit -m "feat: complete day XXX test practice"
git push
```

每天提交前确认没有加入 `.env`、密钥、密码、依赖目录、缓存或大型生成报告。相关规则已经写入 `.gitignore`。

## 推荐顺序

1. 连接并 push 当前学习仓库。
2. 创建 `D:\qa-automation-targets`，按阶段 clone 被测项目。
3. 确认本地服务或在线目标可以访问。
4. 在 `01-` 到 `04-` 对应目录编写测试脚本。
5. 运行测试、保存必要证据，再提交并 push。
