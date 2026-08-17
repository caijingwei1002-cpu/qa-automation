"""Day 8 locator rules.

Prefer role, label, and placeholder for user-facing elements.
Use text only when it is unique or scoped to a business object.
Use CSS mainly for structural containers or missing semantic hooks.
"""

from playwright.sync_api import Page, expect


def test_prefer_semantic_locators(todo_page: Page):
    todo_input = todo_page.get_by_placeholder("What needs to be done?")
    todo_input.fill("Stable locator")
    todo_input.press("Enter")

    todo_item = (
        todo_page.locator(".todo-list")
        .get_by_role("listitem")
        .filter(has_text="Stable locator")
    )

    expect(todo_item).to_have_count(1)
    expect(todo_item).to_contain_text("Stable locator")
    expect(todo_item.get_by_role("checkbox")).to_have_count(1)
    expect(todo_item.get_by_role("checkbox")).to_be_visible()