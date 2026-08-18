import pytest
from playwright.sync_api import Page, expect
from helpers import add_todo

pytestmark = pytest.mark.regression
# 这些测试用等价类和边界值检查输入规则，不测试其他 Todo 功能。


def test_blank_todo_is_not_created(todo_page: Page):
    # 空白输入代表“无有效文本”这一拒绝等价类。
    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")
    add_todo(todo_page, "   ")

    expect(todo_items).to_have_count(0)


def test_todo_text_is_trimmed(todo_page: Page):
    # 前后空格用于验证页面是否按业务规则规范化文本。
    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")
    add_todo(todo_page, "  Buy milk  ")

    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text(["Buy milk"])


def test_duplicate_todos_are_created(todo_page: Page):
    # 重复文本应保留为两个独立 Todo，不能被错误去重。
    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")
    for _ in range(2):
        add_todo(todo_page, "Buy milk")

    expect(todo_items).to_have_count(2)
    expect(todo_items).to_have_text(["Buy milk", "Buy milk"])


def test_long_todo_text_is_preserved(todo_page: Page):
    # 256 个字符作为长文本边界，验证内容没有被截断。
    long_text = "A" * 256
    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")
    add_todo(todo_page, long_text)
    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text([long_text])
