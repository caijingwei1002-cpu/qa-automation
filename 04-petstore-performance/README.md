# Swagger Petstore API 与性能测试

## 被测项目

本地被测源码建议放在：

```text
D:\qa-automation-targets\swagger-petstore
```

来源：[swagger-api/swagger-petstore](https://github.com/swagger-api/swagger-petstore)

先阅读项目 README，启动本地服务并确认 OpenAPI 文档和健康接口可访问，再编写接口或 k6 脚本。本目录只保存自己的测试脚本、配置和分析报告。

## 学习重点

- OpenAPI 契约和字段断言
- API 业务流程关联
- k6 性能冒烟、负载和阈值
- p95、成功率、容量和性能基线

压力、峰值和稳定性测试只对本地或明确授权的服务执行。
