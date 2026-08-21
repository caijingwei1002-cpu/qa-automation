from playwright.sync_api import Locator, Page


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator(".title")
        self.items = page.locator(".inventory_item")
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

    def item_image(self, item: Locator) -> Locator:
        return item.locator(".inventory_item_img img")

    def add_item(self, product_name: str) -> None:
        self.item(product_name).get_by_role(
            "button",
            name="Add to cart",
        ).click()

    def open_cart(self) -> None:
        self.shopping_cart_link.click()

    def product_names(self) -> list[str]:
        return self.items.locator(
            ".inventory_item_name"
        ).all_text_contents()