import pytest
from playwright.sync_api import sync_playwright, Browser
from e2e.test_login_page import LoginPage


@pytest.fixture(scope="function")
def browser() -> Browser:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def login_page(browser) -> LoginPage:
    page = browser.new_page()
    page.goto("http://localhost")  # TODO: Switch with env variable
    yield LoginPage(page)
    page.close()


@pytest.fixture(scope="function")
def valid_user_login(login_page):
    login_page.fill_email("test@example.com")
    login_page.fill_password("validpassword")
    login_page.click_login()
    yield login_page
