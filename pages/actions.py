import allure
from playwright.sync_api import Page

class PageAction:
    def __init__(self, page: Page):
        self.page = page

    @allure.step(f"Переход на страницу")
    def open_url(self, url: str):
        with allure.step(f"Переход на {url}"):
            self.page.goto(url, wait_until='domcontentloaded')

    @allure.step("Ввод текста в поле")
    def enter_text(self, locator: str, text: str):
        with allure.step(f"Заполнение поля {locator}"):
            self.page.type(locator, text, delay=50)

    @allure.step("Клик по элементу")
    def click(self, locator: str):
        with allure.step(f"Клик по элементу {locator}"):
            self.page.click(locator)
