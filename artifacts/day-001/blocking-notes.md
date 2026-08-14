# Day 1 blocking notes

## Test node was not found

- Symptom: `pytest ...::test_add_todo -q` reported `no tests ran`.
- Root cause: `test_add_todo` was initially a method inside `TestAddTodo`, so its pytest node id was `TestAddTodo::test_add_todo` rather than the module-level node requested by the plan.
- Fix: moved the Day 1 test to module scope and removed the class-only `self` parameter.

## Local page was unavailable

- Symptom: Playwright reported `net::ERR_CONNECTION_REFUSED` for `http://127.0.0.1:8080/`.
- Root cause: the local Python HTTP server was not running when the test started.
- Fix: restarted the server from `D:\qa-automation-targets\todomvc\examples\angular\dist\browser` and kept it running during verification.
