import pytest
import random
from playwright.sync_api import Page, expect
import time
from faker import Faker 

fake = Faker()

@pytest.mark.UI
def test_text_box(page: Page):

    name = fake.name()
    email = fake.email()
    password = fake.password()
    
    page.goto('https://dev-cinescope.coconutqa.ru/register', wait_until='domcontentloaded')
    page.locator('[data-qa-id="register_full_name_input"]').fill(name)
    page.locator('[data-qa-id="register_email_input"]').fill(email)
    page.locator('[data-qa-id="register_password_input"]').fill(password)
    page.locator('[data-qa-id="register_password_repeat_input"]').fill(password)
    page.click('[data-qa-id="register_submit_button"]')


    time.sleep(5)


# expect(page.locator('#output #name')).to_have_text('Name:John Doe')
# expect(page.locator('#output #email')).to_have_text('Email:john.doe@email.com')
# expect(page.locator('#output #currentAddress')).to_have_text('Current Address :WD17 4BQ, Watford')

# // Full Name input
# const fullName = page.locator('[data-qa-id="register_full_name_input"]');

# // Email input
# const email = page.locator('[data-qa-id="register_email_input"]');

# // Password input
# const password = page.locator('[data-qa-id="register_password_input"]');

# // Password Repeat input
# const passwordRepeat = page.locator('[data-qa-id="register_password_repeat_input"]');

# // Submit button
# const submitButton = page.locator('[data-qa-id="register_submit_button"]');