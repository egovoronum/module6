import allure
import pytest

from playwright.sync_api import Page, expect
from entities.user import User
from pages.movies_page import CinescopeMoviesPage
from models.base_models import Movie, CreateReviewData


@allure.epic("UI-тесты")
@allure.description("""
    Проверяет корректную работу отзывов 
    """)
@pytest.mark.UI
class TestReview:

    @allure.title("Проверка страницы ревью {browser_name}")
    def test_review(
        self,
        movies_page: CinescopeMoviesPage,
        page: Page,
        common_user: User,
        generate_review: CreateReviewData,
        oneshot_movie: Movie
    ) -> None:

        movies_page.open_movie(oneshot_movie.id)

        expect(
            page.locator('[data-qa-id="movie_review_input"]')
        ).to_be_visible()

        page.locator(
            '[data-qa-id="movie_review_input"]').type(
            f"{generate_review.text}",
            delay=50
        )

        page.locator('[data-qa-id="movie_review_submit_button"]').click()

        expect(page.get_by_text("Отзыв успешно создан")).to_be_visible()

