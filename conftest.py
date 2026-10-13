import re
import pytest
import time
from utils.logger import get_logger
from playwright.async_api import Page
from pages.register_page import CinescopeRegisterPage

DEFAULT_UI_TIMEOUT = 30000
logger = get_logger(__name__)

PROXY_CONFIG = {
    "server": "socks5://127.0.0.1:10808"
}

@pytest.fixture(scope="function")
def register_page(page: Page) -> CinescopeRegisterPage:
    register_page = CinescopeRegisterPage(page)
    register_page.open()

    time.sleep(1)

    return register_page


@pytest.fixture(scope="session")
def browser(playwright):
    logger.info("поднимаем браузер")
    browser = playwright.chromium.launch(
        headless=False,
        args=['--force-dark-mode', '--window-size=800,600'],
        # proxy=PROXY_CONFIG
    )
    
    # docker container on rpi400
    # browser = playwright.chromium.connect("ws://192.168.1.151:3000/")

    yield browser

    logger.info("закрываем браузер")
    browser.close()


@pytest.fixture(scope="function")
def context(browser, request):
    context = browser.new_context(
        viewport={'width': 800, 'height': 600},
        color_scheme='dark'
    )
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context

    name = re.sub(r"[^\w.-]", "_", request.node.name)
    context.tracing.stop(path=f"traces/{name}.zip")
    logger.info("контекст опускается")
    context.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()

    yield page

    logger.info("страница опускается")
    page.close()