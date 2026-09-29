import pytest
from playwright.sync_api import sync_playwright
from utils.logger import get_logger

DEFAULT_UI_TIMEOUT = 30000
logger = get_logger(__name__)

@pytest.fixture(scope="session") 
def browser(playwright):
    
    logger.info('поднимаем браузер')
    browser = playwright.chromium.launch(
        headless=True, 
        args=["--force-dark-color-scheme", "--force-dark-mode"]
    )  

    yield browser  

    logger.info('закрываем браузер')
    browser.close()  

@pytest.fixture(scope="function")
def context(browser):
    
    context = browser.new_context()
    
    context.tracing.start(
        screenshots=True, 
        snapshots=True, 
        sources=True
    )
    
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)

    yield context

    logger.info("контекст опускается")
    context.close()

@pytest.fixture(scope="function")
def page(context):
    
    page = context.new_page()

    yield page

    logger.info("страница опускается")
    page.close()
