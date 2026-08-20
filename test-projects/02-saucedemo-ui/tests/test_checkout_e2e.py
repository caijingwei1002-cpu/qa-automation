import re

import pytest
from playwright.sync_api import Page, expect


pytestmark = pytest.mark.regression

SUMMARY_URL = re.compile(r"/checkout-step-two\.html$")
COMPLETE_URL = re.compile(r"/checkout-complete\.html$")
PRODUCT_NAME = "Sauce Labs Backpack"
PRODUCT_PRICE = "$29.99"


def open_order_summary(
    page: Page,
    credentials: dict[str, str],
):
    """从登录开始准备到订单概览页，形成完整下单的前置状态。"""
    page.get_by_placeholder("Username").fill(credentials["username"])
    page.get_by_placeholder("Password").fill(credentials["password"])
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(page.locator(".title")).to_have_text("Products")

    inventory_item = page.locator(".inventory_item").filter(
        has_text=PRODUCT_NAME
    )
    expect(inventory_item).to_have_count(1)
    expect(
        inventory_item.locator(".inventory_item_price")
    ).to_have_text(PRODUCT_PRICE)
    inventory_item.get_by_role("button", name="Add to cart").click()

    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")
    page.locator('[data-test="shopping-cart-link"]').click()
    expect(page).to_have_url(re.compile(r"/cart\.html$"))
    expect(page.locator(".title")).to_have_text("Your Cart")
    expect(page.locator(".cart_item")).to_have_count(1)
    expect(
        page.locator(".cart_item").locator(".inventory_item_name")
    ).to_have_text(PRODUCT_NAME)
    page.get_by_role("button", name="Checkout").click()

    expect(page).to_have_url(re.compile(r"/checkout-step-one\.html$"))
    expect(page.locator(".title")).to_have_text("Checkout: Your Information")
    page.locator('[data-test="firstName"]').fill("Ada")
    page.locator('[data-test="lastName"]').fill("Lovelace")
    page.locator('[data-test="postalCode"]').fill("10001")
    page.get_by_role("button", name="Continue").click()

    expect(page).to_have_url(SUMMARY_URL)
    expect(page.locator(".title")).to_have_text("Checkout: Overview")


def test_complete_checkout_order(
    saucedemo_page: Page,
    standard_user_credentials: dict[str, str],
):
    page = saucedemo_page
    open_order_summary(page, standard_user_credentials)

    page.get_by_role("button", name="Finish").click()

    # URL 和标题证明订单进入完成页面，成功文案证明业务结果可观察。
    expect(page).to_have_url(COMPLETE_URL)
    expect(page.locator(".title")).to_have_text("Checkout: Complete!")
    expect(page.locator(".complete-header")).to_have_text(
        "Thank you for your order!"
    )

    # 完成订单后，购物车徽标和实际条目都应清空。
    expect(
        page.locator('[data-test="shopping-cart-badge"]')
    ).to_have_count(0)
    page.locator('[data-test="shopping-cart-link"]').click()
    expect(page).to_have_url(re.compile(r"/cart\.html$"))
    expect(page.locator(".cart_item")).to_have_count(0)
