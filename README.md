# Customer Onboarding Automation Bot

Este projeto é um **bot automatizado** desenvolvido em Python utilizando **BotCity WebBot** e **Selenium** para realizar o processo de onboarding de clientes no site da Automation Anywhere, preenchendo formulários com base em um CSV.

O bot realiza:

1. Login seguro no site.
2. Preenchimento automático do formulário de cadastro de clientes.
3. Manipulação de cookies, modais e dropdowns.
4. Submissão dos dados do CSV no site.

---

## Pré-requisitos

- Python 3.9 ou superior
- Google Chrome instalado
- ChromeDriver compatível (o bot baixa automaticamente via `webdriver-manager`)
- Pacotes Python:

```bash
pip install botcity-web selenium webdriver-manager pandas requests

