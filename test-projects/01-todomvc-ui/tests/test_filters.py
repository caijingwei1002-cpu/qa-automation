from playwright.sync_api import Page, expect


def test_filter_todos(todo_page: Page):
    todo_input = todo_page.get_by_placeholder("What needs to be done?")

    for todo_text in ["Buy milk", "Learn pytest"]:
        todo_input.fill(todo_text)
        todo_input.press("Enter")

    todo_items = todo_page.locator(".todo-list li")
    todo_labels = todo_items.locator("label")

    expect(todo_items).to_have_count(2)
    expect(todo_labels).to_have_text(["Buy milk", "Learn pytest"])

    completed_todo = todo_items.filter(has_text="Learn pytest")
    completed_toggle = completed_todo.locator(".toggle")
    completed_toggle.check()

    expect(completed_toggle).to_be_checked()
    expect(completed_todo).to_have_class("completed")

    all_filter = todo_page.get_by_role("link", name="All", exact=True)
    all_filter.click()

    expect(all_filter).to_have_class("selected")
    expect(todo_items).to_have_count(2)
    expect(todo_labels).to_have_text(["Buy milk", "Learn pytest"])

    active_filter = todo_page.get_by_role("link", name="Active", exact=True)
    active_filter.click()

    expect(active_filter).to_have_class("selected")
    expect(todo_items).to_have_count(1)
    expect(todo_labels).to_have_text(["Buy milk"])

    completed_filter = todo_page.get_by_role(
        "link", name="Completed", exact=True
    )
    completed_filter.click()

    expect(completed_filter).to_have_class("selected")
    expect(todo_items).to_have_count(1)
    expect(todo_labels).to_have_text(["Learn pytest"])