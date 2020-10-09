from datetime import datetime
from functools import wraps
import mysql.connector
from flask import flash, redirect, url_for, session, request, render_template
from functions import enviar_emails, petronect_selenium_process
from functions.exporta_propostas import *
from functions.petronect_selenium_process import *
from models import db_config
from models.forms import setupForm, RegisterForm, ArticleForm
import os

print(os.environ.get("MODE"))

app = Flask(__name__)

if os.environ.get("MODE") == 'production':
    app.config['MYSQL_HOST'] = db_config.CLEAR_DB_MYSQL_HOST
    app.config['MYSQL_USER'] = db_config.CLEAR_DB_MYSQL_USER
    app.config['MYSQL_PASSWORD'] = db_config.MYSQL_PASSWORD
    app.config['MYSQL_DB'] = db_config.CLEAR_DB_MYSQL_DB
    app.config['MYSQL_CURSORCLASS'] = db_config.MYSQL_CURSORCLASS
    app.config['FLASK_DEBUG'] = 0
    app.config['SECRET_KEY'] = 'secret_key_123'
else:
    app.config['MYSQL_HOST'] = db_config.MYSQL_HOST
    app.config['MYSQL_USER'] = db_config.MYSQL_USER
    app.config['MYSQL_PASSWORD'] = db_config.MYSQL_PASSWORD
    app.config['MYSQL_DB'] = db_config.MYSQL_DB
    app.config['MYSQL_CURSORCLASS'] = db_config.MYSQL_CURSORCLASS
    app.config['FLASK_DEBUG'] = 1
    app.config['SECRET_KEY'] = 'secret_key_123'

mysql = MySQL(app)


def sensor():
    exportaPropostas = []
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, user, lista, id_oportunidade, realizar_download FROM resumo_oportunidades")
        data = cur.fetchall()
        cur.close()
        nrows = len(data)
        x = 0
        while x < nrows:
            if data[x]['realizar_download'] == 'True':
                exportaPropostas.append(data[x])
            x = x + 1
        print(exportaPropostas)
        print("Scheduler is alive!")

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))

    return wrap


@app.route('/setup', methods=['GET', 'POST'])
@is_logged_in
def setup():
    global fromEmail

    username = (session['username'])
    form = setupForm(request.form)
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM users WHERE username = '{username}'")
    data = cur.fetchall()
    cur.close()
    user = data[0]['usernamePet']
    passwordPet = data[0]['passwordPet']
    empresa = data[0]['empresa']
    fromEmail = data[0]['fromEmail']
    fromPwd = data[0]['fromPwd']
    smtpServer = data[0]['smtpServer']
    smtpPort = data[0]['smtpPort']
    mailList = data[0]['mailList']

    if request.method == 'POST' and form.validate():
        usernamePet = form.usernamePet.data
        passwordPet = form.passwordPet.data
        empresa = form.empresa.data
        fromEmail = form.fromEmail.data
        fromPwd = form.fromPwd.data
        smtpServer = form.smtpServer.data
        smtpPort = form.smtpPort.data
        mailList = form.mailList.data

        cur = mysql.connection.cursor()
        query = """Update users set usernamePet= %s, 
                    passwordPet = %s, 
                    empresa = %s,
                    fromEmail = %s,
                    fromPwd = %s ,
                    smtpServer = %s ,
                    smtpPort = %s, 
                    mailList = %s
                    where username = %s"""
        username = session['username']
        input = (usernamePet, passwordPet,
                 empresa, fromEmail,
                 fromPwd, smtpServer,
                 smtpPort, mailList,
                 username)
        cur.execute(query, input)
        mysql.connection.commit()
        cur.close()
        flash('Setup Salvo Com Sucesso', 'success')
        return redirect(url_for('dashboard'))
    return render_template('setup.html', form=form, user=user, fromEmail=fromEmail, smtpServer=smtpServer,
                           smtpPort=smtpPort, mailList=mailList, passwordPet=passwordPet, fromPwd=fromPwd,
                           empresa=empresa)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/about')
@is_logged_in
def about():
    return render_template('downloadInProgress.html')


