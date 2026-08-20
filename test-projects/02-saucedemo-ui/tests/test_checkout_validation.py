import re

import pytest
from playwright.sync_api import Page, expect


pytestmark = pytest.mark.regression

CHECKOUT_FORM_URL = re.compile(r"/checkout-step-one\.html$")
PRODUCT_NAME = "Sauce Labs Backpack"
VALID_CHECKOUT_VALUES = {
    "firstName": "Ada",
    "lastName": "Lovelace",
    "postalCode": "10001",
}
CHECKOUT_REQUIRED_FIELD_CASES = [
    ("firstName", "Error: First Name is required"),
    ("lastName", "Error: Last Name is required"),
    ("postalCode", "Error: Postal Code is required"),
]


def open_checkout_form(
    page: Page,
    credentials: dict[str, str],
):
    """登录并把测试状态准备到 Checkout information 页面。"""
    page.get_by_placeholder("Username").fill(credentials["username"])
    page.get_by_placeholder("Password").fill(credentials["password"])
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(page.locator(".title")).to_have_text("Products")

    inventory_item = page.locator(".inventory_item").filter(
        has_text=PRODUCT_NAME
    )
    expect(inventory_item).to_have_count(1)
    inventory_item.get_by_role("button", name="Add to cart").click()

    page.locator('[data-test="shopping-cart-link"]').click()
    expect(page).to_have_url(re.compile(r"/cart\.html$"))
    expect(page.locator(".title")).to_have_text("Your Cart")

    page.get_by_role("button", name="Checkout").click()
    expect(page).to_have_url(CHECKOUT_FORM_URL)
    expect(page.locator(".title")).to_have_text("Checkout: Your Information")


@pytest.mark.parametrize(
    "missing_field, expected_error",
    CHECKOUT_REQUIRED_FIELD_CASES,
    ids=["missing-first-name", "missing-last-name", "missing-postal-code"],
)
def test_checkout_required_field_validation(
    saucedemo_page: Page,
    standard_user_credentials: dict[str, str],
    missing_field: str,
    expected_error: str,
):
    page = saucedemo_page
    open_checkout_form(page, standard_user_credentials)

    for field_name, valid_value in VALID_CHECKOUT_VALUES.items():
        field = page.locator(f'[data-test="{field_name}"]')
        field.fill("" if field_name == missing_field else valid_value)

    page.get_by_role("button", name="Continue").click()

    expect(page.locator('[data-test="error"]')).to_have_text(
        expected_error
    )
    expect(page).to_have_url(CHECKOUT_FORM_URL)
