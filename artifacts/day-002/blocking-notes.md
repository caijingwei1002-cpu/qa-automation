# Day 2 blocking notes

## Local TodoMVC page was unavailable

- Symptom: `test_complete_todo` failed during fixture setup with `net::ERR_CONNECTION_REFUSED` at `http://127.0.0.1:8080/`.
- Root cause: the local HTTP server for the TodoMVC application was not running. The test did not reach the checkbox interaction.
- Fix: started a Python HTTP server from `D:\qa-automation-targets\todomvc\examples\angular\dist\browser` and kept it running during verification.
- Verification: reran the target pytest node and received `1 passed in 1.91s`.
- Evidence: `pytest-complete-todo.txt` contains the failure and `pytest-complete-todo-retry.txt` contains the successful retry.
