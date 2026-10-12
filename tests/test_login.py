import allure
import pytest
from playwright.sync_api import expect

from conftest import LOCKED_USER, PASSWORD, STANDARD_USER
from pages import InventoryPage

pytestmark = pytest.mark.login


@allure.feature("Login")
class TestLogin:
    @allure.title("Login com credenciais válidas")
    def test_login_valido(self, login_page):
        login_page.login(STANDARD_USER, PASSWORD)

        expect(login_page.page).to_have_url("/inventory.html")
        expect(InventoryPage(login_page.page).title).to_have_text("Products")

    @allure.title("Login com usuário bloqueado")
    def test_login_usuario_bloqueado(self, login_page):
        login_page.login(LOCKED_USER, PASSWORD)

        expect(login_page.error_message).to_have_text(
            "Epic sadface: Sorry, this user has been locked out."
        )

    @allure.title("Login com senha incorreta")
    def test_login_senha_incorreta(self, login_page):
        login_page.login(STANDARD_USER, "senha_errada")

        expect(login_page.error_message).to_have_text(
            "Epic sadface: Username and password do not match any user in this service"
        )

    @allure.title("Login com campos vazios")
    def test_login_campos_vazios(self, login_page):
        login_page.login("", "")

        expect(login_page.error_message).to_have_text(
            "Epic sadface: Username is required"
        )
