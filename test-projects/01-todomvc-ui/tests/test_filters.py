import pytest
from playwright.sync_api import Page, expect


pytestmark = pytest.mark.regression
# 筛选测试同时验证视图选择状态和实际展示的数据集合。


@pytest.mark.smoke
def test_filter_todos(todo_page_with_todos: Page):
    # 使用页面范围内的 listitem 集合，避免把页面其他文本当成 Todo。
    todo_items = todo_page_with_todos.locator(".todo-list").get_by_role("listitem")

    # 先完成第二条 Todo，形成 Active/Completed 两种明确状态。
    expect(todo_items).to_have_count(2)
    expect(todo_items).to_have_text(["Buy milk", "Learn pytest"])

    completed_todo = todo_items.filter(has_text="Learn pytest")
    completed_toggle = completed_todo.get_by_role("checkbox")
    completed_toggle.check()

    expect(completed_toggle).to_be_checked()
    expect(completed_todo).to_have_class("completed")

    all_filter = todo_page_with_todos.get_by_role(
        "link", name="All", exact=True
    )
    # All 应展示全部数据，并将当前筛选链接标记为 selected。
    all_filter.click()

    expect(all_filter).to_have_class("selected")
    expect(todo_items).to_have_count(2)
    expect(todo_items).to_have_text(["Buy milk", "Learn pytest"])

    active_filter = todo_page_with_todos.get_by_role(
        "link", name="Active", exact=True
    )
    # Active 只应留下未完成的 Buy milk。
    active_filter.click()

    expect(active_filter).to_have_class("selected")
    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text(["Buy milk"])

    completed_filter = todo_page_with_todos.get_by_role(
        "link", name="Completed", exact=True
    )
    # Completed 只应留下已完成的 Learn pytest。
    completed_filter.click()

    expect(completed_filter).to_have_class("selected")
    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text(["Learn pytest"])
