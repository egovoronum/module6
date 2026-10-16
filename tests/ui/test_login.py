from playwright.sync_api import Page, expect

from conftest import common_user
from entities.user import User
from pages.login_page import CinescopeLoginPage
from faker import Faker

fake = Faker('en_US')

class TestLogin:

    def test_login_page(
        self,
        login_page: CinescopeLoginPage,
        page: Page,
        common_user: User
    ) -> None:

        email = common_user.email
        password = common_user.password

        login_page.login(email, password)

        expect(page.get_by_text("Успешный вход")).to_be_visible()
