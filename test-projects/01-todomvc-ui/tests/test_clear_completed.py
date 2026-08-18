import pytest
from playwright.sync_api import Page, expect


pytestmark = pytest.mark.regression
# 该场景验证批量清理后的业务结果，属于完整回归而非最小 smoke。


def test_clear_completed_todos(todo_page_with_todos: Page):
    # fixture 先准备两条 Active Todo，测试再把其中一条转换为 Completed。
    todo_items = todo_page_with_todos.locator(".todo-list").get_by_role("listitem")

    # 先确认前置数据正确，避免把准备失败误判成清理功能失败。
    expect(todo_items).to_have_count(2)
    expect(todo_items).to_have_text(["Buy milk", "Learn pytest"])

    completed_item = todo_items.filter(has_text="Learn pytest")
    completed_toggle = completed_item.get_by_role("checkbox")
    completed_toggle.check()

    # 确认目标项确实进入 Completed 状态，未完成计数同步减少。
    expect(completed_toggle).to_be_checked()
    expect(completed_item).to_have_class("completed")
    expect(todo_page_with_todos.locator(".todo-count")).to_contain_text("1")

    clear_completed = todo_page_with_todos.get_by_role(
        "button", name="Clear completed", exact=True
    )
    # 按用户可见名称定位批量清理操作，不依赖实现细节。
    clear_completed.click()

    # 清理后验证目标消失、Active 项保留、列表和业务计数一致。
    expect(completed_item).to_have_count(0)
    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text(["Buy milk"])
    expect(todo_page_with_todos.locator(".todo-count")).to_contain_text("1")
