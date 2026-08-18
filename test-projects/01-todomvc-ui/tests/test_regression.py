import pytest
from playwright.sync_api import Page, expect

from helpers import add_todo


pytestmark = pytest.mark.regression


def test_regression_state_transition_workflow(todo_page: Page):
    """覆盖高风险的 Todo 状态联动，而不是只验证单个功能。"""
    add_todo(todo_page, "Active item")
    add_todo(todo_page, "Completed item")

    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")
    expect(todo_items).to_have_count(2)
    expect(todo_items).to_have_text(["Active item", "Completed item"])

    completed_item = todo_items.filter(has_text="Completed item")
    completed_toggle = completed_item.get_by_role("checkbox")
    completed_toggle.check()

    expect(completed_toggle).to_be_checked()
    expect(completed_item).to_have_class("completed")
    expect(todo_page.locator(".todo-count")).to_contain_text("1")

    active_filter = todo_page.get_by_role("link", name="Active", exact=True)
    active_filter.click()
    expect(active_filter).to_have_class("selected")
    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text(["Active item"])

    completed_filter = todo_page.get_by_role(
        "link", name="Completed", exact=True
    )
    completed_filter.click()
    expect(completed_filter).to_have_class("selected")
    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text(["Completed item"])

    all_filter = todo_page.get_by_role("link", name="All", exact=True)
    all_filter.click()
    expect(all_filter).to_have_class("selected")
    expect(todo_items).to_have_count(2)

    completed_item.hover()
    completed_item.get_by_role("button").click()

    expect(completed_item).to_have_count(0)
    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text(["Active item"])
    expect(todo_page.locator(".todo-count")).to_contain_text("1")
