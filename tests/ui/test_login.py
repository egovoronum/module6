import pytest
import allure
import time
from playwright.sync_api import Page, expect

from conftest import common_user
from entities.user import User
from pages.login_page import CinescopeLoginPage


@allure.epic("UI-тесты")
@allure.story("Успешная аутентификация")
@allure.feature("Аутентификация пользователей")
@allure.description("Тест проверяет корректную работу UI /login")
@pytest.mark.UI
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

        time.sleep(1) # временный костыль из-за бага
        page.reload(wait_until="networkidle") # временный костыль из-за бага

        expect(page).to_have_url("https://dev-cinescope.coconutqa.ru/")
        expect(page.get_by_role("button", name="Профиль")).to_be_visible()
