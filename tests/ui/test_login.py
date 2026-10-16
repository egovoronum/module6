import pytest
import allure
import time
from playwright.sync_api import Page, expect

from conftest import common_user
from entities.user import User
from pages.login_page import CinescopeLoginPage


@allure.epic("UI-тесты")
@allure.description("""
    Проверяет корректную работу UI /login 
    """)
@pytest.mark.UI
class TestLogin:

    @allure.title("Проверка страницы логина {browser_name}")
    def test_login_page(
        self,
        login_page: CinescopeLoginPage,
        page: Page,
        common_user: User
    ) -> None:

        email = common_user.email
        password = common_user.password

        login_page.login(email, password)

        time.sleep(1)
        page.reload(wait_until="networkidle")

        success = page.get_by_role("button", name="Профиль")
        error = page.get_by_text("Что-то пошло не так")

        if error.is_visible():
            raise AssertionError("Логин не сработал, измени time.sleep() перед page.reload()")

        expect(success).to_be_visible()