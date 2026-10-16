import allure

from playwright.sync_api import Page, expect
from pages.base_page import BasePage

# https://dev-cinescope.coconutqa.ru/login

LOGIN_SUCCESS_LOCATOR = "Профиль"

class CinescopeLoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.url = f"{self.home_url}login"
        self.email_input = '[data-qa-id="login_email_input"]'
        self.password_input = '[data-qa-id="login_password_input"]'
        self.login_button = '[data-qa-id="login_submit_button"]'

    @allure.step("Открытие страницы CinescopeLoginPage")
    def open(self) -> None:
        self.open_url(self.url)

    @allure.step("Ввод данных логина и клик по submit")
    def login(
        self,
        email: str,
        password: str
     ) -> None:

        with allure.step(
                f"""
                Вводим поля:
                Email: {self.email_input}
                Password: {self.password_input}
                """
        ):
            self.enter_text(self.email_input, email)
            self.enter_text(self.password_input, password)

        with allure.step("Клик по кнопке логина"):
            self.click(self.login_button)

    @allure.step("Временный воркараунд бага с логином")
    def login_bug_workaround(self, timeout:int = 1000) -> None:

        with allure.step(f"Ждем {timeout / 100} сек."):
            self.page.wait_for_timeout(timeout)

        with allure.step("Перезагружаем страницу"):
            self.page.reload(wait_until="networkidle")

    @allure.step("Проверка на успешный логин")
    def check_login_is_successful(self) -> None:
        with allure.step(f"Подтверждение перехода на {self.home_url}"):
            expect(self.page).to_have_url(f"{self.home_url}")

        with allure.step(f"Проверка присутствия локатора: {LOGIN_SUCCESS_LOCATOR}"):
            expect(
                self.page.get_by_role("button", name=f"{LOGIN_SUCCESS_LOCATOR}")
            ).to_be_visible()
