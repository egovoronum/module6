import allure
import pytest

from playwright.sync_api import Page, expect
from entities.user import User
from pages.movies_page import CinescopeMoviesPage
from models.base_models import Movie, CreateReviewData


@allure.epic("UI-тесты")
@allure.story("Успешное размещение обзора на фильм")
@allure.feature("Размещение обзора")
@allure.description("""
    Проверяет корректную работу отзывов 
    """)
@pytest.mark.UI
@pytest.mark.regression
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
        movies_page.submit_review(generate_review)
        movies_page.check_review_is_posted()

