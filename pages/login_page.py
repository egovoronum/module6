import allure

from playwright.sync_api import Page
from pages.base_page import BasePage

# https://dev-cinescope.coconutqa.ru/login

class CinescopeLoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.url = f"{self.home_url}login"
        self.email_input = '[data-qa-id="login_email_input"]'
        self.password_input = '[data-qa-id="login_password_input"]'
        self.login_button = '[data-qa-id="login_submit_button"]'

    with allure.step("Открытие страницы CinescopeLoginPage"):
        def open(self):
            self.open_url(self.url)

    with allure.step("Ввод данных логина и клик по submit"):
        def login(
            self,
            email: str,
            password: str
         ):

            self.enter_text(self.email_input, email)
            self.enter_text(self.password_input, password)
            self.click(self.login_button)