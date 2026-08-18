"""Day 8 locator rules.

Prefer role, label, and placeholder for user-facing elements.
Use text only when it is unique or scoped to a business object.
Use CSS mainly for structural containers or missing semantic hooks.
"""

from playwright.sync_api import Page, expect
import pytest
from helpers import add_todo

pytestmark = pytest.mark.regression


def test_prefer_semantic_locators(todo_page: Page):
    # 先创建一个有明确业务文本的 Todo，方便验证作用域和语义定位。
    add_todo(todo_page, "Stable locator")
    # CSS 只用于稳定的列表容器，业务对象和控件优先使用 role/text。
    todo_item = (
        todo_page.locator(".todo-list")
        .get_by_role("listitem")
        .filter(has_text="Stable locator")
    )

    expect(todo_item).to_have_count(1)
    expect(todo_item).to_contain_text("Stable locator")
    # checkbox 的数量和可见性证明定位到了目标 Todo 内的真实控件。
    expect(todo_item.get_by_role("checkbox")).to_have_count(1)
    expect(todo_item.get_by_role("checkbox")).to_be_visible()
