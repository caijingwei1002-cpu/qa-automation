import re

import pytest
from playwright.sync_api import Page, expect
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


pytestmark = pytest.mark.regression


EXPECTED_PRODUCTS = (
    ("Sauce Labs Backpack", "$29.99"),
    ("Sauce Labs Bike Light", "$9.99"),
    ("Sauce Labs Bolt T-Shirt", "$15.99"),
    ("Sauce Labs Fleece Jacket", "$49.99"),
    ("Sauce Labs Onesie", "$7.99"),
    ("Test.allTheThings() T-Shirt (Red)", "$15.99"),
)


def test_inventory_list_is_complete(
    saucedemo_page: Page,
    standard_user_credentials: dict[str, str],
):
    page = saucedemo_page
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    # 使用 fixture 提供的账号，避免把凭据散落在测试代码中。
    login_page.login(
        standard_user_credentials["username"],
        standard_user_credentials["password"],
    )

    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(inventory_page.title).to_have_text("Products")

    items = inventory_page.items
    # 集合层断言：确认商品数量完整。
    expect(items).to_have_count(len(EXPECTED_PRODUCTS))

    # 集合层断言：确认所有商品名称都存在，而不是只检查第一项。
    expected_names = {name for name, _ in EXPECTED_PRODUCTS}
    actual_names = set(inventory_page.product_names())
    assert actual_names == expected_names

    # 元素层断言：逐项确认价格和图片。
    for product_name, expected_price in EXPECTED_PRODUCTS:
        item = inventory_page.item(product_name)

        expect(item).to_have_count(1)
        expect(
            inventory_page.item_name(item)
        ).to_have_text(product_name)
        expect(
            inventory_page.item_price(item)
        ).to_have_text(expected_price)

        product_image = inventory_page.item_image(item)
        expect(product_image).to_have_count(1)
        expect(product_image).to_be_visible()
        expect(product_image).to_have_attribute("alt", re.compile(r".+"))
        expect(product_image).to_have_attribute("src", re.compile(r".+"))
