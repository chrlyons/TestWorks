import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    page.goto("http://localhost:3000")
    yield page
    page.close()


def test_successful_login(page):
    # Fill in the login form
    page.fill('data-testid=email-input', 'test@example.com')
    page.fill('data-testid=password-input', 'validpassword')
    page.click('data-testid=login-button')

    # Assert that the welcome message is displayed
    welcome_message = page.query_selector('data-testid=welcome-message')
    assert welcome_message is not None
    assert welcome_message.text_content() == "Welcome! You are logged in."


def test_invalid_password(page):
    # Fill in the login form with an invalid password
    page.fill('data-testid=email-input', 'test@example.com')
    page.fill('data-testid=password-input', 'password')
    page.click('data-testid=login-button')

    # Assert that the error message is displayed
    error_message = page.query_selector('data-testid=error-message')
    assert error_message is not None
    assert error_message.text_content() == 'Password cannot be "password"'


def test_invalid_email(page):
    # Fill in the login form with an invalid email
    page.fill('data-testid=email-input', 'invalid-email')
    page.fill('data-testid=password-input', 'validpassword')
    page.click('data-testid=login-button')

    # Assert that the email field is still present
    email_input = page.query_selector('data-testid=email-input')
    assert email_input is not None, "Email input field is missing"

    # Assert that the password field is still present
    password_input = page.query_selector('data-testid=password-input')
    assert password_input is not None, "Password input field is missing"
