# Customer Onboarding Automation Bot

Automatiza o processo de onboarding de clientes no site da Automation Anywhere. O bot realiza login, preenche formulários com dados de um CSV e submete as informações, economizando tempo e evitando erros manuais.

---

## Arquivos do projeto

- `bot.py` → Script principal do bot  
- `customer-onboarding-challenge.csv` → CSV de entrada (baixado automaticamente pelo bot)  
- `Accuracy.png` → Screenshot opcional gerada após execução  

---

## Estrutura do CSV

| Coluna            | Descrição                          |
|------------------|-----------------------------------|
| `customerName`    | Nome do cliente                   |
| `customerID`      | ID do cliente                     |
| `primaryContact`  | Contato principal                 |
| `street`          | Rua                               |
| `city`            | Cidade                            |
| `state`           | Estado (sigla ou valor do dropdown) |
| `zip`             | CEP                               |
| `email`           | Email do cliente                  |
| `activeDiscount`  | "YES" ou "NO"                     |
| `NDA`             | "YES" ou "NO"                     |

---

## Configuração

No `bot.py`, configure suas credenciais:

```python
email = "seu_email@example.com"
senha = "sua_senha_forte"

# Como Executar

```bash
python bot.py

Funcionalidades do Bot
✅ Abrir o navegador

✅ Aceitar cookies e clicar nos modais de login

✅ Inserir email e senha

✅ Navegar até a página de onboarding

✅ Preencher e submeter os dados do CSV

✅ Salvar uma screenshot Accuracy.png

Observações Importantes
⏳ Utiliza esperas explícitas (WebDriverWait) para garantir que os elementos estejam visíveis

❌ Mensagens de erro aparecem no console caso algum campo não seja encontrado

🖼️ Se os campos estiverem dentro de iframe, ajustes podem ser necessários

📝 Campos com espaços ou caracteres especiais no CSV podem precisar de ajustes no código
