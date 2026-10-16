import allure

from models.base_models import CreateReviewData, Movie
from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class CinescopeMoviesPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.url = f"{self.home_url}movies"
        self.email_input = '[data-qa-id="login_email_input"]'
        self.password_input = '[data-qa-id="login_password_input"]'
        self.login_button = '[data-qa-id="login_submit_button"]'

    @allure.step("Открытие страницы /movies")
    def open(self):
        self.open_url(self.url)


    @allure.step("Ввод данных логина и клик по submit")
    def login(self, email: str, password: str) -> None:

        self.open_url(f"{self.home_url}login")
        self.enter_text(self.email_input, email)
        self.enter_text(self.password_input, password)
        self.click(self.login_button)


    @allure.step("Открытие страницы фильма")
    def open_movie(self, movie_id) -> None:
        self.open_url(f"{self.url}/{movie_id}")


    @allure.step("Размещение обзора")
    def submit_review(
        self,
        review: CreateReviewData
    ) -> None:

        self.page.locator(
            '[data-qa-id="movie_review_input"]').type(
            f"{review.text}",
            delay=50
        )

        self.page.locator('[data-qa-id="movie_review_submit_button"]').click()

    @allure.step("Проверка на успешное размещение обзора")
    def check_review_is_posted(self) -> None:
        expect(self.page.get_by_text("Отзыв успешно создан")).to_be_visible()