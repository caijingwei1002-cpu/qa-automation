import pytest
from playwright.sync_api import Page, expect
from helpers import add_todo

pytestmark = pytest.mark.regression


def test_blank_todo_is_not_created(todo_page: Page):
    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")
    add_todo(todo_page, "   ")

    expect(todo_items).to_have_count(0)


def test_todo_text_is_trimmed(todo_page: Page):
    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")
    add_todo(todo_page, "  Buy milk  ")

    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text(["Buy milk"])


def test_duplicate_todos_are_created(todo_page: Page):
    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")
    for _ in range(2):
        add_todo(todo_page, "Buy milk")

    expect(todo_items).to_have_count(2)
    expect(todo_items).to_have_text(["Buy milk", "Buy milk"])


def test_long_todo_text_is_preserved(todo_page: Page):
    long_text = "A" * 256
    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")
    add_todo(todo_page, long_text)
    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text([long_text])
