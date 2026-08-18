import os

import pytest
from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    sync_playwright,
)


SAUCEDEMO_URL = os.getenv(
    "SAUCEDEMO_URL",
    "https://www.saucedemo.com/",
)


@pytest.fixture(scope="session")
def browser():
    # 浏览器启动成本较高，整个测试会话只创建一个实例。
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
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
def saucedemo_page(page: Page):
    # 统一从登录页开始，保证登录测试的前置状态一致。
    page.goto(SAUCEDEMO_URL)
    page.wait_for_load_state("domcontentloaded")
    yield page


@pytest.fixture
def standard_user_credentials():
    # 优先读取环境变量；默认值是公开训练账号，不把凭据散落在测试步骤中。
    return {
        "username": os.getenv("SAUCEDEMO_USERNAME", "standard_user"),
        "password": os.getenv("SAUCEDEMO_PASSWORD", "secret_sauce"),
    }
