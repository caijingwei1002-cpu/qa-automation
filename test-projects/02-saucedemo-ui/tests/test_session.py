import re

import pytest
from playwright.sync_api import Page, expect


pytestmark = pytest.mark.regression

LOGIN_URL = re.compile(r"/\/?$")
INVENTORY_URL = re.compile(r"/inventory\.html$")


def login_as_standard_user(
    page: Page,
    credentials: dict[str, str],
):
    """完成标准用户登录并确认进入受保护的商品页。"""
    page.get_by_placeholder("Username").fill(credentials["username"])
    page.get_by_placeholder("Password").fill(credentials["password"])
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(INVENTORY_URL)
    expect(page.locator(".title")).to_have_text("Products")


def test_logout_returns_to_login_page(
    saucedemo_page: Page,
    standard_user_credentials: dict[str, str],
):
    page = saucedemo_page
    login_as_standard_user(page, standard_user_credentials)

    page.get_by_role("button", name="Open Menu").click()
    page.get_by_role("link", name="Logout").click()

    expect(page).to_have_url(LOGIN_URL)
    expect(page.get_by_placeholder("Username")).to_be_visible()
    expect(page.get_by_placeholder("Password")).to_be_visible()
    expect(page.get_by_role("button", name="Login")).to_be_visible()

    # 直接访问受保护路由，验证会话已经失效而不是只完成了页面跳转。
    protected_inventory_url = page.url.rstrip("/") + "/inventory.html"
    page.goto(protected_inventory_url)

    expect(page).to_have_url(LOGIN_URL)
    expect(page.get_by_placeholder("Username")).to_be_visible()
    expect(page.get_by_placeholder("Password")).to_be_visible()
