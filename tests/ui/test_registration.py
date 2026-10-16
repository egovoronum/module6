import allure
import pytest

from playwright.sync_api import Page, expect
from models.base_models import CreateUserData
from pages.register_page import CinescopeRegisterPage


@allure.epic("UI-тесты")
@allure.description("""
    Проверяет корректную работу UI /register
    """)
@allure.story("Успешная регистрация")
@allure.feature("Регистрация пользователей")
@pytest.mark.UI
@pytest.mark.regression
class TestRegistration:

    @allure.title("UI-тест страницы регистрации [{browser_name}]")
    def test_registration(
        self,
        register_page: CinescopeRegisterPage,
        page: Page,
        oneshot_user: CreateUserData
    ) -> None:

        register_page.register(
            oneshot_user.fullName,
            oneshot_user.email,
            oneshot_user.password
        )

        register_page.check_registration_is_successful()
