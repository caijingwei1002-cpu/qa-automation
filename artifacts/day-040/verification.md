# Day 40 验证证据：过滤查询

## 目标测试

验证命令：

```powershell
python -m pytest test-projects\03-restful-booker-api\tests\test_filters.py -q
```

实际结果：

```text
3 passed in 0.28s
```

覆盖范围：

- `firstname=Jim` 等值过滤；
- `lastname=Brown` 等值过滤；
- `checkin=2015-01-01` 日期边界过滤；
- 每条列表结果都通过动态 `bookingid` 查询详情；
- 详情字段分别按 `equals` 或 `after` 规则验证。

## API 项目回归

验证命令：

```powershell
python -m pytest test-projects\03-restful-booker-api\tests -q
```

实际结果：

```text
7 passed in 0.28s
```

## 失败分析与修正

首次日期用例使用 `checkin=2026-08-25`，实际请求返回 `200` 和空列表：

```text
Expected at least one booking for params={'checkin': '2026-08-25'}
```

证据表明请求和 HTTP 层正常，但当前环境没有满足该日期条件的稳定数据；不能直接归因于产品过滤缺陷。随后检查详情时，PowerShell 默认 `Accept` 头导致本地服务返回 `418`；显式设置 `Accept: application/json` 后，booking 详情可正常读取。

修正方案：使用已有数据可覆盖的 `checkin=2015-01-01` 作为边界，并按本地接口语义验证详情日期晚于边界；姓名仍按精确相等验证。修正后目标和全量回归均通过。

## 归因边界

- URL 或 `params` 错误：脚本问题；
- 日期不存在、共享数据被改变或手工请求头不兼容：环境/测试数据问题；
- 请求参数正确、已确认有符合条件的数据，但接口仍返回不满足条件的 booking：才有充分证据进一步怀疑产品过滤逻辑。
