import re

import pytest
from playwright.sync_api import Page, expect


pytestmark = pytest.mark.regression


def test_add_one_item(
    saucedemo_page: Page,
    standard_user_credentials: dict[str, str],
):
    page = saucedemo_page

    page.get_by_placeholder("Username").fill(
        standard_user_credentials["username"]
    )
    page.get_by_placeholder("Password").fill(
        standard_user_credentials["password"]
    )
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(page.locator(".title")).to_have_text("Products")

    expected_name = "Sauce Labs Backpack"
    expected_price = "$29.99"

    inventory_item = page.locator(".inventory_item").filter(
        has_text=expected_name
    )

    # 先确认操作对象唯一，并验证列表页的商品身份和价格。
    expect(inventory_item).to_have_count(1)
    expect(
        inventory_item.locator(".inventory_item_name")
    ).to_have_text(expected_name)
    expect(
        inventory_item.locator(".inventory_item_price")
    ).to_have_text(expected_price)

    # 只在目标商品卡片内点击 Add to cart。
    inventory_item.get_by_role(
        "button",
        name="Add to cart",
    ).click()

    # 徽标证明购物车数量状态已经更新。
    cart_badge = page.locator(
        '[data-test="shopping-cart-badge"]'
    )
    expect(cart_badge).to_have_text("1")

    # 进入购物车，继续验证跨页面商品状态。
    page.locator(
        '[data-test="shopping-cart-link"]'
    ).click()

    expect(page).to_have_url(re.compile(r"/cart\.html$"))
    expect(page.locator(".title")).to_have_text("Your Cart")

    cart_items = page.locator(".cart_item")
    expect(cart_items).to_have_count(1)

    cart_item = cart_items.filter(has_text=expected_name)
    expect(cart_item).to_have_count(1)

    # 名称证明商品身份，价格证明关键数据跨页面一致。
    expect(
        cart_item.locator(".inventory_item_name")
    ).to_have_text(expected_name)
    expect(
        cart_item.locator(".inventory_item_price")
    ).to_have_text(expected_price)