import allure
import pytest
from playwright.sync_api import Page, Playwright

from pages import CartPage, CheckoutPage, InventoryPage, LoginPage

STANDARD_USER = "standard_user"
LOCKED_USER = "locked_out_user"
PASSWORD = "secret_sauce"


@pytest.fixture(scope="session", autouse=True)
def configure_test_id(playwright: Playwright):
    # O SauceDemo usa o atributo data-test em vez de data-testid
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    login = LoginPage(page)
    login.open()
    return login


@pytest.fixture
def inventory_page(login_page: LoginPage) -> InventoryPage:
    login_page.login(STANDARD_USER, PASSWORD)
    return InventoryPage(login_page.page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            allure.attach(
                page.screenshot(full_page=True),
                name="screenshot-falha",
                attachment_type=allure.attachment_type.PNG,
            )
