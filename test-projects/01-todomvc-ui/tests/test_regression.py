import pytest
from playwright.sync_api import Page, expect

from helpers import add_todo


pytestmark = pytest.mark.regression
# 这是跨功能状态联动场景，重点不是单个按钮而是连续操作后的整体一致性。


def test_regression_state_transition_workflow(todo_page: Page):
    """覆盖高风险的 Todo 状态联动，而不是只验证单个功能。"""
    # 准备一个 Active 项和一个将要转换为 Completed 的项目。
    add_todo(todo_page, "Active item")
    add_todo(todo_page, "Completed item")

    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")
    # 前置断言确保回归链路从预期数据状态开始。
    expect(todo_items).to_have_count(2)
    expect(todo_items).to_have_text(["Active item", "Completed item"])

    completed_item = todo_items.filter(has_text="Completed item")
    completed_toggle = completed_item.get_by_role("checkbox")
    completed_toggle.check()

    # 状态转换后验证 checkbox、CSS 状态和未完成计数同步。
    expect(completed_toggle).to_be_checked()
    expect(completed_item).to_have_class("completed")
    expect(todo_page.locator(".todo-count")).to_contain_text("1")

    active_filter = todo_page.get_by_role("link", name="Active", exact=True)
    # Active 视图应只保留未完成的 Active item。
    active_filter.click()
    expect(active_filter).to_have_class("selected")
    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text(["Active item"])

    completed_filter = todo_page.get_by_role(
        "link", name="Completed", exact=True
    )
    # Completed 视图应只保留完成后的 Completed item。
    completed_filter.click()
    expect(completed_filter).to_have_class("selected")
    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text(["Completed item"])

    all_filter = todo_page.get_by_role("link", name="All", exact=True)
    # 返回 All 后才能验证后续删除操作面对完整集合。
    all_filter.click()
    expect(all_filter).to_have_class("selected")
    expect(todo_items).to_have_count(2)

    completed_item.hover()
    # 删除按钮只有在 Todo hover 后才可见，因此先触发用户交互状态。
    completed_item.get_by_role("button").click()

    # 最终验证目标消失、Active 保留且业务计数没有被误改。
    expect(completed_item).to_have_count(0)
    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text(["Active item"])
    expect(todo_page.locator(".todo-count")).to_contain_text("1")
