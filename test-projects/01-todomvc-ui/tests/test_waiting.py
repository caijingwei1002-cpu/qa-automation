import pytest
from playwright.sync_api import Page, expect
from helpers import add_todo

pytestmark = pytest.mark.regression
# 该测试专门验证状态等待，不使用固定 sleep。


def test_todo_creation_waits_for_list_state(todo_page: Page):
    # expect 会等待列表和计数达到目标状态，避免读取过早造成 flaky。
    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")
    add_todo(todo_page, "Wait for state")

    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text(["Wait for state"])
    expect(todo_page.locator(".todo-count")).to_contain_text("1")
