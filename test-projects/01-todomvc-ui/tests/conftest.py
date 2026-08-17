import os

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright


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
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshot_dir = os.path.join(os.path.dirname(__file__), "..", "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"{request.node.name}.png")
        page.screenshot(path=screenshot_path)


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
