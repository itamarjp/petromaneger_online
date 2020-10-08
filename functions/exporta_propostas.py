import os
import time
from pathlib import Path

import mysql.connector
from flask import Flask
from flask_mysqldb import MySQL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from functions import ler_csv_propostas, page_selectors
from models import db_config

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

mysql = MySQL(app)

iDsNaoEncontradas = []
x = 0
iframeID = ''


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


def loginSite(loginPetronect, SenhaPetronect):
    time.sleep(2)
    iframe = browser.find_element_by_id("obnNavIFrame")
    browser.switch_to.frame(iframe)
    browser.switch_to.default_content()
    iframe_obv = browser.find_element_by_xpath("//div[@class='embed-container']//iframe")
    browser.switch_to.frame(iframe_obv)
    inputUser = browser.find_element_by_id("inputUser")
    inputPass = browser.find_element_by_id("inputSenha")
    inputUser.send_keys(loginPetronect)
    inputPass.send_keys(SenhaPetronect)
    okButton = browser.find_element_by_xpath("//button[@class='btn-login btn btn-success form-control']")
    okButton.click()


def painelOportunidades():  # funciona ok
    clickCotacoesElet = WebDriverWait(browser, 30).until(lambda x: x.find_element_by_id("tabIcon1"))
    clickCotacoesElet.click()
    time.sleep(3)
    browser.implicitly_wait(20)
    clickPainelOportunidades = browser.find_element_by_id("subTabIndex1")
    clickPainelOportunidades.click()


def query():  # funciona OK
    try:
        erroEntrada = browser.find_element_by_link_text(page_selectors.query)
        print('query: ' + erroEntrada)
        if erroEntrada == page_selectors.query:
            sair = browser.find_element_by_xpath(page_selectors.sairSeguranca)
            sair.click()
            time.sleep(2)
            yes = browser.find_element_by_xpath(page_selectors.sairSegurancaBttSim)
            yes.click()
        else:
            print(erroEntrada)
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
    print('entra Oportunidade')


def selecionaConcluidas(i):
    wait = WebDriverWait(browser, 30)
    eventoSelecao = browser.find_element_by_xpath(page_selectors.statusEventoSelecao)
    eventoSelecao.click()
    time.sleep(3)
    eventoSelecao.send_keys(Keys.ARROW_UP)
    eventoSelecao.send_keys(Keys.ARROW_UP)
    eventoSelecao.send_keys(Keys.ARROW_UP)
    eventoSelecao.send_keys(Keys.ARROW_UP)
    eventoSelecao.send_keys(Keys.ARROW_UP)
    eventoSelecao.send_keys(Keys.ARROW_DOWN)
    eventoSelecao.send_keys(Keys.ARROW_DOWN)
    eventoSelecao.send_keys(Keys.ARROW_DOWN)
    eventoSelecao.click()
    buscar = browser.find_element_by_xpath(page_selectors.botaoBuscar)
    buscar.click()
    resBuscaId = verif_id(i)  # 'Achou Id' ou 'Não achou Id'
    print('seleciona Concluidas')
    return resBuscaId


def verif_id(i):  # Funciona Ok
    global checaIdAtributo
    global checkId
    time.sleep(2)
    j = i.rstrip()
    try:
        buscaId = "/html[1]/body[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[3]/td[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/span[1]/span[1]/table[1]/tbody[1]/tr[1]/td[1]/span[1]/span[4]/table[1]/tbody[1]/tr[1]/td[1]/span[1]/span[1]/div[1]/div[1]/div[1]/span[1]/span[1]/table[1]/tbody[1]/tr[2]/td[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[2]/td[2]/a[1]/span[1]"
        checaID = browser.find_element_by_xpath(buscaId)
        checaIdAtributo = checaID.text
        if j in checaIdAtributo:
            # id = browser.find_element_by_xpath(buscaId)
            checkId = 'Achou Id'
        else:
            checaIdAtributo = ''
            iDsNaoEncontradas.append(i)
    except:
        checkId = 'Não achou Id'
        print("Id Não Encontrada: " + i)
    return checkId


def downloadOpt(pasta, id):  # precisa trocar o Window handle
    try:
        browser.implicitly_wait(20)
        baixarArquivo = browser.find_element_by_id(page_selectors.downloadOport)
        baixarArquivo.click()
        time.sleep(3)
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        try:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE resumo_oportunidades SET proposta_baixada = 'True', caminho_proposta = %s WHERE "
                        "id_oportunidade = %s", [pasta + '/' + f'Propostas da Oportunidade {id}.csv', id])
            mysql.connection.commit()
            cur.close()
            print('dentro de downloadOpt MYSQL UPDATE, proposta Baixada: id ' + id)
        except Exception as e:
            print('Erro no MYSQL: ' + str(e))
    except:
        print("erro ao realizar download.")


