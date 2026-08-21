from playwright.sync_api import Locator, Page


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator(".title")
        self.items = page.locator(".cart_item")
        self.checkout_button = page.get_by_role(
            "button",
            name="Checkout",
        )
        self.shopping_cart_badge = page.locator(
            '[data-test="shopping-cart-badge"]'
        )
        self.shopping_cart_link = page.locator(
            '[data-test="shopping-cart-link"]'
        )

    def item(self, product_name: str) -> Locator:
        return self.items.filter(has_text=product_name)

    def item_name(self, item: Locator) -> Locator:
        return item.locator(".inventory_item_name")

    def item_price(self, item: Locator) -> Locator:
        return item.locator(".inventory_item_price")

    def item_records(self) -> list[tuple[str, str]]:
        records = []

        for index in range(self.items.count()):
            item = self.items.nth(index)
            records.append(
                (
                    self.item_name(item).inner_text(),
                    self.item_price(item).inner_text(),
                )
            )

        return records

    def open_checkout(self) -> None:
        self.checkout_button.click()

    def open_cart(self) -> None:
        self.shopping_cart_link.click()
