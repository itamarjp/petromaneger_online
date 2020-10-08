from wtforms import Form, StringField, PasswordField, validators, TextAreaField


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


class setupForm(Form):
    usernamePet = StringField('Nome de Usuário Petronect', [validators.Length(min=1, max=25)])
    passwordPet = StringField('Password do Site Petronect', [validators.Length(min=1, max=25)])
    empresa = StringField('Nome da empresa Cadastrada no Petronect', [validators.Length(min=1, max=100)])
    fromEmail = StringField('Email que enviará as mensagens (Seu email)', [validators.Length(min=6, max=50)])
    fromPwd = StringField('Password do seu EMAIL', [validators.Length(min=1, max=25)])
    smtpServer = StringField('Servidor SMTP do seu EMAIL', [validators.Length(min=1, max=50)])
    smtpPort = StringField('Porta SMTP do Seu EMAIL (Geralmente 587)', [validators.Length(min=1, max=50)])
    mailList = StringField('Lista de emails de destino (separe por vírgula)', [validators.Length(min=6, max=500)])


class ArticleForm(Form):
    title = StringField('Nome da Lista', [validators.Length(min=1, max=50)])
    body = TextAreaField('IDs', [validators.Length(min=10)])
