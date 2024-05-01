import pytest
from playwright.sync_api import sync_playwright, Locator, Browser, Page


class LoginPage:
    def __init__(self, page):
        self.page = page

    @property
    def email_input(self) -> Locator:
        return self.page.get_by_test_id('email-input')

    @property
    def password_input(self) -> Locator:
        return self.page.get_by_test_id('password-input')

    @property
    def login_button(self) -> Locator:
        return self.page.get_by_test_id('login-button')

    @property
    def welcome_message(self) -> Locator:
        return self.page.get_by_test_id('welcome-message')

    @property
    def error_message(self) -> Locator:
        return self.page.get_by_test_id('error-message')

    def fill_email(self, email):
        self.email_input.fill(email)

    def fill_password(self, password):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

    def get_welcome_message_text(self):
        return self.welcome_message.text_content()

    def get_error_message_text(self):
        return self.error_message.text_content()

    def is_email_input_present(self):
        return self.email_input.is_visible()

    def is_password_input_present(self):
        return self.password_input.is_visible()


@pytest.fixture(scope="function")
def browser() -> Browser:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def login_page(browser) -> LoginPage(Page):
    page = browser.new_page()
    page.goto("http://localhost:3000")
    yield LoginPage(page)
    page.close()


@pytest.mark.integration
def test_successful_login(login_page):
    login_page.fill_email('test@example.com')
    login_page.fill_password('validpassword')
    login_page.click_login()

    assert login_page.welcome_message.is_visible()
    assert login_page.get_welcome_message_text() == "Welcome! You are logged in."


@pytest.mark.integration
def test_invalid_password(login_page):
    login_page.fill_email('test@example.com')
    login_page.fill_password('password')
    login_page.click_login()

    assert login_page.error_message.is_visible()
    assert login_page.get_error_message_text() == 'Password cannot be "password"'


@pytest.mark.integration
def test_invalid_email(login_page):
    login_page.fill_email('invalid-email')
    login_page.fill_password('validpassword')
    login_page.click_login()

    assert login_page.is_email_input_present(), "Email input field is missing"
    assert login_page.is_password_input_present(), "Password input field is missing"
