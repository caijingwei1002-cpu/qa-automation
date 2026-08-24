import re
from decimal import Decimal

import pytest
from playwright.sync_api import Page, expect
from test_data import BACKPACK, CHECKOUT_CUSTOMER


pytestmark = pytest.mark.regression

SUMMARY_URL = re.compile(r"/checkout-step-two\.html$")
MONEY_PATTERN = re.compile(r"\$([0-9]+(?:\.[0-9]{2})?)")


def parse_money(text: str) -> Decimal:
    """从页面货币文本中提取金额并转换为 Decimal。"""
    match = MONEY_PATTERN.search(text)
    if match is None:
        raise ValueError(f"金额文本缺少货币值: {text!r}")
    return Decimal(match.group(1))


def open_checkout_summary(
    page: Page,
    credentials: dict[str, str],
):
    """登录、加购一个商品并进入 Checkout overview 页面。"""
    page.get_by_placeholder("Username").fill(credentials["username"])
    page.get_by_placeholder("Password").fill(credentials["password"])
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(page.locator(".title")).to_have_text("Products")

    inventory_item = page.locator(".inventory_item").filter(
        has_text=BACKPACK["name"]
    )
    expect(inventory_item).to_have_count(1)
    expect(
        inventory_item.locator(".inventory_item_price")
    ).to_have_text(BACKPACK["price"])
    inventory_item.get_by_role("button", name="Add to cart").click()

    page.locator('[data-test="shopping-cart-link"]').click()
    expect(page).to_have_url(re.compile(r"/cart\.html$"))
    expect(page.locator(".title")).to_have_text("Your Cart")
    expect(page.locator(".cart_item")).to_have_count(1)
    page.get_by_role("button", name="Checkout").click()

    expect(page).to_have_url(re.compile(r"/checkout-step-one\.html$"))
    expect(page.locator(".title")).to_have_text("Checkout: Your Information")
    page.locator('[data-test="firstName"]').fill(
        CHECKOUT_CUSTOMER["first_name"]
    )
    page.locator('[data-test="lastName"]').fill(
        CHECKOUT_CUSTOMER["last_name"]
    )
    page.locator('[data-test="postalCode"]').fill(
        CHECKOUT_CUSTOMER["postal_code"]
    )
    page.get_by_role("button", name="Continue").click()

    expect(page).to_have_url(SUMMARY_URL)
    expect(page.locator(".title")).to_have_text("Checkout: Overview")


def test_checkout_summary_amounts(
    saucedemo_page: Page,
    standard_user_credentials: dict[str, str],
):
    page = saucedemo_page
    open_checkout_summary(page, standard_user_credentials)

    expected_subtotal = parse_money(BACKPACK["price"])
    actual_subtotal = parse_money(
        page.locator(".summary_subtotal_label").inner_text()
    )
    actual_tax = parse_money(
        page.locator(".summary_tax_label").inner_text()
    )
    actual_total = parse_money(
        page.locator(".summary_total_label").inner_text()
    )

    # 小计必须与独立的商品预期一致，不能从同一页面生成 Expected。
    assert actual_subtotal == expected_subtotal
    # 税费是金额字段，必须可解析且为正数。
    assert actual_tax > Decimal("0")
    # 总价不变量：商品小计加税费等于总价。
    assert actual_total == actual_subtotal + actual_tax
