import pytest
from playwright.sync_api import Page, expect


@pytest.mark.parametrize(
    "todo_text",
    ["Buy milk", "Learn pytest", "Write parameterized test"],
)
def test_create_todo_for_each_input(todo_page: Page, todo_text: str):
    todo_input = todo_page.get_by_placeholder("What needs to be done?")
    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")

    todo_input.fill(todo_text)
    todo_input.press("Enter")

    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text([todo_text])
