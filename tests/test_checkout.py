import allure
import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.checkout

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@allure.feature("Checkout")
class TestCheckout:
    @allure.title("Fluxo completo de checkout com sucesso")
    def test_checkout_completo(self, inventory_page, cart_page, checkout_page):
        inventory_page.add_to_cart(BACKPACK)
        inventory_page.open_cart()
        cart_page.checkout()

        checkout_page.fill_information("Ivan", "Teste", "12345-678")
        checkout_page.continue_to_overview()
        checkout_page.finish()

        expect(checkout_page.page).to_have_url("/checkout-complete.html")
        expect(checkout_page.complete_header).to_have_text("Thank you for your order!")
        expect(inventory_page.cart_badge).to_be_hidden()

    @allure.title("Checkout sem preencher dados exibe erro")
    def test_checkout_sem_dados(self, inventory_page, cart_page, checkout_page):
        inventory_page.add_to_cart(BACKPACK)
        inventory_page.open_cart()
        cart_page.checkout()

        checkout_page.continue_to_overview()

        expect(checkout_page.error_message).to_have_text("Error: First Name is required")
        expect(checkout_page.page).to_have_url("/checkout-step-one.html")

    @allure.title("Verificar resumo do pedido")
    def test_resumo_do_pedido(self, inventory_page, cart_page, checkout_page):
        produtos = [BACKPACK, BIKE_LIGHT]
        precos = [inventory_page.price_of(p) for p in produtos]
        for produto in produtos:
            inventory_page.add_to_cart(produto)
        inventory_page.open_cart()
        cart_page.checkout()
        checkout_page.fill_information("Ivan", "Teste", "12345-678")
        checkout_page.continue_to_overview()

        expect(checkout_page.item_names).to_have_text(produtos)
        assert checkout_page.item_price_values() == precos
        assert checkout_page.subtotal() == pytest.approx(sum(precos))
        assert checkout_page.total() == pytest.approx(
            checkout_page.subtotal() + checkout_page.tax()
        )
