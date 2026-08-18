from playwright.sync_api import Page


def add_todo(page: Page, text: str) -> None:
    todo_input = page.get_by_placeholder("What needs to be done?")
    todo_input.fill(text)
    todo_input.press("Enter")
