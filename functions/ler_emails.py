import email
import imaplib
import os

import EmailProperties

listIds = []
listSubject = []
idUnico = []


def read_email():
    try:
        mail = imaplib.IMAP4_SSL(EmailProperties.SMTP_SERVER)
        mail.login(EmailProperties.FROM_EMAIL, EmailProperties.FROM_PWD)
        mail.select('inbox', readonly=False)

        type_mail, data = mail.search(None, f'(SINCE {EmailProperties.SINCE} SUBJECT "Oportunidade Publicada ID")')
        mail_ids = data[0]

        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        print("Reading emails from {} to {}.\n\n".format(latest_email_id, first_email_id))

        for i in range(first_email_id, latest_email_id + 1):
            typ, data = mail.fetch(str(i), '(RFC822)')
            for response_part in data:
                if not isinstance(response_part, tuple):
                    continue
                msg = email.message_from_string(response_part[1].decode('utf-8'))
                mail_str = str(msg)
                # Se e-mail não contém a estrutura que precisamos, não processa
                if mail_str.find('Oportunidade Publicada ID') <= 1:
                    continue
                email_subject = msg['subject']
                email_from = msg['from']
                email_date = msg['Date']
                sliceSubject = email_subject[-10:]
                print(sliceSubject)
                listIds.append(sliceSubject)
                listSubject.append(email_subject)
                print('From : ' + email_from + '\n')
                print('Subject : ' + email_subject + '\n')
                print('Date : ' + email_date + '\n')
                print('----------------------------------------------------------')
        mail.logout()
    except Exception as e:
        print(e)


def comparaEmailLog():
    with open('c:\\teste\\' + 'readEmails_py_log.txt', 'r') as arquivo:
        for id in arquivo:
            if ((id[-11:]).strip()) in listIds:
                print('id já incluso: ' + id)
            else:
                idUnico.append((id[-11:]).strip())


def log():
    with open('c:\\teste\\' + 'readEmails_py_log.txt', 'a') as arquivo:
        for id in listSubject:
            if ((id[-11:]).strip()) not in idUnico:
                idUnico.append((id[-11:]).strip())
                arquivo.write(str(id) + '\n')
            else:
                print('id já incluso: ' + id)
    arquivo.close()


def excluiLog():
    dir = os.listdir('c:\\teste\\')
    for file in dir:
        if file == "readEmails_py_log.txt":
            os.remove('c:\\teste\\' + file)


read_email()
excluiLog()
log()
# comparaEmailLog()


print(listIds)
print('----------------------------------------------------------')
print(listSubject)
print('----------------------------------------------------------')
print(idUnico)
