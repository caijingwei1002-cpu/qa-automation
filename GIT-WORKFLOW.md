# Git 工作流

## 首次绑定远程仓库

先在 GitHub、GitLab 或 Gitee 创建一个空仓库，然后在本目录执行：

```powershell
git remote add origin <远程仓库地址>
git push -u origin main
```

之后每天保存学习成果：

```powershell
git status
git add .
git commit -m "feat: 完成第 XXX 天测试练习"
git push
```

提交前确认不要把 `.env`、密钥、密码、报告缓存或依赖目录提交进去；这些内容已经在 `.gitignore` 中排除。

## 被测项目需要从 Git 获取时

如果测试脚本要测试另一个 Git 项目，先 clone 被测项目，再编写或运行测试脚本。建议把两个仓库并列放置：

```powershell
cd D:\
git clone <被测项目地址> app-under-test
cd D:\qa-automation-learning
```

也可以把被测项目放在当前仓库的 `targets/` 目录中；该目录已被忽略，不会把被测项目的文件或它自己的 `.git` 纳入本仓库。不要把另一个仓库直接复制到当前仓库已跟踪的四个练习目录中，除非你明确要把它们合并成一个仓库。

推荐顺序：

1. clone 或准备被测项目，确认它能启动。
2. 在本仓库对应的练习目录编写测试代码。
3. 在本地运行测试并保存必要证据。
4. 提交并 push 测试代码与学习记录。