def voltarPrimeiraTela():
    try:
        wait = WebDriverWait(browser, 20)
        wait.until(EC.visibility_of_element_located((By.XPATH, page_selectors.voltaPrimeiraTela)))
        voltar = browser.find_element_by_xpath(page_selectors.voltaPrimeiraTela)
        voltar.click()
    except:
        print("erro ao voltar a primeira tela.")


def sair():
    browser.switch_to.default_content()
    sair = browser.find_element_by_xpath(page_selectors.sairSeguranca)
    sair.click()
    time.sleep(2)
    yes = browser.find_element_by_xpath(page_selectors.sairSegurancaBttSim)
    yes.click()


def iconeOculos(i):
    try:
        wait = WebDriverWait(browser, 15)
        wait.until(EC.visibility_of_element_located((By.XPATH, page_selectors.iconeOculos)))
        time.sleep(2)
        oculos = browser.find_element_by_xpath(page_selectors.iconeOculos)
        oculos.click()
        iconeExiste = 'existe'
        print('achou icone')
    except:
        iconeExiste = 'nexiste'
        print('nao achou icone')
    return iconeExiste


def exportaPropostas():
    try:
        wait = WebDriverWait(browser, 120)
        wait.until(EC.visibility_of_element_located((By.XPATH, page_selectors.exportarPropostas)))
        exportar = browser.find_element_by_xpath(page_selectors.exportarPropostas)
        exportar.click()
        print('clicou em exportar propostas')
    except:
        print('Processo ainda em aberto.')


def downloadPropostasProcess(records, loginPetronect, SenhaPetronect, username, empresa):
    global browser
    pasta = criarPastaUser(username)

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    preferences = {"download.default_directory": pasta}
    options.add_experimental_option("prefs", preferences)
    browser = webdriver.Chrome(options=options)
    browser.get("https://www.petronect.com.br/irj/portal/anonymous/pt")

    loginSite(loginPetronect, SenhaPetronect)
    painelOportunidades()
    query()
    trocaFrame()
    lenght = len(records)
    x = 0
    while x < lenght:
        print('x = ' + str(x))
        print('records: ' + str(records))
        id = records[x]['id_oportunidade']
        idList = records[x]['id']
        print('id_oportunidade :' + id)
        user = records[x]['user']
        currentWindow = browser.title
        entraOportunidade(id)
        verificaId = selecionaConcluidas(id)
        if verificaId == 'Não achou Id':
            cur = mysql.connection.cursor()
            cur.execute("UPDATE resumo_oportunidades SET proposta_baixada = 'indisponivel' WHERE id_oportunidade = %s",
                        [id])
            mysql.connection.commit()
            cur.close()
            print('Não Achou ID')
            x = x + 1
            continue

        iconeExiste = iconeOculos(id)
        if iconeExiste == "nexiste":
            cur = mysql.connection.cursor()
            cur.execute("UPDATE resumo_oportunidades SET proposta_baixada = 'indisponivel' WHERE id_oportunidade = %s",
                        [id])
            mysql.connection.commit()
            cur.close()
            print('Nao achou icone Oculos')
            x = x + 1
            continue
        while currentWindow == "Painel de Oportunidades - SAP NetWeaver Portal":
            time.sleep(2)
            currentWindow = browser.title
        trocaFrame()
        exportaPropostas()
        while currentWindow == "Visualização de Propostas de Fornecedores - SAP NetWeaver Portal":
            time.sleep(2)
            try:
                browser.switch_to.window(browser.window_handles[1])
            except:
                pass
            currentWindow = browser.title
        downloadOpt(pasta, id)
        while currentWindow == f"-Baixar arquivo 'Propostas da Oportunidade {id}.csv'":
            time.sleep(2)
            try:
                browser.switch_to.window(browser.window_handles[1])
            except:
                pass
            currentWindow = browser.title
        trocaFrame()
        voltarPrimeiraTela()
        while currentWindow == "Visualização de Propostas de Fornecedores - SAP NetWeaver Portal":
            time.sleep(2)
            currentWindow = browser.title
        trocaFrame()
        print("ciclo")

        endereçoProposta = pasta + '/' + f'Propostas da Oportunidade {id}.csv'
        csv = endereçoProposta
        sort = ''
        sort = ler_csv_propostas.leCsv(csv, sort)
        ler_csv_propostas.classifica(sort, user, idList, id, empresa)
        x = x + 1
    sair()
    browser.close()


def criarPastaUser(username):
    pasta = f"./downloads/{username}/propostas"
    if os.path.exists(pasta) == False:
        Path(pasta).mkdir(parents=True, exist_ok=True)
    else:
        print("Diretório já existe.")
    return pasta
