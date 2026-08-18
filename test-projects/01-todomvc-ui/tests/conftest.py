import os

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
import re
from pathlib import Path


TODO_MVC_URL = os.getenv("TODO_MVC_URL", "http://127.0.0.1:8080")


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def context(browser: Browser):
    context = browser.new_context()
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True,
    )
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext):
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def todo_page(page: Page):
    page.goto(TODO_MVC_URL)
    page.wait_for_load_state("networkidle")
    yield page


@pytest.fixture(autouse=True)
def _screenshot_on_failure(request, page: Page):
    # 先让测试执行
    yield

    # pytest_runtest_makereport 会在测试结束后写入 rep_call
    report = getattr(request.node, "rep_call", None)
    failed = report is not None and report.failed

    # 成功时停止并丢弃 Trace
    if not failed:
        page.context.tracing.stop()
        return

    # 失败时保存截图和 Trace
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
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture
def todo_page_with_todos(todo_page: Page):
    todo_input = todo_page.get_by_placeholder("What needs to be done?")

    for todo_text in ["Buy milk", "Learn pytest"]:
        todo_input.fill(todo_text)
        todo_input.press("Enter")

    yield todo_page
