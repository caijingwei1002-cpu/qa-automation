import re

import pytest
from playwright.sync_api import Page, expect
from test_data import BACKPACK


pytestmark = pytest.mark.regression


EXPECTED_NAME = BACKPACK["name"]
EXPECTED_PRICE = BACKPACK["price"]


def login_as_standard_user(
    page: Page,
    credentials: dict[str, str],
):
    """完成两个移除场景共用的登录前置，并确认已进入商品列表。"""
    page.get_by_placeholder("Username").fill(credentials["username"])
    page.get_by_placeholder("Password").fill(credentials["password"])
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(page.locator(".title")).to_have_text("Products")


def test_remove_item_from_inventory_updates_cart_state(
    saucedemo_page: Page,
    standard_user_credentials: dict[str, str],
):
    page = saucedemo_page
    login_as_standard_user(page, standard_user_credentials)

    inventory_item = page.locator(".inventory_item").filter(
        has_text=EXPECTED_NAME
    )
    expect(inventory_item).to_have_count(1)

    # 先建立已加入状态，才能验证 Remove 后是否真正回退。
    inventory_item.get_by_role(
        "button",
        name="Add to cart",
    ).click()

    expect(
        inventory_item.get_by_role("button", name="Remove")
    ).to_be_visible()
    expect(
        page.locator('[data-test="shopping-cart-badge"]')
    ).to_have_text("1")

    inventory_item.get_by_role(
        "button",
        name="Remove",
    ).click()

    # 列表页操作状态恢复，说明移除动作已经生效。
    expect(
        inventory_item.get_by_role("button", name="Add to cart")
    ).to_be_visible()

    # 徽标消失，说明购物车数量从 1 回退为 0。
    expect(
        page.locator('[data-test="shopping-cart-badge"]')
    ).to_have_count(0)

    page.locator('[data-test="shopping-cart-link"]').click()

    expect(page).to_have_url(re.compile(r"/cart\.html$"))
    expect(page.locator(".title")).to_have_text("Your Cart")
    expect(page.locator(".cart_item")).to_have_count(0)


def test_remove_item_from_cart_updates_inventory_state(
    saucedemo_page: Page,
    standard_user_credentials: dict[str, str],
):
    page = saucedemo_page
    login_as_standard_user(page, standard_user_credentials)

    inventory_item = page.locator(".inventory_item").filter(
        has_text=EXPECTED_NAME
    )
    expect(inventory_item).to_have_count(1)
    expect(
        inventory_item.locator(".inventory_item_price")
    ).to_have_text(EXPECTED_PRICE)

    # 从列表页加入后切换到购物车，验证购物车入口的 Remove 行为。
    inventory_item.get_by_role(
        "button",
        name="Add to cart",
    ).click()

    expect(
        page.locator('[data-test="shopping-cart-badge"]')
    ).to_have_text("1")

    page.locator('[data-test="shopping-cart-link"]').click()

    expect(page).to_have_url(re.compile(r"/cart\.html$"))

    cart_items = page.locator(".cart_item")
    expect(cart_items).to_have_count(1)

    cart_item = cart_items.filter(has_text=EXPECTED_NAME)
    expect(cart_item).to_have_count(1)
    expect(
        cart_item.locator(".inventory_item_name")
    ).to_have_text(EXPECTED_NAME)
    expect(
        cart_item.locator(".inventory_item_price")
    ).to_have_text(EXPECTED_PRICE)

    cart_item.get_by_role(
        "button",
        name="Remove",
    ).click()

    # 购物车内容和徽标必须同步回退。
    expect(cart_items).to_have_count(0)
    expect(
        page.locator('[data-test="shopping-cart-badge"]')
    ).to_have_count(0)

    # 返回列表页，确认同一商品已经恢复为未加入状态。
    page.get_by_role(
        "button",
        name="Continue Shopping",
    ).click()

    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(page.locator(".title")).to_have_text("Products")
    expect(
        page.locator(".inventory_item")
        .filter(has_text=EXPECTED_NAME)
        .get_by_role("button", name="Add to cart")
    ).to_be_visible()
