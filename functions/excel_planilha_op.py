import pandas as pd

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


class optToExcel:
    def __init__(self, idOportunidade, abertura, vencimento, horario, descr, pasta):
        self.idOportunidade = idOportunidade
        self.abertura = abertura
        self.vencimento = vencimento
        self.horario = horario
        self.descr = descr
        self.pasta = pasta

    def lerLinhasDoLog(self):
        file = open(self.pasta + "\\" + "pdf_py_log.txt", "r")
        number_of_lines = 0
        for line in file:
            line = line.strip("\n")
            number_of_lines += 1
        file.close()
        print(number_of_lines)
        number_opt_file = number_of_lines / 11
        cycles = number_opt_file
        count = 0
        linha = 9
        while count < cycles:  # lê o log e coleta os dados
            dataLinha = file.readlines()[linha - 9]
            nomeOportunidadeLinha = file.readlines()[linha - 8]
            dataPublicacaoLinha = file.readlines()[linha - 7]
            inicioCotacaoLinha = file.readlines()[linha - 6]
            fimCotacaoLinha = file.readlines()[linha - 5]
            tipoOportunidadeLinha = file.readlines()[linha - 4]
            criterioAvaliacaoLinha = file.readlines()[linha - 3]
            idOportunidadeLinha = file.readlines()[linha - 2]
            arquivoLinha = file.readlines()[linha - 1]
            anexoLinha = file.readlines()[linha - 0]
            if linha <= number_of_lines:
                linha = linha + 11
                count = count + 1
                data.insert(count, dataLinha.strip())
                nomeOportunidade.insert(count, nomeOportunidadeLinha.strip())
                dataPublicacao.insert(count, dataPublicacaoLinha.strip())
                inicioCotacao.insert(count, inicioCotacaoLinha.strip())
                fimCotacao.insert(count, fimCotacaoLinha.strip())
                tipoOportunidade.insert(count, tipoOportunidadeLinha.strip())
                criterioAvaliacao.insert(count, criterioAvaliacaoLinha.strip())
                idOportunidade.insert(count, idOportunidadeLinha.strip())
                arquivo.insert(count, arquivoLinha.strip())
                anexos.insert(count, anexoLinha.strip())  # ler# #
        print(number_opt_file)
        return (number_opt_file)

    def criaDic(self):
        dic = {'ID Oportunidade': [id[-11:] for id in idOportunidade],
               'Data Abertura': [data[-21:-11] for data in self.abertura],
               'Data Vencimento': [venc[-21:-11] for venc in self.vencimento],
               'Horario': [hr[-8:] for hr in self.horario],
               'Descrição': [n[35:] for n in self.descr]}
        return dic

    def dicToExcel(self):
        df = pd.DataFrame(data=dic)
        writer = pd.ExcelWriter('C:\\teste\\oportunidades.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()

    def criaDic(self):
        dic = {'ID Oportunidade': [id[-11:] for id in idOportunidade],
               'Data Abertura': [data[-21:-11] for data in self.abertura],
               'Data Vencimento': [venc[-21:-11] for venc in self.vencimento],
               'Horario': [hr[-8:] for hr in self.horario],
               'Descrição': [n[35:] for n in self.descr]}
        return dic
