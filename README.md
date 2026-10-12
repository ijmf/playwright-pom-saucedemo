# playwright-pom-saucedemo

Suíte de testes E2E para o [SauceDemo](https://www.saucedemo.com) com **Playwright + pytest**, usando o padrão **Page Object Model (POM)** e relatórios **Allure**.

## Stack

- Python 3.13
- Playwright (`pytest-playwright`)
- pytest
- Allure (`allure-pytest`)

## Estrutura

```
pages/            # Page Objects (login, inventário, carrinho, checkout)
tests/            # Cenários de teste
conftest.py       # Fixtures (páginas, login) e screenshot no Allure em caso de falha
pytest.ini        # base_url, markers e diretório do Allure
.github/workflows # CI no GitHub Actions
```

## Cenários

| Arquivo | Cenários |
|---|---|
| `test_login.py` | login válido, usuário bloqueado, senha incorreta, campos vazios |
| `test_cart.py` | adicionar um produto, adicionar vários, remover produto, contador do carrinho |
| `test_checkout.py` | checkout completo, checkout sem dados (erro), resumo do pedido (itens, preços, subtotal, total) |

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
playwright install chromium
pytest
```

Opções úteis:

```bash
pytest --headed --slowmo 300        # ver o navegador
pytest -m cart                      # só um grupo (login | cart | checkout)
pytest --browser firefox            # outro navegador
pytest --tracing retain-on-failure  # trace do Playwright nas falhas
```

## Relatório Allure

Os resultados vão para `allure-results/`. Para abrir o relatório (requer Java):

```bash
allure serve allure-results                              # com o Allure CLI instalado
npx --yes allure-commandline@2.30.0 serve allure-results # sem instalar, via Node.js
```

Em falhas, o screenshot da página é anexado ao relatório.

## CI

O workflow `.github/workflows/ci.yml` roda a suíte no Chromium a cada push na `main` e em pull requests, gera o relatório Allure e o publica como artefato (`allure-report`), junto com os traces das falhas.
