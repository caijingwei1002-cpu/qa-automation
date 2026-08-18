from playwright.sync_api import Page


def add_todo(page: Page, text: str) -> None:
    # helper 封装稳定的创建动作，不隐藏任何 expect 断言。
    todo_input = page.get_by_placeholder("What needs to be done?")
    todo_input.fill(text)
    todo_input.press("Enter")
