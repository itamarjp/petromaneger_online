import glob
import os
import time
from os.path import basename
from pathlib import Path
from zipfile import ZipFile

import mysql.connector
from flask import Flask
from flask_mysqldb import MySQL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from functions import ler_pdf, page_selectors
from models import db_config

cadaLinha = []
opIds = []
iDsNaoEncontradas = []
continua = 's'
x = 0
iframeID = ''

app = Flask(__name__)

if db_config.MODE == 'development':
    app.config['MYSQL_HOST'] = db_config.MYSQL_HOST
    app.config['MYSQL_USER'] = db_config.MYSQL_USER
    app.config['MYSQL_PASSWORD'] = db_config.MYSQL_PASSWORD
    app.config['MYSQL_DB'] = db_config.MYSQL_DB
    app.config['MYSQL_CURSORCLASS'] = db_config.MYSQL_CURSORCLASS
    app.config['FLASK_DEBUG'] = 1
else:
    app.config['MYSQL_HOST'] = db_config.CLEAR_DB_MYSQL_HOST
    app.config['MYSQL_USER'] = db_config.CLEAR_DB_MYSQL_USER
    app.config['MYSQL_PASSWORD'] = db_config.MYSQL_PASSWORD
    app.config['MYSQL_DB'] = db_config.CLEAR_DB_MYSQL_DB
    app.config['MYSQL_CURSORCLASS'] = db_config.MYSQL_CURSORCLASS
    app.config['FLASK_DEBUG'] = 0

# init MYSQL
mysql = MySQL(app)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def trocaFrame():
    try:
        time.sleep(3)
        global iframeID
        browser.implicitly_wait(20)
        iframe = browser.find_element_by_id("contentAreaFrame")
        iframeID = iframe.get_attribute("id")
        browser.switch_to.frame(iframe)
        iframeIsolated = browser.find_element_by_id("isolatedWorkArea")
        iframeID = iframeIsolated.get_attribute("id")
        browser.switch_to.frame(iframeIsolated)
    except:
        print("erro na troca de frame.")


def loginSite(login, senha):  # funciona ok
    iframe = browser.find_element_by_id("obnNavIFrame")
    browser.switch_to.frame(iframe)
    browser.switch_to.default_content()
    iframe_obv = browser.find_element_by_xpath("//div[@class='embed-container']//iframe")
    browser.switch_to.frame(iframe_obv)
    inputUser = browser.find_element_by_id("inputUser")
    inputPass = browser.find_element_by_id("inputSenha")
    inputUser.send_keys(login)
    inputPass.send_keys(senha)
    okButton = browser.find_element_by_xpath("//button[@class='btn-login btn btn-success form-control']")
    okButton.click()
    time.sleep(10)
    if browser.title == 'YPUSER_MAINTENANCE [Web Dynpro para ABAP]':
        iframe = browser.find_element_by_id('URLSPW-0')
        browser.switch_to.frame(iframe)
        estou_ciente = browser.find_element_by_xpath("//a[@class='urPWClose urPWCloseIcon urPWBtnIcon urPWButton']")
        estou_ciente.click()


def painelOportunidades():  # funciona ok
    time.sleep(3)
    clickCotacoesElet = WebDriverWait(browser, 30).until(lambda x: x.find_element_by_id("tabIcon1"))
    clickCotacoesElet.click()
    time.sleep(3)
    browser.implicitly_wait(20)
    clickPainelOportunidades = browser.find_element_by_id("subTabIndex1")
    clickPainelOportunidades.click()


def query():  # funciona OK
    try:
        erroEntrada = browser.find_element_by_link_text(page_selectors.query)
        if erroEntrada == page_selectors.query:
            sair = browser.find_element_by_xpath(page_selectors.sairSeguranca)
            sair.click()
            time.sleep(2)
            yes = browser.find_element_by_xpath(page_selectors.sairSegurancaBttSim)
            yes.click()
        else:
            pass
    except:
        print("entrada OK.")


def entraOportunidade(i):  # Funciona OK
    flag = False
    while flag == False:
        try:
            campoOport = browser.find_element_by_xpath(page_selectors.num_oport)
            campoOport.clear()
            flag = True
        except:
            time.sleep(2)
            pass

    campoOport = browser.find_element_by_xpath(page_selectors.num_oport)
    campoOport.clear()
    campoOport.send_keys(i)


