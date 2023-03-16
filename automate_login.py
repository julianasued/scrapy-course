from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# GranConcursos credenciais
USERNAME = ""
PASSWORD = ""


def run():
    # inicializa o chrome drive
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=chrome_options)

    # entra na pagina do curso
    driver.get("https://www.grancursosonline.com.br/identificacao")
    # procura nome e insere no input
    driver.find_element("id", "login-email-site").send_keys(USERNAME)
    # procura senha e insere no input
    driver.find_element("id", "login-senha-site").send_keys(PASSWORD)
    # clica no botão de login
    driver.find_element("id", "login-entrar-site").click()
    # aguarda a pagina ser carregada
    WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )
    time.sleep(20)

if __name__ == '__main__':
    run()
