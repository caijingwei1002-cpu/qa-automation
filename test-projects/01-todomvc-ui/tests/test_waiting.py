import pytest
from playwright.sync_api import Page, expect


pytestmark = pytest.mark.regression


def test_todo_creation_waits_for_list_state(todo_page: Page):
    todo_input = todo_page.get_by_placeholder("What needs to be done?")
    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")

    todo_input.fill("Wait for state")
    todo_input.press("Enter")

    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text(["Wait for state"])
    expect(todo_page.locator(".todo-count")).to_contain_text("1")
