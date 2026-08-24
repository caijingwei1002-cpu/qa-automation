import re

import pytest
from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data import BACKPACK, BIKE_LIGHT, CHECKOUT_CUSTOMER


pytestmark = pytest.mark.regression


def test_two_item_checkout_preserves_product_records(
    saucedemo_page: Page,
    standard_user_credentials: dict[str, str],
):
    page = saucedemo_page

    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    # 测试负责定义业务预期。
    expected_records = {
        (BACKPACK["name"], BACKPACK["price"]),
        (BIKE_LIGHT["name"], BIKE_LIGHT["price"]),
    }

    login_page.login(
        standard_user_credentials["username"],
        standard_user_credentials["password"],
    )

    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(inventory_page.title).to_have_text("Products")

    inventory_page.add_item(BACKPACK["name"])
    inventory_page.add_item(BIKE_LIGHT["name"])

    expect(inventory_page.shopping_cart_badge).to_have_text("2")

    inventory_page.open_cart()

    expect(page).to_have_url(re.compile(r"/cart\.html$"))
    expect(cart_page.title).to_have_text("Your Cart")
    expect(cart_page.items).to_have_count(2)

    assert set(cart_page.item_records()) == expected_records

    cart_page.open_checkout()

    expect(page).to_have_url(
        re.compile(r"/checkout-step-one\.html$")
    )

    checkout_page.fill_customer_info(
        CHECKOUT_CUSTOMER["first_name"],
        CHECKOUT_CUSTOMER["last_name"],
        CHECKOUT_CUSTOMER["postal_code"],
    )
    checkout_page.continue_to_overview()

    expect(page).to_have_url(
        re.compile(r"/checkout-step-two\.html$")
    )
    expect(checkout_page.title).to_have_text("Checkout: Overview")
    expect(checkout_page.overview_items).to_have_count(2)

    # 验证跨页面后商品名称和价格没有变化。
    assert (
        set(checkout_page.overview_item_records())
        == expected_records
    )

    checkout_page.finish_checkout()

    expect(page).to_have_url(
        re.compile(r"/checkout-complete\.html$")
    )
    expect(checkout_page.complete_header).to_have_text(
        "Thank you for your order!"
    )
    expect(cart_page.shopping_cart_badge).to_have_count(0)

    cart_page.open_cart()
    expect(cart_page.items).to_have_count(0)
