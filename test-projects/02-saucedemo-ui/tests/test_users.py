import re

import pytest
from playwright.sync_api import Page, expect
from test_data import LOCKED_OUT_USER, PROBLEM_USER


# 特殊账号场景属于完整回归范围，不纳入最小 smoke。
pytestmark = pytest.mark.regression


def test_locked_out_user_cannot_login(
    saucedemo_page: Page,
    standard_user_credentials: dict[str, str],
):
    # 使用锁定账号和有效密码，验证账号状态优先于正常登录路径。
    saucedemo_page.get_by_placeholder("Username").fill(LOCKED_OUT_USER)
    saucedemo_page.get_by_placeholder("Password").fill(
        standard_user_credentials["password"]
    )
    saucedemo_page.get_by_role("button", name="Login").click()

    # 错误提示证明系统识别并拒绝了锁定账号。
    expect(
        saucedemo_page.locator('[data-test="error"]')
    ).to_have_text(
        "Epic sadface: Sorry, this user has been locked out."
    )

    # 锁定账号不能进入登录后的商品页。
    expect(saucedemo_page).not_to_have_url(
        re.compile(r"/inventory\.html$")
    )


def test_problem_user_login_records_product_state(
    saucedemo_page: Page,
    standard_user_credentials: dict[str, str],
):
    # problem_user 的风险发生在登录后的页面状态，而不是登录认证阶段。
    saucedemo_page.get_by_placeholder("Username").fill(PROBLEM_USER)
    saucedemo_page.get_by_placeholder("Password").fill(
        standard_user_credentials["password"]
    )
    saucedemo_page.get_by_role("button", name="Login").click()

    # 先确认账号确实完成登录，避免把认证失败误记为商品页异常。
    expect(saucedemo_page).to_have_url(
        re.compile(r"/inventory\.html$")
    )
    expect(saucedemo_page.locator(".title")).to_have_text("Products")

    # 收集问题用户的商品图片状态，供验证证据记录和后续分析。
    product_images = saucedemo_page.locator(".inventory_item_img img")
    expect(product_images).to_have_count(6)
    image_states = product_images.evaluate_all(
        """images => images.map(image => ({
            alt: image.getAttribute("alt"),
            src: image.getAttribute("src"),
        }))"""
    )
    print(f"problem_user product image observation: {image_states}")
