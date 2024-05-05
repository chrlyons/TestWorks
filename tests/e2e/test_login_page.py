import pytest
from playwright.sync_api import sync_playwright, Locator, Browser, expect


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

    def click_login(self, expect_routing=True):
        if expect_routing:
            with self.page.expect_request("**/login**") as login_req:
                with self.page.expect_response("**/login**") as login_res:
                    self.login_button.click()
        else:
            self.login_button.click()

    def get_welcome_message_text(self):
        return self.welcome_message.text_content()

    def get_error_message_text(self):
        return self.error_message.text_content()

    def is_email_input_present(self):
        return self.email_input.is_visible()

    def is_password_input_present(self):
        return self.password_input.is_visible()


@pytest.mark.e2e
class TestLoginPage:
    @pytest.fixture(scope="function")
    def browser(self) -> Browser:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            yield browser
            browser.close()

    @pytest.fixture(scope="function")
    def login_page(self, browser) -> LoginPage:
        page = browser.new_page()
        page.goto("http://localhost")  # TODO: Switch with env variable
        yield LoginPage(page)
        page.close()

    def test_successful_login(self, login_page):
        login_page.fill_email('test@example.com')
        login_page.fill_password('validpassword')
        login_page.click_login()

        expect(login_page.welcome_message).to_be_visible()
        expect(login_page.welcome_message).to_have_text("Welcome! You are logged in.")

    def test_invalid_password(self, login_page):
        login_page.fill_email('test@example.com')
        login_page.fill_password('password')
        login_page.click_login()

        expect(login_page.error_message).to_be_visible()
        expect(login_page.error_message).to_contain_text("Password cannot be 'password'")

    def test_invalid_email(self, login_page):
        login_page.fill_email('invalid-email')
        login_page.fill_password('validpassword')
        login_page.click_login(expect_routing=False)

        expect(login_page.email_input).to_be_visible()
        expect(login_page.password_input).to_be_visible()
