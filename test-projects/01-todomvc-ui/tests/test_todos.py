import pytest
from playwright.sync_api import Page, expect
from helpers import add_todo


pytestmark = pytest.mark.regression
# 所有 Todo 基础行为默认进入回归；其中四条关键路径额外属于 smoke。


@pytest.mark.smoke
def test_add_todo(todo_page: Page):
    # 新增测试验证用户输入后列表和未完成计数同时更新。
    add_todo(todo_page, "Buy milk")
    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")

    expect(todo_items).to_have_count(1)
    expect(todo_items).to_contain_text("Buy milk")
    expect(todo_page.locator(".todo-count")).to_contain_text("1")


@pytest.mark.smoke
def test_complete_todo(todo_page: Page):
    # 完成测试验证 checkbox、CSS 状态和未完成计数的一致性。
    add_todo(todo_page, "Learn checkbox state")

    todo_item = todo_page.locator(".todo-list").get_by_role("listitem")
    expect(todo_item).to_have_count(1)
    expect(todo_page.locator(".todo-count")).to_contain_text("1")
    toggle = todo_item.get_by_role("checkbox")

    toggle.check()

    expect(toggle).to_be_checked()
    expect(todo_item).to_have_class("completed")
    expect(todo_page.locator(".todo-count")).to_contain_text("0")


@pytest.mark.smoke
def test_delete_todo(todo_page_with_todos: Page):
    # 删除测试验证目标 Todo 消失且其他 Todo 不受影响。
    todo_items = todo_page_with_todos.locator(".todo-list").get_by_role("listitem")

    expect(todo_items).to_have_count(2)
    expect(todo_items).to_have_text(["Buy milk", "Learn pytest"])

    target_todo = todo_items.filter(has_text="Buy milk")
    expect(target_todo).to_have_count(1)

    # 删除按钮通过 hover 后出现，模拟真实用户的删除操作。
    target_todo.hover()
    target_todo.get_by_role("button").click()

    expect(target_todo).to_have_count(0)
    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text(["Learn pytest"])
    expect(todo_page_with_todos.locator(".todo-count")).to_contain_text("1")
