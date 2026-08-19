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


def test_wrong_password_shows_error(
    saucedemo_page: Page,
    standard_user_credentials: dict[str, str],
):
    # 使用有效用户名配合错误密码，专门验证认证失败反馈。
    saucedemo_page.get_by_placeholder("Username").fill(
        standard_user_credentials["username"]
    )
    saucedemo_page.get_by_placeholder("Password").fill("wrong_password")

    saucedemo_page.get_by_role("button", name="Login").click()

    # 错误容器中的文案证明系统给出了正确的失败原因。
    expect(
        saucedemo_page.locator('[data-test="error"]')
    ).to_have_text(
        "Epic sadface: Username and password do not match any user in this service"
    )

    # 错误凭据不能进入登录后的商品页。
    expect(saucedemo_page).not_to_have_url(
        re.compile(r"/inventory\.html$")
    )



def test_empty_username_shows_error(
    saucedemo_page: Page,
    standard_user_credentials: dict[str, str],
):
    # 空用户名属于表单必填校验，不是账号认证失败。
    saucedemo_page.get_by_placeholder("Username").fill("")
    saucedemo_page.get_by_placeholder("Password").fill(
        standard_user_credentials["password"]
    )

    saucedemo_page.get_by_role("button", name="Login").click()

    # 错误容器的文案证明必填校验返回了正确原因。
    expect(
        saucedemo_page.locator('[data-test="error"]')
    ).to_have_text("Epic sadface: Username is required")

    # 表单校验失败时不能进入登录后的商品页。
    expect(saucedemo_page).not_to_have_url(
        re.compile(r"/inventory\.html$")
    )
