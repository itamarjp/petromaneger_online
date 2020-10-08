import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

data = []
nomeOportunidade = []
dataPublicacao = []
inicioCotacao = []
fimCotacao = []
tipoOportunidade = []
criterioAvaliacao = []
idOportunidade = []
arquivo = []
anexos = []


class sendEmails:

    def __init__(self, fromEmail, fromPwd, smtpServer, smtpPort, mailListFilter, downloadFolder, dadosOpts):
        self.fromEmail = fromEmail
        self.fromPwd = fromPwd
        self.smtpSesewlrver = smtpServer
        self.smtpPort = smtpPort
        self.smtpServer = smtpServer
        self.mailListFilter = mailListFilter
        self.downloadFolder = downloadFolder
        self.dadosOpts = dadosOpts
        self.index = 0

    def sendEmailsF(self):

        global attachment, fileName
        lenArquivos = len(self.dadosOpts)
        x = 0
        while x < lenArquivos:
            idOportunidade = self.dadosOpts[x]['id_oportunidade']
            descricao = self.dadosOpts[x]['descricao']
            dataColeta = self.dadosOpts[x]['create_date']
            dataAbertura = self.dadosOpts[x]['data_abertura']
            fimCotacao = (self.dadosOpts[x]['data_vencimento']) + " - " + (self.dadosOpts[x]['horario'])
            nomeAnexo = self.dadosOpts[x]['nome_anexo']
            arquivo = self.dadosOpts[x]['nome_arquivo']

            email_user = self.fromEmail
            email_password = self.fromPwd
            email_send = self.mailListFilter
            print(email_send)

            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = ', '.join(email_send)
            msg['Subject'] = 'Oportunidade Petronect: ' + '- ' + idOportunidade + " - " + descricao

            body = f"Srs,<p>Segue em anexo os dados da Oportunidade:</p>Coleta no Petronect: {dataColeta}" \
                   f"<br>Data da Abertura:  {dataAbertura}<br><strong>Fim do período de Cotação: {fimCotacao}" \
                   f" </strong><br>Nome no anexo: {nomeAnexo}" \
                   f"<p>Segue link para download dos anexos:<p>https://insaut-my.sharepoint.com/:f:/g/personal/insaut_insaut_onmicrosoft_com/EjEf2TriJlZFp4M6uD0T06QBuYiVtIFRXkVI0x4g4fsPyg?e=yIW2xs"

            msg.attach(MIMEText(body, 'html'))
            try:
                attachment = self.downloadFolder + "/" + arquivo
                print(attachment)

                fileName = str(arquivo)
                print(fileName)
            except:
                print('erro nas definições')
            try:
                attach_file = open(attachment, 'rb')
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attach_file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment", filename=fileName, )
                msg.attach(part)
                attach_file.close()
            except Exception as e:
                print('erro ao anexar oportunidade :' + str(e))
            text = msg.as_string()
            server = smtplib.SMTP(self.smtpServer, 587, timeout=240)
            server.starttls()
            server.login(email_user, email_password)
            server.sendmail(email_user, email_send, text)
            server.quit()
            x = x + 1