@app.route('/articles')
@is_logged_in
def articles():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()
    cur.close()
    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)


@app.route('/register_route', methods=['GET', 'POST'])
def register_route():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
                        (name, email, username, password))
            mysql.connection.commit()
            cur.close()
            flash('Registro feito com sucesso!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Usuário já existe!', 'danger')
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)


@app.route('/article/<string:id>/')
@is_logged_in
def article(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get article
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    article = cur.fetchone()
    return render_template('listaDash.html', article=article)


@app.route('/login', methods=['GET', 'POST'])
def login():
    print('login')
    if request.method == 'POST':
        username = request.form['username']
        print('username: ' + username)
        password_candidate = request.form['password']
        print('passqord :' + password_candidate)
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        if result > 0:
            data = cur.fetchone()
            print('data: ' + str(data))
            password = data['password']

            if password_candidate == password:
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('Você está logado!', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection

        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('Logout feito com sucesso!', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles WHERE author = %s ORDER BY create_date DESC", [session['username']])
    articles = cur.fetchall()
    cur.close()
    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)


@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)", (title, body, session['username']))
        mysql.connection.commit()
        cur.close()
        flash('Lista Criada', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form=form)


@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    username = (session['username'])
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    article = cur.fetchone()
    cur.close()
    form = ArticleForm(request.form)
    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        cur = mysql.connection.cursor()
        app.logger.info(title)
        cur.execute("UPDATE articles SET title=%s, body=%s WHERE id=%s AND author = %s", [title, body, id, username])
        mysql.connection.commit()
        cur.close()
        flash('Lista Atualizada', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_article.html', form=form)


@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id): #alterar o query para deletar apenas os Ids do usuário logado, incluir o usuário na planilha de classifica
    username = (session['username'])
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM articles WHERE id = %s AND author = %s", [id, username])
    cur.execute("DELETE FROM resumo_oportunidades WHERE id = %s AND user = %s", [id, username])
    cur.execute("DELETE FROM classifica WHERE Oportunidade = %s AND user = %s", [id, username])
    mysql.connection.commit()
    cur.close()

    flash('Lista de IDs Deletada', 'success')
    return redirect(url_for('dashboard'))


# @app.route('/enviarEmails', defaults={'id': 'No Id'})
@app.route('/listIds/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def listIds(id):
    global resultListIds, titleListFilter, idArticles
    idArticles = id
    resultListIds = []
    cur = mysql.connection.cursor()
    search = f"select * from articles where id = {id}"
    cur.execute(search)
    records = cur.fetchall()
    cur.close()
    list = records[0]['body']
    titleList = records[0]['title']
    titleListFilter = titleList.replace("/", '_')

    filter = list.replace("\r\n", ",")
    filter1 = filter.replace(" ", "")
    listIds = filter1.split(",")
    listIds = [x for x in listIds if x]
    idsNotFound = petronect_selenium_process.iDsNaoEncontradas
    for i in listIds:
        try:
            resultListIds.append(i)
        except:
            pass
    resultListIds = set(resultListIds)
    if request.method == 'POST':
        baixar_anexos = request.form['baixar_anexos']
        print(str(baixar_anexos))
        return redirect(url_for('download', id=id, baixar_anexos=baixar_anexos))
    return render_template('listIds.html', listIds=resultListIds, idsNotFound=idsNotFound, titleList=titleList,
                           idList=id)


@app.route('/downloadInProgress', methods=['GET', 'POST'])
@is_logged_in
def download():
    id = request.args.get('id')
    baixar_anexos = request.args.get('baixar_anexos')
    username = (session['username'])
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM users WHERE username = '{username}'")
    data = cur.fetchall()
    cur.close()
    user = data[0]['usernamePet']
    passwordPet = data[0]['passwordPet']

    downloadFilesProcess(resultListIds, user, passwordPet, username, titleListFilter, idArticles, id, baixar_anexos)
    cur = mysql.connection.cursor()
    resumo = f"SELECT * from resumo_oportunidades where id = '{id}'"
    cur.execute(resumo)
    records = cur.fetchall()
    cur.close()
    return render_template('downloadInProgress.html', records=records)


@app.route('/enviarEmails/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def enviarEmails(id):
    username = (session['username'])
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM users WHERE username = '{username}'")
    data = cur.fetchall()
    cur.close()
    fromEmail = data[0]['fromEmail']
    fromPwd = data[0]['fromPwd']
    smtpServer = data[0]['smtpServer']
    smtpPort = data[0]['smtpPort']
    mailList = data[0]['mailList']
    mailListFilter = mailList.split(',')

    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM articles WHERE id = '{id}'")
    dataFolder = cur.fetchall()
    cur.execute(f"SELECT nome_arquivo, descricao,id_oportunidade, create_date,data_abertura, data_vencimento,"
                f"horario ,nome_anexo FROM resumo_oportunidades WHERE id = '{id}'")
    dadosOpts = cur.fetchall()
    print(dadosOpts)
    cur.close()
    downloadFolder = dataFolder[0]['downloadFolder']

    if request.method == 'POST':
        send = enviar_emails.sendEmails(fromEmail, fromPwd, smtpServer, smtpPort, mailListFilter, downloadFolder,
                                        dadosOpts)
        send.sendEmailsF()
        for i in dadosOpts:
            file = downloadFolder + "\\" + i['nome_arquivo']
            os.remove(file)

        flash('Emails Enviados!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('enviarEmails.html', fromEmail=fromEmail, mailList=mailListFilter)


@app.route('/listaDash/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def listaDash(id):
    cur = mysql.connection.cursor()
    resumo = f"SELECT * from resumo_oportunidades where id = '{id}'"
    cur.execute(resumo)
    records = cur.fetchall()
    cur.close()
    if records != ():
        return render_template('listaDash.html', records=records)
    else:
        msg = 'Nenhuma oportunidade encontrada!'
        return render_template('listaDash.html', msg=msg)


class comparaDataHora:
    def __init__(self, data_vencimento, horario):
        self.data_vencimento = data_vencimento
        self.horario = horario

    def compara(self):
        vencimento = datetime.strptime((self.data_vencimento + ' ' + self.horario), '%d.%m.%Y %H:%M:%S')
        dataHoraAtuais = datetime.now()
        if vencimento > dataHoraAtuais:
            liberaDownloadPropostas = False
        else:
            liberaDownloadPropostas = True
        return liberaDownloadPropostas


@app.route('/resumoGeral')
@is_logged_in
def resumoGeral():
    cur = mysql.connection.cursor()
    username = (session['username'])
    resumo = f"SELECT lista,id_oportunidade,descricao,data_abertura,data_vencimento,horario FROM resumo_oportunidades WHERE user  = '{username}'"
    cur.execute(resumo)
    records = cur.fetchall()
    print(records)
    for i in records:
        data_vencimento = i['data_vencimento']  # pegar do MYSQL
        horario = i['horario']  # pegar do MYSQL
        compara = comparaDataHora(data_vencimento, horario)
        liberaDownloadPropostas = compara.compara()
        if liberaDownloadPropostas == True:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE resumo_oportunidades SET realizar_download=%s WHERE id_oportunidade = %s",
                        (['True', i['id_oportunidade']]))
            mysql.connection.commit()
        else:
            cur.execute("UPDATE resumo_oportunidades SET realizar_download=%s WHERE id_oportunidade = %s",
                        (['False', i['id_oportunidade']]))
            mysql.connection.commit()
    cur = mysql.connection.cursor()
    username = (session['username'])
    resumo = f"SELECT lista,id_oportunidade,descricao,data_abertura,data_vencimento,horario FROM resumo_oportunidades WHERE user  = '{username}'"
    cur.execute(resumo)
    records = cur.fetchall()
    cur.close()

    res = []
    for idx, sub in enumerate(records, start=0):
        if idx == 0:
            res.append(list(sub.values()))
        else:
            res.append(list(sub.values()))

    if records != ():
        return render_template('resumoGeral.html', res=res)
    else:
        return render_template('resumoGeral.html', res=res)


@app.route('/propostas', methods=['GET', 'POST'])
@is_logged_in
def propostas():
    listIds = []

    cur = mysql.connection.cursor()
    username = (session['username'])
    resumo = f"SELECT lista,id_oportunidade,descricao,data_abertura,data_vencimento,horario FROM resumo_oportunidades WHERE user  = '{username}'"
    cur.execute(resumo)
    records = cur.fetchall()
    print(records)
    for i in records:
        data_vencimento = i['data_vencimento']  # pegar do MYSQL
        horario = i['horario']  # pegar do MYSQL
        compara = comparaDataHora(data_vencimento, horario)
        liberaDownloadPropostas = compara.compara()
        if liberaDownloadPropostas == True:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE resumo_oportunidades SET realizar_download=%s WHERE id_oportunidade = %s",
                        (['True', i['id_oportunidade']]))
            mysql.connection.commit()
        else:
            cur.execute("UPDATE resumo_oportunidades SET realizar_download=%s WHERE id_oportunidade = %s",
                        (['False', i['id_oportunidade']]))
            mysql.connection.commit()

    cur = mysql.connection.cursor()
    username = (session['username'])
    resumo = f"SELECT lista,id,id_oportunidade,user,descricao,data_abertura,data_vencimento,horario " \
             f"FROM resumo_oportunidades WHERE user = '{username}'  " \
             f"AND caminho_proposta IS NULL AND realizar_download = 'True' " \
             f"AND proposta_baixada IS NULL"
    cur.execute(resumo)
    records1 = cur.fetchall()
    print(records1)
    user = f"SELECT *  FROM users WHERE username = '{username}'"
    cur.execute(user)
    userData = cur.fetchall()
    cur.close()
    loginPetronect = userData[0]['usernamePet']
    SenhaPetronect = userData[0]['passwordPet']
    empresa = userData[0]['empresa']
    x = 0
    if request.method == 'POST':
        downloadPropostasProcess(records1, loginPetronect, SenhaPetronect, username, empresa)

        cur = mysql.connection.cursor()
        username = (session['username'])
        resumo = f"SELECT * FROM resumo_oportunidades WHERE user = '{username}'  AND  proposta_baixada = 'True'"
        cur.execute(resumo)
        records2 = cur.fetchall()
        cur.close()

        flash('Download das propostas Completo', 'success')
        return render_template('downloadInProgress.html', records=records2)

    if records1 != ():
        res = []
        for idx, sub in enumerate(records1, start=0):
            if idx == 0:
                res.append(list(sub.values()))
            else:
                res.append(list(sub.values()))
        return render_template('propostas.html', records=records1)
    else:
        msg = 'Nenhuma oportunidade encontrada!'
        return render_template('propostas.html', msg=msg)


@app.route('/classificacao/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def classificacao(id):
    cur = mysql.connection.cursor()
    username = (session['username'])
    resumo = f"SELECT Oportunidade, item, descricao, " \
             f"emp_menor_valor, menor_valor, emp_maior_val," \
             f" maior_valor, res_percentual, status_sua_empresa, " \
             f"margem_seg_menor_valor FROM classifica WHERE user = '{username}' and Oportunidade = '{id}'"
    cur.execute(resumo)
    records = cur.fetchall()
    cur.close()

    res = []
    for idx, sub in enumerate(records, start=0):
        if idx == 0:
            res.append(list(sub.values()))
        else:
            res.append(list(sub.values()))
    print(res)

    return render_template('classificacao.html', res=res)


@app.route('/classificageral')
@is_logged_in
def classificageral():
    cur = mysql.connection.cursor()
    username = (session['username'])
    resumo = f"SELECT Oportunidade, item, descricao, emp_menor_valor, menor_valor, emp_maior_val, maior_valor, " \
             f"res_percentual, status_sua_empresa, margem_seg_menor_valor FROM classifica WHERE user = '{username}' ORDER BY id_lista DESC"
    cur.execute(resumo)
    records = cur.fetchall()
    cur.close()

    res = []
    for idx, sub in enumerate(records, start=0):
        if idx == 0:
            res.append(list(sub.values()))
        else:
            res.append(list(sub.values()))

    print(res)
    return render_template('classificageral.html', res=res)


if __name__ == '__main__':
    app.run(debug=True)
