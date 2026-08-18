import pytest
from playwright.sync_api import Page, expect
from helpers import add_todo

pytestmark = pytest.mark.regression


def test_todo_creation_waits_for_list_state(todo_page: Page):
    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")
    add_todo(todo_page, "Wait for state")

    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text(["Wait for state"])
    expect(todo_page.locator(".todo-count")).to_contain_text("1")
