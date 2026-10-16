import allure

from pages.base_page import BasePage
from playwright.sync_api import Page, expect

REGISTER_SUCCESS_POPUP = "Подтвердите свою почту"

class CinescopeRegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.url = f"{self.home_url}register"
        self.full_name_input = '[data-qa-id="register_full_name_input"]'
        self.email_input = '[data-qa-id="register_email_input"]'
        self.password_input = '[data-qa-id="register_password_input"]'
        self.repeat_password_input = '[data-qa-id="register_password_repeat_input"]'
        self.submit_button = '[data-qa-id="register_submit_button"]'

    @allure.step("Открытие страницы регистрации")
    def open(self) -> None:
        with allure.step(f"Переход по {self.url}"):
            self.open_url(self.url)

    @allure.step("Ввод данных регистрации и клик по submit")
    def register(
        self,
        full_name: str,
        email: str,
        password: str
    ) -> None:

        with allure.step(
            f"Заполнение - Имя: {self.full_name_input} Имейл: {self.email_input}"
        ):
            self.enter_text(self.full_name_input, full_name)
            self.enter_text(self.email_input, email)
            self.enter_text(self.password_input, password)
            self.enter_text(self.repeat_password_input, password)

        with allure.step("Клик по кнопке регистрации"):
            self.click(self.submit_button)

    @allure.step("Проверка видимости поля 'подтвердите свою почту'")
    def check_registration_is_successful(self):
        with allure.step(f"Отображается сообщение: {REGISTER_SUCCESS_POPUP}"):
            expect(
                self.page.get_by_text(f"{REGISTER_SUCCESS_POPUP}")
            ).to_be_visible()