import allure
from playwright.sync_api import Page


def product_slug(product_name: str) -> str:
    """'Sauce Labs Backpack' -> 'sauce-labs-backpack' (usado nos data-test dos botões)."""
    return product_name.lower().replace(" ", "-")


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.get_by_test_id("title")
        self.items = page.get_by_test_id("inventory-item")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.cart_link = page.get_by_test_id("shopping-cart-link")

    @allure.step("Adicionar '{product_name}' ao carrinho")
    def add_to_cart(self, product_name: str):
        self.page.get_by_test_id(f"add-to-cart-{product_slug(product_name)}").click()

    @allure.step("Remover '{product_name}' do carrinho")
    def remove_from_cart(self, product_name: str):
        self.page.get_by_test_id(f"remove-{product_slug(product_name)}").click()

    def price_of(self, product_name: str) -> float:
        item = self.items.filter(has_text=product_name)
        text = item.get_by_test_id("inventory-item-price").inner_text()
        return float(text.replace("$", ""))

    @allure.step("Abrir carrinho")
    def open_cart(self):
        self.cart_link.click()
