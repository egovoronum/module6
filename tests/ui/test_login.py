import pytest
import allure
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
    def test_login_page(
        self,
        login_page: CinescopeLoginPage,
        page: Page,
        common_user: User
    ) -> None:

        with allure.step("""
            Передаем имейл и пароль из common_user в переменные
            """):
            email = common_user.email
            password = common_user.password

        with allure.step("Ввод данных для логина"):
            login_page.login(email, password)

        with allure.step("Задаем success/error параметры"):
            success = page.get_by_text("Успешный вход")
            error = page.get_by_text("Что-то пошло не так")

        with allure.step("Проверяем страницу на ошибку 'Что-то пошло не так'"):
            if error.is_visible():
                raise AssertionError("Логин не сработал")

        with allure.step("Проверяем видимость 'Успешный вход'"):
            expect(success).to_be_visible()