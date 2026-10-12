import allure
import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.cart

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"
BOLT_TSHIRT = "Sauce Labs Bolt T-Shirt"


@allure.feature("Carrinho")
class TestCart:
    @allure.title("Adicionar um produto ao carrinho")
    def test_adicionar_um_produto(self, inventory_page, cart_page):
        inventory_page.add_to_cart(BACKPACK)
        inventory_page.open_cart()

        expect(cart_page.item_names).to_have_text([BACKPACK])

    @allure.title("Adicionar múltiplos produtos ao carrinho")
    def test_adicionar_multiplos_produtos(self, inventory_page, cart_page):
        produtos = [BACKPACK, BIKE_LIGHT, BOLT_TSHIRT]
        for produto in produtos:
            inventory_page.add_to_cart(produto)
        inventory_page.open_cart()

        expect(cart_page.item_names).to_have_text(produtos)

    @allure.title("Remover produto do carrinho")
    def test_remover_produto(self, inventory_page, cart_page):
        inventory_page.add_to_cart(BACKPACK)
        inventory_page.add_to_cart(BIKE_LIGHT)
        inventory_page.open_cart()

        cart_page.remove(BACKPACK)

        expect(cart_page.item_names).to_have_text([BIKE_LIGHT])
        expect(inventory_page.cart_badge).to_have_text("1")

    @allure.title("Verificar contador do carrinho")
    def test_contador_do_carrinho(self, inventory_page):
        expect(inventory_page.cart_badge).to_be_hidden()

        inventory_page.add_to_cart(BACKPACK)
        expect(inventory_page.cart_badge).to_have_text("1")

        inventory_page.add_to_cart(BIKE_LIGHT)
        expect(inventory_page.cart_badge).to_have_text("2")

        inventory_page.remove_from_cart(BACKPACK)
        expect(inventory_page.cart_badge).to_have_text("1")

        inventory_page.remove_from_cart(BIKE_LIGHT)
        expect(inventory_page.cart_badge).to_be_hidden()
