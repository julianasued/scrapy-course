from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# GranConcursos credenciais
username = "usuario"
password = "senha"

# inicializa o chrome drive
driver = webdriver.Chrome(r"chromedriver")
# entra na pagina do curso
driver.get("https://www.grancursosonline.com.br/identificacao")
# procura nome e insere no input
driver.find_element("id", "login-email-site").send_keys(username)
# procura senha e insere no input
driver.find_element("id", "login-senha-site").send_keys(password)
# clica no botão de login
driver.find_element("id", "login-entrar-site").click()
# aguarda a pagina ser carregada
WebDriverWait(driver=driver, timeout=10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
)
