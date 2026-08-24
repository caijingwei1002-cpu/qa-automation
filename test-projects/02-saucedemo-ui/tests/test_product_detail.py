import re

import pytest
from playwright.sync_api import Page, expect
from test_data import BACKPACK

pytestmark = pytest.mark.regression


def test_product_detail_matches_inventory_and_returns(
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

    expected_name = BACKPACK["name"]
    expected_price = BACKPACK["price"]

    inventory_item = page.locator(".inventory_item").filter(
        has_text=expected_name
    )

    # 先确认列表页定位到唯一的目标商品。
    expect(inventory_item).to_have_count(1)
    expect(
        inventory_item.locator(".inventory_item_name")
    ).to_have_text(expected_name)
    expect(
        inventory_item.locator(".inventory_item_price")
    ).to_have_text(expected_price)

    # 点击列表中的目标商品，而不是直接访问详情 URL。
    inventory_item.locator(".inventory_item_name").click()

    # 验证进入了带商品 id 的详情路由。
    expect(page).to_have_url(
        re.compile(r"/inventory-item\.html\?id=\d+$")
    )

    # 验证详情页身份和关键数据与列表页一致。
    expect(
        page.locator(".inventory_details_name")
    ).to_have_text(expected_name)
    expect(
        page.locator(".inventory_details_price")
    ).to_have_text(expected_price)

    # 验证能够返回商品列表。
    page.get_by_role("button", name="Back to products").click()

    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(page.locator(".title")).to_have_text("Products")