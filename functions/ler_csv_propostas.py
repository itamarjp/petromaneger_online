import mysql.connector
import pandas as pd
from flask import Flask
from flask_mysqldb import MySQL
import os

from models import db_config

app = Flask(__name__)

if os.environ.get("MODE") == 'production':
    app.config['MYSQL_HOST'] = db_config.CLEAR_DB_MYSQL_HOST
    app.config['MYSQL_USER'] = db_config.CLEAR_DB_MYSQL_USER
    app.config['MYSQL_PASSWORD'] = db_config.MYSQL_PASSWORD
    app.config['MYSQL_DB'] = db_config.CLEAR_DB_MYSQL_DB
    app.config['MYSQL_CURSORCLASS'] = db_config.MYSQL_CURSORCLASS
    app.config['FLASK_DEBUG'] = 0
else:
    app.config['MYSQL_HOST'] = db_config.MYSQL_HOST
    app.config['MYSQL_USER'] = db_config.MYSQL_USER
    app.config['MYSQL_PASSWORD'] = db_config.MYSQL_PASSWORD
    app.config['MYSQL_DB'] = db_config.MYSQL_DB
    app.config['MYSQL_CURSORCLASS'] = db_config.MYSQL_CURSORCLASS
    app.config['FLASK_DEBUG'] = 1

mysql = MySQL(app)


def leCsv(csv, sort):
    try:
        leCsv = pd.read_csv(csv, encoding='ANSI', sep=';', header=None)
        leCsv = leCsv.drop(0)
        leCsv[7] = leCsv[7].astype(float)
        is_value = leCsv[7] != 0
        is_value = leCsv[is_value]
        sort = is_value.sort_values([1, 7], ascending=[True, False])
    except:
        print('erro na converssão do arquivo: ' + csv)

    return sort


def classifica(sort, user, idList, id, empresa):
    global busca, secMenor
    resultado = ''
    empSecMenorValor = ''
    sBusca = ''
    margem = 0
    try:
        busca = set(sort[1])
        sBusca = sorted(busca)
    except Exception as e:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE resumo_oportunidades SET func_classifica = 'arq_n_encontrado' WHERE "
                    "id_oportunidade = %s", [id])
        mysql.connection.commit()
        cur.close()
        print('Arquivo inexistente: ' + str(e))
    for i in sBusca:
        f = sort[sort[1] == i]
        descItem = f[3]
        indexMax = f[7].idxmax()
        maxValue = f[7][indexMax]
        empMaxV = f[10][indexMax]
        indexMin = f[7].idxmin()
        minValue = f[7][indexMin]
        empMinV = f[10][indexMin]
        try:
            secMenor = f[7].nsmallest(2).iloc[-1]
            indexSecMenor = f[7].nsmallest(2)
            indexSecMenor = indexSecMenor.index
            empSecMenorValor = f[10][indexSecMenor[1]]
        except:
            pass
        isCompany = f[f[10].str.contains(empresa)][7]
        companyIndex = isCompany.index.values.tolist()
        companyValue = 0
        companyPercent = 1
        try:
            companyValue = f[7][companyIndex[0]]
            companyPercent = round((minValue / companyValue), 2)
            if companyPercent == 1:
                resultado = 'Teve Menor Valor'
                companyPercent = round((companyPercent), 2)
                margem = round((1 - (companyValue / secMenor)), 2)
            else:
                resultado = 'Perdeu por Preço'
        except:
            resultado = 'Não Participou do ítem'
        if margem == 0:
            empSecMenorValor = 'S/Concorrentes'
            secMenor = 0
        companyPercent = round(companyPercent, 2)
        companyPercent = float(companyPercent)

        try:
            cur = mysql.connection.cursor()
            cur.execute(f"INSERT INTO classifica(unique_key, id_lista, Oportunidade, item, descricao, emp_menor_valor, "
                        f"menor_valor, empr_seg_men_val, seg_men_val, emp_maior_val, maior_valor, "
                        f"valor_sua_empresa, res_percentual, status_sua_empresa, margem_seg_menor_valor, user) VALUES "
                        f"('{id + i}','{idList}','{id}','{i}','{descItem}','{empMinV}','{minValue}','"
                        f"{empSecMenorValor}','{secMenor}','{empMaxV}','{maxValue}','{companyValue}',"
                        f"'{round(((1 - companyPercent) * 100), 2)}','{resultado}','{margem}','{user}')")
            cur.execute("UPDATE resumo_oportunidades SET func_classifica = 'analisado' WHERE "
                        "id_oportunidade = %s AND user = %s", [id, user])
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            print(str(e))
