import pytest
from playwright.sync_api import Page, expect


pytestmark = pytest.mark.regression


def test_clear_completed_todos(todo_page_with_todos: Page):
    todo_items = todo_page_with_todos.locator(".todo-list").get_by_role("listitem")

    expect(todo_items).to_have_count(2)
    expect(todo_items).to_have_text(["Buy milk", "Learn pytest"])

    completed_item = todo_items.filter(has_text="Learn pytest")
    completed_toggle = completed_item.get_by_role("checkbox")
    completed_toggle.check()

    expect(completed_toggle).to_be_checked()
    expect(completed_item).to_have_class("completed")
    expect(todo_page_with_todos.locator(".todo-count")).to_contain_text("1")

    clear_completed = todo_page_with_todos.get_by_role(
        "button", name="Clear completed", exact=True
    )
    clear_completed.click()

    expect(completed_item).to_have_count(0)
    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text(["Buy milk"])
    expect(todo_page_with_todos.locator(".todo-count")).to_contain_text("1")
