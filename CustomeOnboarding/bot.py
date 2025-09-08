# Importações
import botcity.core
from botcity.web import WebBot, Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import Select

email = "xxxxxxxxxx"
senha = "xxxxxxxxxx"

# --- Função para preencher campos ---
def fill_input(bot, placeholder_text, value, timeout=15):
    try:
        input_field = WebDriverWait(bot.driver, timeout).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 f"//input[contains(@placeholder,'{placeholder_text}')] | //input[contains(@aria-label,'{placeholder_text}')]")
            )
        )
        input_field.click()
        bot.wait(500)
        input_field.clear()
        input_field.send_keys(value)
        return True
    except Exception as e:
        print(f"Erro ao preencher '{placeholder_text}': {e}")
        return False


# --- Função de login ---
def login_site(bot):
    try:
        # Aceitar cookies
        try:
            bot.driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
            print("Cookies aceitos via ID")
        except (NoSuchElementException, TimeoutException):
            try:
                bot.driver.find_element(By.XPATH, "//button[@id='onetrust-accept-btn-handler']").click()
                print("Cookies aceitos via XPath")
            except Exception as e:
                print(f"Erro ao aceitar cookies: {e}")

        # Botão de login
        WebDriverWait(bot.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "button_site-header__login-btn__zqRbe"))
        ).click()
        print("Botão de login clicado ✅")

        # Botão Community login
        WebDriverWait(bot.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "button_modal-login-btn__iPh6x"))
        ).click()
        print("Botão 'Community login' clicado ✅")

        # Preencher e-mail
        if fill_input(bot, "Email", email):
            print("E-mail preenchido ✅")
        else:
            print("Falha ao preencher e-mail ❌")
            return False

        # Clicar no botão Next
        next_button = WebDriverWait(bot.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Next']"))
        )
        bot.wait(500)
        next_button.click()
        bot.wait(2000)
        print("Clicou no botão Next ✅")

        # Preencher senha
        if fill_input(bot, "Password", senha):
            print("Senha preenchida ✅")
        else:
            print("Falha ao preencher senha ❌")
            return False

        # Clicar no botão Log in
        login_button = WebDriverWait(bot.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Log in']"))
        )
        bot.wait(500)
        login_button.click()
        bot.wait(2000)
        print("Clicou no botão Log in ✅")

        return True

    except Exception as e:
        print(f"Erro durante login: {e}")
        return False


def processo(bot, dados):
    try:
        for colunas in dados.itertuples():
            # Preencher campos de texto
            WebDriverWait(bot.driver, 10).until(
                EC.presence_of_element_located((By.ID, "customerName"))
            ).send_keys(colunas[1])

            WebDriverWait(bot.driver, 10).until(
                EC.presence_of_element_located((By.ID, "customerID"))
            ).send_keys(colunas[2])

            WebDriverWait(bot.driver, 10).until(
                EC.presence_of_element_located((By.ID, "primaryContact"))
            ).send_keys(colunas[3])

            WebDriverWait(bot.driver, 10).until(
                EC.presence_of_element_located((By.ID, "street"))
            ).send_keys(colunas[4])

            WebDriverWait(bot.driver, 10).until(
                EC.presence_of_element_located((By.ID, "city"))
            ).send_keys(colunas[5])

            # Selecionar estado no dropdown
            state_element = WebDriverWait(bot.driver, 10).until(
                EC.presence_of_element_located((By.ID, "state"))
            )
            Select(state_element).select_by_value(str(colunas[6]))

            WebDriverWait(bot.driver, 10).until(
                EC.presence_of_element_located((By.ID, "zip"))
            ).send_keys(colunas[7])

            WebDriverWait(bot.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            ).send_keys(colunas[8])

            # Radio buttons / checkboxes
            if colunas[9] == 'YES':
                bot.driver.find_element(By.ID, "activeDiscountYes").click()
            else:
                bot.driver.find_element(By.ID, "activeDiscountNo").click()

            if colunas[10] == 'NO':
                bot.driver.find_element(By.ID, "NDA").click()

            # Botão submit
            WebDriverWait(bot.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "submit_button"))
            ).click()

            # Pequena pausa para o formulário processar
            bot.wait(1000)

        return True

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Erro ao preencher o formulário: {e}")
        return False
    except Exception as e:
        print(f"Erro inesperado no processo: {e}")
        return False

# --- Função principal ---
def main():
    # Baixar CSV
    url = 'https://aai-devportal-media.s3.us-west-2.amazonaws.com/challenges/customer-onboarding-challenge.csv'
    r = requests.get(url, allow_redirects=True)
    open('customer-onboarding-challenge.csv', 'wb').write(r.content)

    # Ler CSV
    dados = pd.read_csv('customer-onboarding-challenge.csv', sep=',')

    # Inicializar BotCity
    bot = WebBot()
    bot.headless = False
    bot.browser = Browser.CHROME
    bot.driver_path = ChromeDriverManager().install()

    # Abrir página
    bot.browse("https://pathfinder.automationanywhere.com/")
    bot.maximize_window()
    bot.wait(1000)

    # Executar login
    if login_site(bot):
        print("✅ Login realizado com sucesso!")
        bot.wait(2000)
    else:
        print("❌ Falha no login.")

    bot.browse("https://pathfinder.automationanywhere.com/challenges/automationanywherelabs-customeronboarding.html")
    bot.wait(2000)

    if processo(bot, dados):
        print("✅ Processo realizado com sucesso!")
    else:
        print("❌ Falha no processo.")

    bot.wait(1000)
    bot.screenshot('Accuracy.png')
    bot.stop_browser()

# --- Executa o main ---
if __name__ == "__main__":
    main()
