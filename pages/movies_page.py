import allure

from pages.base_page import BasePage
from playwright.sync_api import Page


class CinescopeMoviesPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.url = f"{self.home_url}movies"
        self.email_input = '[data-qa-id="login_email_input"]'
        self.password_input = '[data-qa-id="login_password_input"]'
        self.login_button = '[data-qa-id="login_submit_button"]'

    with allure.step("Открытие страницы /movies"):
        def open(self):
            self.open_url(self.url)

    with allure.step("Аутентификация пользователя"):
        with allure.step("Ввод данных логина и клик по submit"):
            def login(
                    self,
                    email: str,
                    password: str
            ):

                self.open_url(f"{self.home_url}login")
                self.enter_text(self.email_input, email)
                self.enter_text(self.password_input, password)
                self.click(self.login_button)

    with allure.step("Открытие страницы фильма"):
        def open_movie(self, movie_id):
            self.open_url(f"{self.url}/{movie_id}")

