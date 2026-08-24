import re

import pytest
from playwright.sync_api import Page, expect
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data import BACKPACK, CHECKOUT_CUSTOMER

pytestmark = pytest.mark.regression

SUMMARY_URL = re.compile(r"/checkout-step-two\.html$")
COMPLETE_URL = re.compile(r"/checkout-complete\.html$")



def test_complete_checkout_order(
    saucedemo_page: Page,
    standard_user_credentials: dict[str, str],
):
    page = saucedemo_page

    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    login_page.login(
        standard_user_credentials["username"],
        standard_user_credentials["password"],
    )

    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(inventory_page.title).to_have_text("Products")

    inventory_page.add_item(BACKPACK["name"])
    expect(inventory_page.shopping_cart_badge).to_have_text("1")

    inventory_page.open_cart()

    expect(page).to_have_url(re.compile(r"/cart\.html$"))
    expect(cart_page.title).to_have_text("Your Cart")
    expect(cart_page.items).to_have_count(1)

    cart_item = cart_page.item(BACKPACK["name"])
    expect(cart_page.item_name(cart_item)).to_have_text(BACKPACK["name"])
    expect(cart_page.item_price(cart_item)).to_have_text(BACKPACK["price"])

    cart_page.open_checkout()

    expect(page).to_have_url(
        re.compile(r"/checkout-step-one\.html$")
    )
    expect(checkout_page.title).to_have_text(
        "Checkout: Your Information"
    )

    checkout_page.fill_customer_info(
        CHECKOUT_CUSTOMER["first_name"],
        CHECKOUT_CUSTOMER["last_name"],
        CHECKOUT_CUSTOMER["postal_code"],
    )
    checkout_page.continue_to_overview()

    expect(page).to_have_url(SUMMARY_URL)
    expect(checkout_page.title).to_have_text(
        "Checkout: Overview"
    )

    checkout_page.finish_checkout()

    # URL 和标题证明订单进入完成页面，成功文案证明业务结果可观察。
    expect(page).to_have_url(COMPLETE_URL)
    expect(checkout_page.title).to_have_text(
        "Checkout: Complete!"
    )
    expect(checkout_page.complete_header).to_have_text(
        "Thank you for your order!"
    )

    # 完成订单后，购物车徽标和实际条目都应清空。
    expect(cart_page.shopping_cart_badge).to_have_count(0)
    cart_page.open_cart()
    expect(page).to_have_url(re.compile(r"/cart\.html$"))
    expect(cart_page.items).to_have_count(0)