def clicaOport():  # Funciona Ok
    time.sleep(3)
    clickOpt = browser.find_element_by_xpath(page_selectors.clicaOportunidade)
    clickOpt.click()


def selecionaNulo():  # Funciona Ok
    wait = WebDriverWait(browser, 30)
    eventoSelecao = wait.until(EC.element_to_be_clickable((By.XPATH, page_selectors.statusEventoSelecao)))
    eventoSelecao = browser.find_element_by_xpath(page_selectors.statusEventoSelecao)
    eventoSelecao.click()
    time.sleep(3)
    eventoSelecao.send_keys(Keys.ARROW_UP)
    eventoSelecao.send_keys(Keys.ARROW_UP)
    buscar = browser.find_element_by_xpath(page_selectors.botaoBuscar)
    buscar.click()


def verif_id(i):  # Funciona Ok
    time.sleep(2)
    checkId = False
    try:
        j = i.rstrip()
        buscaId = "/html[1]/body[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[3]/td[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/span[1]/span[1]/table[1]/tbody[1]/tr[1]/td[1]/span[1]/span[4]/table[1]/tbody[1]/tr[1]/td[1]/span[1]/span[1]/div[1]/div[1]/div[1]/span[1]/span[1]/table[1]/tbody[1]/tr[2]/td[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[2]/td[2]/a[1]/span[1]"
        checaID = browser.find_element_by_xpath(buscaId)
        checaIdAtributo = checaID.text
        if j in checaIdAtributo:
            id = browser.find_element_by_xpath(buscaId)
            idDigitada = id.get_attribute("value")
            iDsNaoEncontradas.append(idDigitada)
            checkId = False
        else:
            checaIdAtributo = ''
    except:
        checkId = True
        print("Id Não Encontrada.")
    return checkId


def resumoOpt():  # Funciona Ok
    try:
        wait = WebDriverWait(browser, 500)
        wait.until(EC.visibility_of_element_located((By.XPATH, page_selectors.resumoOportunidade)))
    except:
        print('timeout')
    resumo = browser.find_element_by_xpath(page_selectors.resumoOportunidade)
    resumo.click()


def downloadOpt():  # precisa trocar o Window handle
    try:
        browser.implicitly_wait(20)
        baixarArquivo = browser.find_element_by_id(page_selectors.downloadOport)
        baixarArquivo.click()
        time.sleep(3)
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
    except:
        print("erro ao realizar download.")


def baixarAnexos():
    time.sleep(2)
    try:
        wait = WebDriverWait(browser, 5)
        wait.until(EC.visibility_of_element_located((By.XPATH, page_selectors.notasAnexos)))
    except:
        print('timeout')
    notasAnexos = browser.find_element_by_xpath(page_selectors.notasAnexos)
    notasAnexos.click()
    time.sleep(2)
    try:
        wait = WebDriverWait(browser, 5)
        wait.until(EC.visibility_of_element_located((By.XPATH, page_selectors.baixarTodosAnexos)))
    except:
        print('timeout')
    baixarTodosAnexos = browser.find_element_by_xpath(page_selectors.baixarTodosAnexos)
    baixarTodosAnexos.click()


def renomeiaAnexos(i, pasta):
    REMOVE_WORD = "Anexos" + i.rstrip() + ".zip"
    PATH_REPLACE = pasta + '/'
    try:
        for filename in os.listdir(PATH_REPLACE):
            if filename == "Anexos.zip":
                os.rename(PATH_REPLACE + "Anexos.zip", PATH_REPLACE + REMOVE_WORD)
    except Exception as e:
        print("Anexos não encontrados" + str(e))


def voltaPainelOport():
    try:
        wait = WebDriverWait(browser, 500)
        wait.until(EC.visibility_of_element_located((By.LINK_TEXT, page_selectors.voltaPainelOport)))
        voltar = browser.find_element_by_link_text(page_selectors.voltaPainelOport)
        voltar.click()
    except:
        print("erro ao voltar ao painel de oportunidades.")


