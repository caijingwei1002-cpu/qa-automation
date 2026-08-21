from playwright.sync_api import Page


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator(".title")

        self.first_name_input = page.locator(
            '[data-test="firstName"]'
        )
        self.last_name_input = page.locator(
            '[data-test="lastName"]'
        )
        self.postal_code_input = page.locator(
            '[data-test="postalCode"]'
        )

        self.continue_button = page.get_by_role(
            "button",
            name="Continue",
        )
        self.finish_button = page.get_by_role(
            "button",
            name="Finish",
        )
        self.complete_header = page.locator(
            ".complete-header"
        )

    def fill_customer_info(
        self,
        first_name: str,
        last_name: str,
        postal_code: str,
    ) -> None:
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def continue_to_overview(self) -> None:
        self.continue_button.click()

    def finish_checkout(self) -> None:
        self.finish_button.click()