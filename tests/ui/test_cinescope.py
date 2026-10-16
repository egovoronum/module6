import pytest
from playwright.sync_api import Page, expect
from faker import Faker

fake = Faker()

@pytest.mark.skip
@pytest.mark.UI
def test_text_box(page: Page) -> None:

    name = fake.name()
    email = fake.email()
    password = fake.password(length=12, special_chars=False, digits=True, upper_case=True, lower_case=True)
    
    page.goto('https://dev-cinescope.coconutqa.ru/register', wait_until='networkidle')
    page.locator('[data-qa-id="register_full_name_input"]').fill(name)
    page.locator('[data-qa-id="register_email_input"]').fill(email)
    page.locator('[data-qa-id="register_password_input"]').fill(password)
    page.locator('[data-qa-id="register_password_repeat_input"]').fill(password)
    page.click('[data-qa-id="register_submit_button"]')
    page.wait_for_url('https://dev-cinescope.coconutqa.ru/login')



    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)

