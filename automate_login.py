from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from pathlib import Path
import time
import util
import os


SETTINGS = util.load_config()

# GranConcursos credenciais
USERNAME = SETTINGS['login']
PASSWORD = SETTINGS['senha']
LAST_REFRESH = time.time()


def refresh_session(driver:'WebDriver', tab_id:'int'):
    """
    Atualiza a sessão do navegador
    """
    global LAST_REFRESH
    current_time = time.time()

    if((current_time - LAST_REFRESH) > 55):
        driver.switch_to.window(driver.window_handles[0])
        driver.refresh()
        LAST_REFRESH = current_time
        print("Sessão atualizada.")
        util.wait_sleep(1, 1)
        driver.switch_to.window(driver.window_handles[tab_id])


def download_pdf(driver:'WebDriver', path:'Path'):
    """
    Faz o download de todos os PDFs de um concurso
    """
    print("-- Fazendo download dos pdf.")
    tab = driver.find_element(By.ID, "tab-row-pdf")
    disciplinas = tab.find_elements(By.CSS_SELECTOR, "#accordion2.listagem-aulas > div")
    for disciplina in disciplinas[:2]:
        disciplina_nome = disciplina.find_element(By.CSS_SELECTOR, "h5 span").get_attribute("textContent")
        aulas_target = disciplina.find_element(By.TAG_NAME, "div").get_attribute("data-target")
        disciplina_path = util.create_folder(path, disciplina_nome)
        try:
            aulas = disciplina.find_elements(By.CSS_SELECTOR, f"{aulas_target} > div")
            for aula in aulas[:1]:
                aula_nome = aula.find_element(By.CSS_SELECTOR, "h5 span").get_attribute("textContent") 
                target = aula.find_element(By.TAG_NAME, "div").get_attribute("data-target")
                aula_path = util.create_folder(disciplina_path, f'pdf{os.sep}{aula_nome.strip()}')
                conteudos = aula.find_elements(By.CSS_SELECTOR, f'{target} .card-body .item')
                for conteudo in conteudos[:1]:
                    conteudo_nome = conteudo.find_element(By.CLASS_NAME, 'text-color-hover-blue-600').get_attribute("textContent")
                    try:
                        pdf_url = conteudo.find_element(By.CSS_SELECTOR, 'a[aria-label="Baixar aula em PDF"]').get_attribute("href")
                        print("---- Baixando pdf: ", conteudo_nome)
                        util.download_file(driver, pdf_url, aula_path, conteudo_nome)
                        util.wait_sleep(2, 4)
                    except NoSuchElementException as err:
                        print("Pdf não encontrado.")
                    refresh_session(driver, 2)
        except NoSuchElementException:
            print('---- Layout tipo 2.')
            links_videos = {}
            toggle = driver.find_element(By.CSS_SELECTOR, f'div[data-target="{aulas_target}"]')
            driver.execute_script("arguments[0].click();",  toggle)
            util.wait_sleep(2, 2)
            conteudos = driver.find_elements(By.CSS_SELECTOR, f'{aulas_target} .card-body .item')
            aula_path = util.create_folder(disciplina_path, 'pdf')
            for conteudo in conteudos[:2]:
                conteudo_nome = conteudo.find_element(By.CLASS_NAME, 'text-color-hover-blue-600').get_attribute("textContent")
                try:
                    pdf_url = conteudo.find_element(By.CSS_SELECTOR, 'a[aria-label="Baixar aula em PDF"]').get_attribute("href")
                    print("---- Baixando pdf: ", conteudo_nome)
                    util.download_file(driver, pdf_url, aula_path, conteudo_nome)
                    util.wait_sleep(2, 4)
                except NoSuchElementException as err:
                    print("Pdf não encontrado.")
                refresh_session(driver, 2)


def download_materiais(driver:'WebDriver', path:'Path'):
    """
    Faz o download de todos os materias de um 
    """
    print("-- Fazendo download dos materias.")
    tab_btn = driver.find_element(By.CSS_SELECTOR, 'a[href="#tab-row-materiais"]')
    driver.execute_script("arguments[0].click();", tab_btn) 
    util.wait_sleep(1, 2)
    materiais = driver.find_elements(By.CSS_SELECTOR, "#tab-row-materiais .justify-content-between")
    materiais_path = util.create_folder(path, 'materiais')
    for material in materiais[:1]:
        material_nome = material.find_element(By.CSS_SELECTOR, ".lh-5").get_attribute("textContent")
        material_url = material.find_element(By.TAG_NAME, "a").get_attribute("href")
        print("---- Baixando material: ", material_nome)
        util.download_file(driver, material_url, materiais_path, material_nome)
        util.wait_sleep(2, 4)
        refresh_session(driver, 2)


def download_videos(driver:'WebDriver', path:'Path', links:dict):
    """
    Faz o download dos videos passados
    """
    nova_aba = True
    for nome, link in sorted(links.items())[:1]:
        print("---- Baixando video: ", nome)
        if nova_aba:
            driver.execute_script(f"window.open('{link}', '_blank')")
            driver.switch_to.window(driver.window_handles[3])
            nova_aba = False
        else:
            driver.get(link)
            util.wait_sleep(5, 8)
        video_url = driver.find_element(By.TAG_NAME, "video").get_attribute("src")
        util.download_video(video_url, nome, path)
        refresh_session(driver, 3)
    driver.close()


