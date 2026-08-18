import pytest
from playwright.sync_api import Page, expect


pytestmark = pytest.mark.regression


def test_blank_todo_is_not_created(todo_page: Page):
    todo_input = todo_page.get_by_placeholder("What needs to be done?")
    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")
    todo_input.fill("   ")
    todo_input.press("Enter")

    expect(todo_items).to_have_count(0)


def test_todo_text_is_trimmed(todo_page: Page):
    todo_input = todo_page.get_by_placeholder("What needs to be done?")
    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")
    todo_input.fill("  Buy milk  ")
    todo_input.press("Enter")

    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text(["Buy milk"])


def test_duplicate_todos_are_created(todo_page: Page):
    todo_input = todo_page.get_by_placeholder("What needs to be done?")
    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")
    for _ in range(2):
        todo_input.fill("Buy milk")
        todo_input.press("Enter")

    expect(todo_items).to_have_count(2)
    expect(todo_items).to_have_text(["Buy milk", "Buy milk"])


def test_long_todo_text_is_preserved(todo_page: Page):
    long_text = "A" * 256
    todo_input = todo_page.get_by_placeholder("What needs to be done?")
    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")
    todo_input.fill(long_text)
    todo_input.press("Enter")

    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text([long_text])
