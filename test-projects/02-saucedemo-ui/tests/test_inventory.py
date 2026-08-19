import re

import pytest
from playwright.sync_api import Page, expect


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

    page.get_by_placeholder("Username").fill(
        standard_user_credentials["username"]
    )
    page.get_by_placeholder("Password").fill(
        standard_user_credentials["password"]
    )
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(page.locator(".title")).to_have_text("Products")

    items = page.locator(".inventory_item")

    # 集合层断言：确认商品数量完整。
    expect(items).to_have_count(len(EXPECTED_PRODUCTS))

    # 集合层断言：确认所有商品名称都存在，而不是只检查第一项。
    expected_names = {name for name, _ in EXPECTED_PRODUCTS}
    actual_names = set(
        items.locator(".inventory_item_name").all_text_contents()
    )
    assert actual_names == expected_names

    # 元素层断言：逐项确认价格和图片。
    for product_name, expected_price in EXPECTED_PRODUCTS:
        item = items.filter(has_text=product_name)

        expect(item).to_have_count(1)
        expect(
            item.locator(".inventory_item_name")
        ).to_have_text(product_name)
        expect(
            item.locator(".inventory_item_price")
        ).to_have_text(expected_price)

        product_image = item.locator(".inventory_item_img img")
        expect(product_image).to_have_count(1)
        expect(product_image).to_be_visible()
        expect(product_image).to_have_attribute("alt", re.compile(r".+"))
        expect(product_image).to_have_attribute("src", re.compile(r".+"))
