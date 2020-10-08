from datetime import datetime


class comparaDataHora:
    def __init__(self, data_vencimento, horario):
        self.data_vencimento = data_vencimento
        self.horario = horario

    def compara(self):
        vencimento = datetime.strptime((self.data_vencimento + ' ' + self.horario), '%d.%m.%Y %H:%M:%S')
        dataHoraAtuais = datetime.now()
        print(vencimento)
        print(dataHoraAtuais)
        if vencimento > dataHoraAtuais:
            print('processo em aberto')
            liberaDownloadPropostas = False
        else:
            print('processo fechado, baixar propostas')
            liberaDownloadPropostas = True
        return liberaDownloadPropostas


data_vencimento = '22.06.2020'  # pegar do MYSQL
horario = '10:00:00'  # pegar do MYSQL
compara = comparaDataHora(data_vencimento, horario)
liberaDownloadPropostas = compara.compara()
print(liberaDownloadPropostas)
