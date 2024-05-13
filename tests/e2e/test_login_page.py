import pytest
from playwright.sync_api import Locator, expect


class LoginPage:
    def __init__(self, page):
        self.page = page

    @property
    def email_input(self) -> Locator:
        return self.page.get_by_test_id("email-input")

    @property
    def password_input(self) -> Locator:
        return self.page.get_by_test_id("password-input")

    @property
    def login_button(self) -> Locator:
        return self.page.get_by_test_id("login-button")

    @property
    def welcome_message(self) -> Locator:
        return self.page.get_by_test_id("welcome-message")

    @property
    def error_message(self) -> Locator:
        return self.page.get_by_test_id("error-message")

    @property
    def logout_button(self) -> Locator:
        return self.page.get_by_test_id("logout-button")

    def fill_email(self, email):
        self.email_input.fill(email)

    def fill_password(self, password):
        self.password_input.fill(password)

    def click_login(self, expect_routing=True):
        if expect_routing:
            with self.page.expect_request("**/login**"):
                with self.page.expect_response("**/login**"):
                    self.login_button.click()
        else:
            self.login_button.click()

    def click_logout(self):
        self.logout_button.click()


@pytest.mark.e2e
class TestLoginPage:

    def test_successful_login(self, login_page):
        login_page.fill_email("test@example.com")
        login_page.fill_password("validpassword")
        login_page.click_login()

        expect(login_page.welcome_message).to_be_visible()
        expect(login_page.welcome_message).to_have_text("Welcome! You are logged in.")

    def test_invalid_password(self, login_page):
        login_page.fill_email("test@example.com")
        login_page.fill_password("password")
        login_page.click_login()

        expect(login_page.error_message).to_be_visible()
        expect(login_page.error_message).to_contain_text(
            "Password cannot be 'password'"
        )

    def test_invalid_email(self, login_page):
        login_page.fill_email("invalid-email")
        login_page.fill_password("validpassword")
        login_page.click_login(expect_routing=False)

        expect(login_page.email_input).to_be_visible()
        expect(login_page.password_input).to_be_visible()

    def test_no_password(self, login_page):
        login_page.fill_email("test@example.com")
        login_page.fill_password("")
        login_page.click_login(expect_routing=False)

        expect(login_page.login_button).to_be_visible()

    def test_no_email(self, login_page):
        login_page.fill_password("validpassword")
        login_page.click_login(expect_routing=False)

        expect(login_page.email_input).to_be_visible()
        expect(login_page.password_input).to_be_visible()

    def test_logout(self, valid_user_login):
        valid_user_login.click_logout()

        expect(valid_user_login.login_button).to_be_visible()


@pytest.mark.e2e
def test_user_flow(login_page):
    login_page.fill_email("test@example.com")
    login_page.fill_password("validpassword")
    login_page.click_login()

    expect(login_page.welcome_message).to_be_visible()
    expect(login_page.welcome_message).to_have_text("Welcome! You are logged in.")

    login_page.click_logout()
    expect(login_page.login_button).to_be_visible()
