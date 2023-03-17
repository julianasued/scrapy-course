from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from decouple import config
import time
import util

# GranConcursos credenciais
USERNAME = config('LOGIN')
PASSWORD = config('SENHA')


def download_pdf(driver:'WebDriver', path:'Path'):
    tab = driver.find_element(By.ID, "tab-row-pdf")
    disciplinas = tab.find_elements(By.CSS_SELECTOR, "#accordion2 > div")
    for disciplina in disciplinas:
        disciplina_nome = disciplina.find_element(By.CSS_SELECTOR, "h5 span").get_attribute("textContent")
        disciplina_path = util.create_folder(path, disciplina_nome)
        aulas = tab.find_elements(By.CSS_SELECTOR, "div[data-slug]")
        for aula in aulas:
            aula_nome = aula.find_element(By.CSS_SELECTOR, "h5 span").get_attribute("textContent") 
            target = aula.get_attribute("data-target")[1:]
            aula_path = util.create_folder(disciplina_path, f'pdf/{aula_nome}')
            conteudos = disciplina.find_elements(By.CSS_SELECTOR, f'#{target} .card-body .item')
            for conteudo in conteudos:
                conteudo_nome = conteudo.find_element(By.CLASS_NAME, 'text-color-hover-blue-600').get_attribute("textContent")
                pdf_url = conteudo.find_element(By.CSS_SELECTOR, 'a[aria-label="Baixar aula em PDF"]').get_attribute('href')
                util.download_file(driver, pdf_url, aula_path, conteudo_nome)
                util.wait_sleep(1, 2)


def download_materiais(driver:'WebDriver', path:'Path'):
    tab_btn = driver.find_element(By.CSS_SELECTOR, 'a[href="#tab-row-materiais"]')
    driver.execute_script("arguments[0].click();", tab_btn) 
    util.wait_sleep(1, 2)
    materiais = driver.find_elements(By.CSS_SELECTOR, "#tab-row-materiais .justify-content-between")
    materiais_path = util.create_folder(path, 'materiais')
    for material in materiais:
        material_nome = material.find_element(By.CSS_SELECTOR, ".lh-5").get_attribute("textContent")
        material_url = material.find_element(By.TAG_NAME, "a").get_attribute("href")
        util.download_file(driver, material_url, materiais_path, material_nome)
        time.sleep(1)


def download_videos(driver:'WebDriver', path:'Path'):
    tab = driver.find_element(By.ID, "tab-row-video")
    disciplinas = tab.find_elements(By.CSS_SELECTOR, "#accordion > div")
    for disciplina in disciplinas:
        disciplina_nome = disciplina.find_element(By.CSS_SELECTOR, "h5 span").get_attribute("textContent")
        disciplina_path = util.create_folder(path, disciplina_nome)
        aulas = tab.find_elements(By.CSS_SELECTOR, "div[data-slug]")
        for aula in aulas:
            aula_nome = aula.find_element(By.CSS_SELECTOR, "h5 span").get_attribute("textContent") 
            target = aula.get_attribute("data-target")[1:]
            aula_path = util.create_folder(disciplina_path, f'pdf/{aula_nome}')
            conteudos = disciplina.find_elements(By.CSS_SELECTOR, f'#{target} .card-body .item')
            for conteudo in conteudos:
                conteudo_nome = conteudo.find_element(By.CLASS_NAME, 'text-color-hover-blue-600').get_attribute("textContent")
                videu_url = conteudo.find_element(By.CSS_SELECTOR, 'a[aria-label="Baixar aula em PDF"]').get_attribute('href')
                #util.download_file(driver, pdf_url, aula_path, conteudo_nome)
                #util.wait_sleep(1, 2)
                print(videu_url)


def download_concurso(driver:'WebDriver', link:str, nome:str):
    path = util.create_root_folder(nome)
    driver.get(link)
    util.wait_sleep(1, 3)
    #download_pdf(driver, path)
    #download_materiais(driver, path)
    download_videos(driver, path)


def download_concursos(driver:'WebDriver'):
    driver.get("https://www.grancursosonline.com.br/aluno/espaco/meus-cursos")
    util.wait_loading(driver)
    cursos = driver.find_elements(By.CSS_SELECTOR, '.card-curso')
    
    for curso in cursos:
        nome = curso.find_element(By.CSS_SELECTOR, '[role="link"]').text
        download_concurso(driver, curso.get_attribute("href"), nome)
    time.sleep(5)



def run():
    # inicializa o chrome drive
    chrome_options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()

    # entra na pagina do curso
    driver.get("https://www.grancursosonline.com.br/identificacao")
    # procura nome e insere no input
    driver.find_element("id", "login-email-site").send_keys(USERNAME)
    # procura senha e insere no input
    util.wait_sleep(1, 2)
    driver.find_element("id", "login-senha-site").send_keys(PASSWORD)
    # clica no botão de login
    driver.find_element("id", "login-entrar-site").click()
    # aguarda a pagina ser carregada
    util.wait_sleep(5, 6)
    download_concursos(driver)


if __name__ == '__main__':
    run()