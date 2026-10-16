# ─── стандартные библиотеки ──────────────────────────────────────────────────
import os

# ─── доп библиотеки ──────────────────────────────────────────────────────────
import allure
import requests
from dotenv import load_dotenv
from faker import Faker
from typing import Generator

# ─── модули проекта ──────────────────────────────────────────────────────────
from utils.data_generator import DataGenerator
from clients.api_manager import ApiManager
from entities.user import User
from enums.roles import Roles
from models.base_models import CreateUserData

# ─── UI test imports──────────────────────────────────────────────────────────
import re
import pytest
import time
from utils.logger import get_logger
from playwright.async_api import Page
from pages.register_page import CinescopeRegisterPage
from pages.login_page import CinescopeLoginPage

# ─── init─────────────────────────────────────────────────────────────────────
fake = Faker("ru_RU")
load_dotenv()
DEFAULT_UI_TIMEOUT = 30000
logger = get_logger(__name__)

PROXY_CONFIG = {
    "server": "socks5://192.168.1.151:10808"
}

def env_check(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(
            f"Required environment variable '{name}' is missing")
    return value


ADMIN_EMAIL = env_check("ADMIN_EMAIL")
ADMIN_PASSWORD = env_check("ADMIN_PASSWORD")


# ─── fixtures─────────────────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def login_page(page: Page) -> CinescopeLoginPage:
    login_page = CinescopeLoginPage(page)
    login_page.open()

    time.sleep(1)

    return login_page


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


@pytest.fixture(scope="function")
def oneshot_user() -> CreateUserData:
    password = fake.password(
        length=12,
        special_chars=False,
        digits=True,
        upper_case=True,
        lower_case=True
    )

    register_data = {
        "email": DataGenerator.generate_random_email(),
        "fullName": fake.name(),
        "password": password,
        "passwordRepeat": password,
    }

    model = CreateUserData.model_validate(register_data)

    return model


@pytest.fixture(scope="function")
def create_user_data(oneshot_user: CreateUserData) -> CreateUserData:
    return oneshot_user.model_copy(update={"verified": True, "banned": False})


@pytest.fixture(scope="function")
def create_admin_user_data(oneshot_user: CreateUserData) -> CreateUserData:
    return oneshot_user.model_copy(
        update={"roles": ["USER", "ADMIN"], "verified": True, "banned": False})


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture(scope="function")
def common_user(
        user_session,
        super_admin: User,
        create_user_data: CreateUserData
) -> Generator[User, None, None]:

    new_session = user_session()

    common_user = User(
        create_user_data.email,
        create_user_data.password,
        [Roles.USER],
        new_session)

    response = super_admin.api.user_api.create_user(create_user_data)

    data = response.json()
    new_common_user_id = data["id"]

    yield common_user


    with allure.step("tearing down common_user"):
        super_admin.api.user_api.delete_user(
            new_common_user_id,
            expected_status=200
        )


@pytest.fixture
def super_admin(user_session) -> User:
    new_session = user_session()

    super_admin = User(
        ADMIN_EMAIL,
        ADMIN_PASSWORD,
        [Roles.SUPER_ADMIN],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)

    return super_admin