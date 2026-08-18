import os

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
import re
from pathlib import Path
from helpers import add_todo

TODO_MVC_URL = os.getenv("TODO_MVC_URL", "http://127.0.0.1:8080")
# URL 允许通过环境变量切换，默认指向本地 TodoMVC 服务。


@pytest.fixture(scope="session")
def browser():
    # 浏览器进程启动成本较高，因此整个测试会话只启动一次。
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def context(browser: Browser):
    # 每条测试使用独立 context，隔离 Cookie、localStorage 和 Trace。
    context = browser.new_context()
    # Trace 只在测试失败时保留，成功时在后置 fixture 中丢弃。
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True,
    )
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext):
    # 每条测试创建独立页面，避免页面对象在测试之间共享状态。
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def todo_page(page: Page):
    # 所有 Todo 测试从干净的首页开始，统一前置状态。
    page.goto(TODO_MVC_URL)
    page.wait_for_load_state("networkidle")
    yield page


@pytest.fixture(autouse=True)
def _screenshot_on_failure(request, page: Page):
    # 先让测试执行，后置逻辑再根据 pytest 的结果决定是否留证。
    yield

    # pytest_runtest_makereport 会在测试结束后写入 rep_call。
    report = getattr(request.node, "rep_call", None)
    failed = report is not None and report.failed

    # 成功时停止并丢弃 Trace，避免产生大量无用调试文件。
    if not failed:
        page.context.tracing.stop()
        return

    # 失败时保存截图和 Trace，帮助区分定位器、状态和环境问题。
    artifact_dir = (
        Path(__file__).resolve().parents[3] / "artifacts" / "day-010"
    )
    artifact_dir.mkdir(parents=True, exist_ok=True)

    # 测试名可能包含空格、方括号等字符，先转换为安全文件名
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", request.node.name)

    page.screenshot(
        path=str(artifact_dir / f"{safe_name}.png"),
        full_page=True,
    )

    page.context.tracing.stop(
        path=str(artifact_dir / f"{safe_name}.zip")
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 将 setup/call/teardown 阶段的结果挂到测试节点，供失败 fixture 读取。
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture
def todo_page_with_todos(todo_page: Page):
    # fixture 只负责准备公共数据；具体测试仍负责自己的业务断言。
    for todo_text in ["Buy milk", "Learn pytest"]:
        add_todo(todo_page, todo_text)

    yield todo_page
