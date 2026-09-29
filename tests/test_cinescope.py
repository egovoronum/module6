import pytest
from playwright.sync_api import Page, expect
import time

@pytest.mark.UI
def test_text_box(page: Page):
    page.goto('https://dev-cinescope.coconutqa.ru/register', wait_until='domcontentloaded')
    time.sleep(1) 

    page.locator('[data-qa-id="register_full_name_input"]').fill('John Doe')
    time.sleep(1)

    page.locator('[data-qa-id="register_email_input"]').fill('john.doe@email.com')
    time.sleep(1)
    page.locator('[data-qa-id="register_password_input"]')
    time.sleep(1)
    page.locator('[data-qa-id="register_password_repeat_input"]')
    time.sleep(1)
    page.locator('[data-qa-id="register_submit_button"]')
    time.sleep(1)

    # expect(page.locator('#output #name')).to_have_text('Name:John Doe')
    # expect(page.locator('#output #email')).to_have_text('Email:john.doe@email.com')
    # expect(page.locator('#output #currentAddress')).to_have_text('Current Address :WD17 4BQ, Watford')
    time.sleep(1)
