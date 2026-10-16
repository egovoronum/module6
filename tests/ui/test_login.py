import pytest
import allure
from playwright.sync_api import Page, expect

from conftest import common_user
from entities.user import User
from pages.login_page import CinescopeLoginPage


@allure.epic("UI-тесты")
@allure.story("Успешная аутентификация")
@allure.feature("Аутентификация пользователей")
@allure.description("Тест проверяет корректную работу UI /login")
@pytest.mark.ui
@pytest.mark.regression
class TestLogin:
    @allure.title("Проверка страницы логина {browser_name}")
    def test_login_page(
        self,
        login_page: CinescopeLoginPage,
        page: Page,
        common_user: User
    ) -> None:

        login_page.login(common_user.email, common_user.password)
        login_page.login_bug_workaround()
        login_page.check_login_is_successful()

