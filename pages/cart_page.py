import allure
from playwright.sync_api import Page

from pages.inventory_page import product_slug


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.items = page.get_by_test_id("inventory-item")
        self.item_names = page.get_by_test_id("inventory-item-name")
        self.checkout_button = page.get_by_test_id("checkout")
        self.continue_shopping_button = page.get_by_test_id("continue-shopping")

    @allure.step("Remover '{product_name}' na página do carrinho")
    def remove(self, product_name: str):
        self.page.get_by_test_id(f"remove-{product_slug(product_name)}").click()

    @allure.step("Ir para o checkout")
    def checkout(self):
        self.checkout_button.click()
