import re
import pytest
from utils.logger import get_logger

DEFAULT_UI_TIMEOUT = 30000
logger = get_logger(__name__)


@pytest.fixture(scope="session")
def browser(playwright):
    logger.info("поднимаем браузер")
    browser = playwright.chromium.launch(
        headless=False,
        args=['--force-dark-mode', '--window-size=1400,900']
    )
    
    # docker container on rpi400
    # browser = playwright.chromium.connect("ws://192.168.1.151:3000/")

    yield browser

    logger.info("закрываем браузер")
    browser.close()


@pytest.fixture(scope="function")
def context(browser, request):
    context = browser.new_context(
        viewport={'width': 1400, 'height': 900},
        color_scheme='dark',
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