def download_video_aulas(driver:'WebDriver', path:'Path'):
    """
    Inicia o download das videos aulas
    """
    print("-- Fazendo download dos Videos.")
    disciplinas = driver.find_elements(By.CSS_SELECTOR, "#accordion > div")
    for disciplina in disciplinas[:2]:
        disciplina_nome = disciplina.find_element(By.CSS_SELECTOR, "h5 span").get_attribute("textContent")
        aulas_target = disciplina.find_element(By.TAG_NAME, "div").get_attribute("data-target")
        disciplina_path = util.create_folder(path, disciplina_nome)
        try:
            aulas = disciplina.find_elements(By.CSS_SELECTOR, f"{aulas_target} > div")
            for aula in aulas[:1]:
                links_videos = {}
                aula_nome = aula.find_element(By.CSS_SELECTOR, "h5 span").get_attribute("textContent") 
                aula_path = util.create_folder(disciplina_path, f'videos{os.sep}{aula_nome.strip()}')
                conteudos = aula.find_elements(By.CSS_SELECTOR, '.card-body .item')
                for conteudo in conteudos[:1]:
                    a = conteudo.find_element(By.CSS_SELECTOR, "label a")
                    link = a.get_attribute("href")
                    nome = a.get_attribute("textContent")
                    links_videos[nome] = link
                    refresh_session(driver, 2)
        except NoSuchElementException:
            print('---- Layout tipo 2.')
            links_videos = {}
            toggle = driver.find_element(By.CSS_SELECTOR, f'div[data-target="{aulas_target}"]')
            driver.execute_script("arguments[0].click();",  toggle)
            util.wait_sleep(2, 2)
            conteudos = driver.find_elements(By.CSS_SELECTOR, f'{aulas_target} .card-body .item')
            aula_path = util.create_folder(disciplina_path, 'videos')
            for conteudo in conteudos[:2]:
                a = conteudo.find_element(By.CSS_SELECTOR, "label a")
                link = a.get_attribute("href")
                nome = a.get_attribute("textContent")
                links_videos[nome] = link
                refresh_session(driver, 2)
        download_videos(driver, aula_path, links_videos)
        driver.switch_to.window(driver.window_handles[2])
        util.wait_sleep(1, 2)

def download_concurso(driver:'WebDriver', link:str, nome:str):
    """
    Inicia download dos arquivos dos Concurso
    """
    print("# Fazendo download do concurso: ", nome)
    path = util.create_root_folder(SETTINGS['root'], nome)
    driver.execute_script(f"window.open('{link}', '_blank')")
    driver.switch_to.window(driver.window_handles[2])
    util.wait_sleep(4, 6)
    #download_video_aulas(driver, path)
    download_pdf(driver, path)
    download_materiais(driver, path)
    driver.close()


def download_concursos(driver:'WebDriver', pagina_num=1):
    """
    Inicia o download de todos os cursos matrículados
    """
    proxima_pagina = driver.find_elements(By.CSS_SELECTOR, "#pagination li.active + li.cursor-pointer")
    cursos = driver.find_elements(By.CSS_SELECTOR, '.card-curso')
    print("Pagina: ", pagina_num)
    util.wait_sleep(1, 1)

    # Pecorre todas as páginas se 'pagina' igual a 0 Ou apenas a página Especificada
    if SETTINGS['pagina'] == 0 or SETTINGS['pagina'] == pagina_num:
        for curso in cursos:
            driver.switch_to.window(driver.window_handles[1])
            nome = curso.find_element(By.CSS_SELECTOR, '[role="link"]').text.strip()
            if len(SETTINGS['concursos']) == 0 or nome in SETTINGS['concursos']:
                download_concurso(driver, curso.get_attribute("href"), nome)
                util.wait_sleep(2,5)

    if len(proxima_pagina) > 0:
        print()
        pagina_num = int(proxima_pagina[0].text)
        driver.execute_script("arguments[0].click();", proxima_pagina[0])
        util.wait_sleep(1, 1)
        download_concursos(driver, pagina_num)


def run():
    # inicializa o chrome drive
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('log-level=3')
    if not SETTINGS['tela']:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()

    # entra na pagina do curso
    driver.get("https://www.grancursosonline.com.br/identificacao")
    driver.find_element("id", "login-email-site").send_keys(USERNAME)
    util.wait_sleep(1, 2)
    driver.find_element("id", "login-senha-site").send_keys(PASSWORD)
    driver.find_element("id", "login-entrar-site").click()
    util.wait_sleep(2, 3)

    driver.execute_script(f"window.open('https://www.grancursosonline.com.br/aluno/espaco/meus-cursos', '_blank')")
    driver.switch_to.window(driver.window_handles[1])
    util.wait_sleep(3, 5)
    download_concursos(driver)


if __name__ == '__main__':
    run()