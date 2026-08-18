import re

import pytest
from playwright.sync_api import Page, expect


# 标准登录是关键用户路径，也属于完整回归范围。
pytestmark = pytest.mark.regression


@pytest.mark.smoke
def test_standard_user_login(
    saucedemo_page: Page,
    standard_user_credentials: dict[str, str],
):
    # 使用 fixture 提供的账号，避免把凭据散落在测试代码中。
    saucedemo_page.get_by_placeholder("Username").fill(
        standard_user_credentials["username"]
    )
    saucedemo_page.get_by_placeholder("Password").fill(
        standard_user_credentials["password"]
    )

    # 本测试只验证登录，不扩展到商品、购物车或结账流程。
    saucedemo_page.get_by_role("button", name="Login").click()

    # URL 证明登录后的路由正确。
    expect(saucedemo_page).to_have_url(
        re.compile(r"/inventory\.html$")
    )

    # 页面标题证明商品页已经真正加载，而不只是 URL 发生了跳转。
    expect(saucedemo_page.locator(".title")).to_have_text("Products")