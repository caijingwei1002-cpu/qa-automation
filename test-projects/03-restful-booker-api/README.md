# Restful Booker 自动化测试工程

被测项目：`D:\qa-automation-targets\restful-booker`

来源：[mwinteringham/restful-booker](https://github.com/mwinteringham/restful-booker)

本目录只保存 API 测试代码、客户端封装、Schema、测试数据、报告和工程化配置。按被测项目当前 README 使用 npm 或 Docker 启动本地 API，通过 `RESTFUL_BOOKER_URL` 配置地址。

学习重点：健康检查、CRUD、Token、接口关联、负向场景、Schema、数据隔离、清理、并行和 CI。

## Day 69 验收对象与边界

本次验收对象为本目录对应的 API 自动化测试项目，被测服务为 `mwinteringham/restful-booker`。被测 API 按其 README 使用 npm 或 Docker 在本地独立启动；测试项目仅通过 `RESTFUL_BOOKER_URL` 指向目标服务，不负责被测服务本身的启动、实现或修改。

本阶段验收范围包括健康检查、CRUD、Token 鉴权、接口关联、负向场景、Schema 校验、测试数据隔离、资源清理、并行执行及 CI 等 API 自动化能力。验收结论仅针对当前代码版本、当前测试范围和本次实际执行环境。

## Day 69 变更归属与证据范围

Day 69 本次新增内容仅为本文件中的 API 阶段验收说明，不应将当前工作区内其他既有改动归入本次产出。后续 Ruff、pytest、并行执行等验证结果反映的是当前 `03-restful-booker-api` 项目代码在本次环境下的整体状态；除本文件外的测试代码、客户端封装、Schema、测试数据及工程化配置均可能来自此前已有实现，因此这些通过结果只能作为当前项目状态的验收证据，不能证明它们由 Day 69 新增或修改。本次验收结论仅适用于已实际执行的命令、已覆盖的测试范围、当前被测服务版本及当前环境，不能扩展为整个仓库无问题、所有未执行场景均正确，或所有工作区既有改动均已完成审查。
