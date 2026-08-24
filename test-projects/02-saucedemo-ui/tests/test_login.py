import logging
import re

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


logger = logging.getLogger(__name__)


# 标准登录是关键用户路径，也属于完整回归范围。
pytestmark = pytest.mark.regression


@pytest.mark.smoke
def test_standard_user_login(
    saucedemo_page: Page,
    standard_user_credentials: dict[str, str],
):
    # 使用 fixture 提供的账号，避免把凭据散落在测试代码中。
    login_page = LoginPage(saucedemo_page)
    logger.info("STEP: 使用标准用户凭据登录")
    login_page.login(
        standard_user_credentials["username"],
        standard_user_credentials["password"],
    )

    # 本测试只验证登录，不扩展到商品、购物车或结账流程。
    # URL 证明登录后的路由正确。
    logger.info("STEP: 验证登录后进入商品列表 URL")
    expect(saucedemo_page).to_have_url(
        re.compile(r"/inventory\.html$")
    )
    # 页面标题证明商品页已经真正加载，而不只是 URL 发生了跳转。
    logger.info("STEP: 验证商品列表页标题")
    expect(saucedemo_page.locator(".title")).to_have_text("Products")


def test_wrong_password_shows_error(
    saucedemo_page: Page,
    standard_user_credentials: dict[str, str],
):
    # 使用有效用户名配合错误密码，专门验证认证失败反馈。
    login_page = LoginPage(saucedemo_page)
    login_page.login(
        standard_user_credentials["username"],
        "wrong_password",
    )

    # 错误容器中的文案证明系统给出了正确的失败原因。
    expect(login_page.error_message).to_have_text(
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
    login_page = LoginPage(saucedemo_page)
    login_page.login(
        "",
        standard_user_credentials["password"],
    )

    # 错误容器的文案证明必填校验返回了正确原因。
    expect(login_page.error_message).to_have_text(
        "Epic sadface: Username is required"
    )
    # 表单校验失败时不能进入登录后的商品页。
    expect(saucedemo_page).not_to_have_url(
        re.compile(r"/inventory\.html$")
    )
