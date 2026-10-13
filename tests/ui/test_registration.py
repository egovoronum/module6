from playwright.sync_api import Page, expect
from pages.register_page import CinescopeRegisterPage
from faker import Faker
import time

fake = Faker()

class TestRegistration:

    def test_registration(
        self,
        register_page: CinescopeRegisterPage,
        page: Page
    ) -> None:

        name = fake.name()
        email = fake.email()
        password = fake.password(
            length=24,
            special_chars=False,
            digits=True,
            upper_case=True,
            lower_case=True
        )

        register_page.register(name, email, password)

        time.sleep(5)

        expect(page.get_by_text("Подтвердите свою почту")).to_be_visible()
