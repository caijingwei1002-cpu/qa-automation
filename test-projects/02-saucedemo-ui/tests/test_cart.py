import re

import pytest
from playwright.sync_api import Page, expect
from decimal import Decimal
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytestmark = pytest.mark.regression


def test_add_one_item(
    saucedemo_page: Page,
    standard_user_credentials: dict[str, str],
):
    page = saucedemo_page

    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.login(
        standard_user_credentials["username"],
        standard_user_credentials["password"],
    )
    expected_name = "Sauce Labs Backpack"
    expected_price = "$29.99"

    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(inventory_page.title).to_have_text("Products")

    inventory_item = inventory_page.item(expected_name)

    # 先确认操作对象唯一，并验证列表页的商品身份和价格。
    expect(inventory_item).to_have_count(1)
    expect(
        inventory_page.item_name(inventory_item)
    ).to_have_text(expected_name)
    expect(
        inventory_page.item_price(inventory_item)
    ).to_have_text(expected_price)

    # 只在目标商品卡片内点击 Add to cart。
    inventory_page.add_item(expected_name)

    # 徽标证明购物车数量状态已经更新。
    expect(inventory_page.shopping_cart_badge).to_have_text("1")

    # 进入购物车，继续验证跨页面商品状态。
    inventory_page.open_cart()
    cart_page = CartPage(page)

    expect(page).to_have_url(re.compile(r"/cart\.html$"))
    expect(cart_page.title).to_have_text("Your Cart")

    cart_items = cart_page.items
    expect(cart_items).to_have_count(1)

    cart_item = cart_page.item(expected_name)
    expect(cart_item).to_have_count(1)
    # 名称证明商品身份，价格证明关键数据跨页面一致。
    expect(
        cart_page.item_name(cart_item)
    ).to_have_text(expected_name)
    expect(
        cart_page.item_price(cart_item)
    ).to_have_text(expected_price)


def parse_price(price_text: str) -> Decimal:
    """将页面货币文本转为 Decimal，避免按字符串或浮点近似比较金额。"""
    return Decimal(price_text.strip().removeprefix("$"))


def test_add_multiple_items_and_verify_cart(
    saucedemo_page: Page,
    standard_user_credentials: dict[str, str],
):
    page = saucedemo_page

    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.login(
        standard_user_credentials["username"],
        standard_user_credentials["password"],
    )

    expect(page).to_have_url(re.compile(r"/inventory\.html$"))

    # 用独立的名称—价格预期驱动加购，避免从页面实时数据生成 Expected。
    selected_products = (
        ("Sauce Labs Backpack", "$29.99"),
        ("Sauce Labs Bike Light", "$9.99"),
        ("Sauce Labs Onesie", "$7.99"),
    )

    # 元组集合保留商品与价格的绑定关系，Decimal 合计作为后续金额校验基准。
    expected_items = set(selected_products)
    expected_subtotal = sum(
        parse_price(price)
        for _, price in selected_products
    )

    # 先定位目标商品卡片，再在卡片内部点击按钮，避免点击错误商品。
    for product_name, expected_price in selected_products:
        inventory_item = inventory_page.item(product_name)

        expect(inventory_item).to_have_count(1)
        expect(
            inventory_page.item_price(inventory_item)
        ).to_have_text(expected_price)

        inventory_page.add_item(product_name)

    # 徽标只证明加入数量，后续还要进入购物车验证实际条目。
    expect(inventory_page.shopping_cart_badge).to_have_text(
        str(len(selected_products))
    )

    inventory_page.open_cart()
    cart_page = CartPage(page)

    expect(page).to_have_url(re.compile(r"/cart\.html$"))

    cart_items = cart_page.items
    expect(cart_items).to_have_count(len(selected_products))

    # 从页面提取实际的名称—价格记录，用于与独立预期比较。
    actual_items = cart_page.item_records()

    # 数量防止集合去重掩盖重复条目，元组集合验证成员和字段关联。
    assert len(actual_items) == len(selected_products)
    assert set(actual_items) == expected_items

    # 金额汇总验证购物车价格没有遗漏、重复或串位。
    actual_subtotal = sum(
        parse_price(price)
        for _, price in actual_items
    )
    assert actual_subtotal == expected_subtotal
