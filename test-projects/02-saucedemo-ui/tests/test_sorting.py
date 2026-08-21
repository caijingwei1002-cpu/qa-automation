import re
from decimal import Decimal

import pytest
from playwright.sync_api import Page, expect


pytestmark = pytest.mark.regression


SORT_CASES = (
    pytest.param("az", "name", False, id="name-a-to-z"),
    pytest.param("za", "name", True, id="name-z-to-a"),
    pytest.param("lohi", "price", False, id="price-low-to-high"),
    pytest.param("hilo", "price", True, id="price-high-to-low"),
)


def parse_price(price_text: str) -> Decimal:
    """去掉货币符号并按 Decimal 解析，确保价格按数值而非文本排序。"""
    return Decimal(price_text.strip().removeprefix("$"))


@pytest.mark.parametrize(
    ("sort_option", "sort_field", "reverse"),
    SORT_CASES,
)
def test_inventory_sorting_matches_expected_order(
    saucedemo_page: Page,
    standard_user_credentials: dict[str, str],
    sort_option: str,
    sort_field: str,
    reverse: bool,
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

    product_names = page.locator(".inventory_item_name")
    product_prices = page.locator(".inventory_item_price")

    expect(product_names).to_have_count(6)
    expect(product_prices).to_have_count(6)

    original_names = product_names.all_text_contents()
    original_prices = product_prices.all_text_contents()

    if sort_field == "name":
        values_locator = product_names
        expected_values = sorted(
            original_names,
            reverse=reverse,
        )
    else:
        values_locator = product_prices
        expected_values = sorted(
            original_prices,
            key=parse_price,
            reverse=reverse,
        )

    sort_control = page.locator(
        '[data-test="product-sort-container"]'
    )
    expect(sort_control).to_be_visible()

    # A→Z 是默认状态，先切换到 Z→A，确保最终验证的是排序操作。
    if sort_option == "az":
        descending_names = sorted(
            original_names,
            reverse=True,
        )

        sort_control.select_option("za")
        expect(sort_control).to_have_value("za")
        expect(product_names).to_have_text(descending_names)

    sort_control.select_option(sort_option)
    expect(sort_control).to_have_value(sort_option)

    # Playwright 断言等待页面完成重排。
    expect(values_locator).to_have_text(expected_values)

    # 再提取实际列表，明确验证顺序没有被 set 等结构丢失。
    actual_values = values_locator.all_text_contents()
    assert actual_values == expected_values
