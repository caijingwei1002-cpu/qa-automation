import pytest
from playwright.sync_api import Page, expect
from helpers import add_todo

pytestmark = pytest.mark.regression
# 参数化把多组输入集中管理，测试逻辑仍保持一份。


@pytest.mark.parametrize(
    "todo_text",
    ["Buy milk", "Learn pytest", "Write parameterized test"],
)
def test_create_todo_for_each_input(todo_page: Page, todo_text: str):
    # 每个参数代表一个独立输入场景，断言统一验证创建结果。
    todo_items = todo_page.locator(".todo-list").get_by_role("listitem")
    add_todo(todo_page, todo_text)

    expect(todo_items).to_have_count(1)
    expect(todo_items).to_have_text([todo_text])
