import datetime
import os
import shutil
import camelot
import mysql.connector
from flask import Flask
from flask_mysqldb import MySQL
from models import db_config

anexos = []
listFiles = []
lista = []
ids = []
arquivoParaEnviar = []
arquivosEncontrados = []
errConversaoPdf = False

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


class pdf:
    def __init__(self, pasta, id, username, titleList):
        self.pasta = pasta
        self.id = id
        self.username = username
        self.titleList = titleList

    def listaPastasEArquivos(self):
        dir = os.listdir(self.pasta)
        for file in dir:
            if file.endswith(".pdf"):
                arquivosEncontrados.append(file)

    def renomeiaArquivos(self):
        for i in arquivosEncontrados:
            filePath = self.pasta + '/' + i
            errConversaoPdf = pdf.readPdf(self, filePath)
            if errConversaoPdf == True:
                continue
            oldName = filePath
            newName = self.pasta + '/' + idOpt + ' - ' + nomeOpt + '.pdf'
            shutil.move(oldName, newName)

            listFiles.append(newName)
            pdf.log(self)

    def readPdf(self, filePath):
        global tipo_opt, criterio, idOpt, nomeOpt, dataPublic, inicPerCotacao, fimPerCotacao
        try:
            tables = camelot.read_pdf(filePath)
            t1 = tables[1].df
            tipo_opt = t1.iat[2, 1]
            criterio = t1.iat[3, 1]
            idOpt = t1.iat[4, 1]
            nomeOpt = t1.iat[5, 1]
            dataPublic = (t1.iat[6, 1])
            inicPerCotacao = t1.iat[7, 1]
            fimPerCotacao = t1.iat[8, 1]
            errConversaoPdf = False
        except Exception as e:
            errConversaoPdf = True
            print("Erro da conversao do PDF." + str(e))
        return errConversaoPdf

    def log(self):
        timeNow = datetime.datetime.now()
        data = str(timeNow)
        ano = data[0:4]
        mes = data[5:7]
        dia = data[8:10]
        dataCompleta = dia + "/" + mes + "/" + ano
        anexo = "Anexos" + str(idOpt) + ".zip"
        arquivo = str(idOpt + ' - ' + nomeOpt + '.pdf')

        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO resumo_oportunidades(id, user, lista, id_oportunidade, data_abertura, "
                        "data_vencimento, horario, descricao, nome_arquivo, nome_anexo, create_date) VALUES(%s, %s, "
                        "%s, %s, %s, %s,%s, %s, %s, %s, %s)", ([self.id, self.username, self.titleList, idOpt,
                                                                inicPerCotacao[:10], fimPerCotacao[:10],
                                                                fimPerCotacao[-8:],nomeOpt[13:], arquivo,
                                                                anexo, dataCompleta]))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            print('Entrada Duplicada: ' + str(e))
