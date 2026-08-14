from playwright.sync_api import Page, expect


def test_add_todo(todo_page: Page):
    todo_input = todo_page.get_by_placeholder("What needs to be done?")
    todo_input.fill("Buy milk")
    todo_input.press("Enter")

    expect(todo_page.locator(".todo-list li")).to_have_count(1)
    expect(todo_page.locator(".todo-list li label")).to_have_text("Buy milk")
    expect(todo_page.locator(".todo-count")).to_contain_text("1")


def test_complete_todo(todo_page: Page):
    todo_input = todo_page.get_by_placeholder("What needs to be done?")
    todo_input.fill("Learn checkbox state")
    todo_input.press("Enter")

    todo_item = todo_page.locator(".todo-list li")
    expect(todo_item).to_have_count(1)
    expect(todo_page.locator(".todo-count")).to_contain_text("1")
    toggle = todo_item.locator(".toggle")

    toggle.check()

    expect(toggle).to_be_checked()
    expect(todo_item).to_have_class("completed")
    expect(todo_page.locator(".todo-count")).to_contain_text("0")