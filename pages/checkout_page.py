import re

import allure
from playwright.sync_api import Page


def _money(text: str) -> float:
    return float(re.search(r"\$([\d.]+)", text).group(1))


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        # Etapa 1: dados do cliente
        self.first_name = page.get_by_test_id("firstName")
        self.last_name = page.get_by_test_id("lastName")
        self.postal_code = page.get_by_test_id("postalCode")
        self.continue_button = page.get_by_test_id("continue")
        self.error_message = page.get_by_test_id("error")
        # Etapa 2: resumo do pedido
        self.item_names = page.get_by_test_id("inventory-item-name")
        self.item_prices = page.get_by_test_id("inventory-item-price")
        self.subtotal_label = page.get_by_test_id("subtotal-label")
        self.tax_label = page.get_by_test_id("tax-label")
        self.total_label = page.get_by_test_id("total-label")
        self.finish_button = page.get_by_test_id("finish")
        # Etapa 3: confirmação
        self.complete_header = page.get_by_test_id("complete-header")

    @allure.step("Preencher dados do cliente")
    def fill_information(self, first_name: str, last_name: str, postal_code: str):
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)

    @allure.step("Continuar para o resumo")
    def continue_to_overview(self):
        self.continue_button.click()

    @allure.step("Finalizar compra")
    def finish(self):
        self.finish_button.click()

    def item_price_values(self) -> list[float]:
        return [_money(t) for t in self.item_prices.all_inner_texts()]

    def subtotal(self) -> float:
        return _money(self.subtotal_label.inner_text())

    def tax(self) -> float:
        return _money(self.tax_label.inner_text())

    def total(self) -> float:
        return _money(self.total_label.inner_text())