def sair():
    browser.switch_to.default_content()
    sair = browser.find_element_by_xpath(page_selectors.sairSeguranca)
    sair.click()
    time.sleep(2)
    yes = browser.find_element_by_xpath(page_selectors.sairSegurancaBttSim)
    yes.click()


def exportaPropostas():
    try:
        wait = WebDriverWait(browser, 150)
        wait.until(EC.visibility_of_element_located((By.XPATH, page_selectors.exportarPropostas)))
    except:
        print('Processo ainda em aberto.')
    exportar = browser.find_element_by_xpath(page_selectors.exportarPropostas)
    exportar.click()


def downloadFilesProcess(listIds, loginPetronect, SenhaPetronect, username, titleList, idArticles, id):
    global browser
    pasta = os.path.realpath(criarPastaUser(username, titleList))
    print(listIds)
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("--start-maximized")
    options.add_argument('--disable-dev-shm-usage')
    preferences = {"download.default_directory": pasta}
    options.add_experimental_option("prefs", preferences)
    browser = webdriver.Chrome(chrome_options=options)
    browser.get("https://www.petronect.com.br/irj/portal/anonymous/pt")
    loginSite(loginPetronect, SenhaPetronect)
    painelOportunidades()
    trocaFrame()
    query()
    for i in listIds:
        currentWindow = browser.title
        entraOportunidade(i)
        selecionaNulo()
        checkId = verif_id(i)
        if checkId:
            iDsNaoEncontradas.append(i)
            continue
        clicaOport()
        while currentWindow == "Painel de Oportunidades - SAP NetWeaver Portal":
            time.sleep(2)
            currentWindow = browser.title
        trocaFrame()
        resumoOpt()
        while currentWindow == "Solicitação de cotação - SAP NetWeaver Portal":
            time.sleep(2)
            try:
                browser.switch_to.window(browser.window_handles[1])
            except:
                pass
            currentWindow = browser.title
        downloadOpt()
        while currentWindow == "Aplicação Floor Plan Manager para OIF-Baixar arquivo 'Resumo_da_oportunidade.pdf'":
            time.sleep(2)
            try:
                browser.switch_to.window(browser.window_handles[1])
            except:
                pass
            currentWindow = browser.title
        trocaFrame()
        baixarAnexos()
        while currentWindow == "Solicitação de cotação - SAP NetWeaver Portal":
            time.sleep(2)
            try:
                browser.switch_to.window(browser.window_handles[1])
            except:
                pass
            currentWindow = browser.title
        downloadOpt()
        while currentWindow == "Aplicação Floor Plan Manager para OIF-Baixar arquivo 'Anexos.zip'":
            time.sleep(2)
            try:
                browser.switch_to.window(browser.window_handles[1])
            except:
                pass
            currentWindow = browser.title
        trocaFrame()
        voltaPainelOport()
        renomeiaAnexos(i, pasta)
        while currentWindow == "Solicitação de cotação - SAP NetWeaver Portal":
            time.sleep(2)
            currentWindow = browser.title
        trocaFrame()
        print("ciclo")
    sair()
    browser.close()
    pdfClass = ler_pdf.pdf(pasta, id, username, titleList)
    pdfClass.listaPastasEArquivos()
    pdfClass.renomeiaArquivos()

    cur = mysql.connection.cursor()
    cur.execute("UPDATE articles SET downloadComplete = 'Sim', downloadFolder = %s WHERE id = %s", [pasta, idArticles])
    mysql.connection.commit()
    cur.close()

    zipAnexos(pasta, titleList)


def criarPastaUser(username, titleList):
    pasta = f"./downloads/oportunidades/{username}/{titleList}"
    if os.path.exists(pasta) == False:
        Path(pasta).mkdir(parents=True, exist_ok=True)
    else:
        print("Diretório já existe.")
    return pasta


def zipAnexos(pasta, titleList):
    zips = []
    for file in glob.glob(pasta + "/" + "*.zip"):
        zips.append(file)
    print(zips)
    with ZipFile(pasta + "/" + titleList + ".zip", 'w') as zip:
        for file in zips:
            zip.write(file, basename(file))
    for file in zips:
        os.remove(file)
