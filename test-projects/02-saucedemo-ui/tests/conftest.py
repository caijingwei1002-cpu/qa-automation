import base64
import logging
import os

import pytest
from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    sync_playwright,
)
from pytest_html import extras as html_extras

from config import resolve_base_url
from test_data import DEFAULT_PASSWORD, STANDARD_USER

logger = logging.getLogger(__name__)

FAILURE_CATEGORY_LABELS = {
    "product": "产品缺陷",
    "script": "脚本缺陷",
    "environment": "环境问题",
}


def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default=None,
        help="覆盖 SauceDemo base URL",
    )
    parser.addoption(
        "--browser",
        action="store",
        choices=("chromium", "firefox"),
        default="chromium",
        help="选择 Playwright 浏览器",
    )
    parser.addoption(
        "--failure-category",
        action="store",
        choices=("product", "script", "environment"),
        default=None,
        help="人工分析后的失败分类",
    )
    parser.addoption(
        "--failure-reason",
        action="store",
        default=None,
        help="支持失败分类的证据与理由",
    )


@pytest.fixture
def saucedemo_base_url(pytestconfig):
    return resolve_base_url(
        pytestconfig.getoption("--base-url")
    )


@pytest.fixture(scope="session")
def browser(pytestconfig):
    # 每个测试会话只启动一个指定类型的浏览器。
    browser_name = pytestconfig.getoption("--browser")

    with sync_playwright() as playwright:
        browser_types = {
            "chromium": playwright.chromium,
            "firefox": playwright.firefox,
        }
        selected_browser = browser_types[browser_name]
        browser = selected_browser.launch(headless=True)

        yield browser

        browser.close()


@pytest.fixture
def context(browser: Browser):
    # 每条测试使用独立 context，避免 Cookie、localStorage 和登录状态互相污染。
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext):
    # 每条测试创建独立页面，测试主体只关注页面上的业务行为。
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def saucedemo_page(
    page: Page,
    saucedemo_base_url: str,
):
    # 统一从配置解析出的地址开始。
    page.goto(saucedemo_base_url)
    page.wait_for_load_state("domcontentloaded")
    yield page


@pytest.fixture
def standard_user_credentials():
    # 优先读取环境变量；默认值是公开训练账号，不把凭据散落在测试步骤中。
    return {
        "username": os.getenv("SAUCEDEMO_USERNAME", STANDARD_USER),
        "password": os.getenv("SAUCEDEMO_PASSWORD", DEFAULT_PASSWORD),
    }


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # 只处理测试主体 call 阶段的失败
    if report.when != "call" or not report.failed:
        return

    # 从当前测试使用的 fixture 中获取 saucedemo_page。
    extras = list(getattr(report, "extras", []))

    page = item.funcargs.get("saucedemo_page")
    if page is not None:
        try:
            screenshot_bytes = page.screenshot(full_page=True)
            screenshot_base64 = base64.b64encode(
                screenshot_bytes
            ).decode("ascii")

            extras.append(
                html_extras.png(
                    screenshot_base64,
                    name="Failure Screenshot",
                )
            )
        except Exception as exc:
            logger.warning(
                "Failed to capture screenshot: %s",
                exc,
            )

    category = item.config.getoption("--failure-category")
    reason = item.config.getoption("--failure-reason")

    if category is not None:
        category_label = FAILURE_CATEGORY_LABELS[category]
        classification = (
            f"分类：{category_label}\n"
            f"理由：{reason or '未提供'}"
        )
        extras.append(
            html_extras.text(
                classification,
                name="Failure Classification",
            )
        )

    report.extras = extras
