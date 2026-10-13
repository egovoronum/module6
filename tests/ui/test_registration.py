import time

from playwright.sync_api import Page, expect
from pages.register_page import CinescopeRegisterPage
from faker import Faker 

fake = Faker()

def test_registration(page: Page):
    
    name = fake.name()
    email = fake.email()
    password = fake.password(
        length=12, 
        special_chars=False, 
        digits=True, 
        upper_case=True, 
        lower_case=True
    )

    register_page = CinescopeRegisterPage(page)

    register_page.open()
    register_page.register(name, email, password)

    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible()

    time.sleep(2)