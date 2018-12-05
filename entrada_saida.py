import csv


class Entrada:

    def __init__(self, arquivo=None):
        """
        Variaveis necessarias para aplicacao do Simplex.

        Dado um indice N  pode ser obter: preco custo, preco de venda,
        quantidade em estoque, quantidade demanda, codigo produto,
        nome do produto.
        """
        self.preco_custo = []
        self.preco_venda = []
        self.quantidade_estoque = []
        self.quantidade_demanda = []
        self.codigo_produto = []
        self.nome_produto = []
        self.dinheiro_total = 0.0
        self.quantide_produtos = 0

        if arquivo:
            self.get_entrada(arquivo)

    def get_entrada(self, arquivo):
        """
        Dado um arquivo de entrada padronizado CSV
        onde:

        1 Linha = Header (codigo, nome, preco custo, preco venda, estoque, quantidade)
        n Linha = Informacoes de entrada
        Ultima linha = Duas celulas contendo label 'Dinheiro' na primeira
        e o valor do dinheiro na segunda.

        :param arquivo (formato csv):
        """
        with open('entrada.csv', 'r') as ficheiro:
            reader = csv.reader(ficheiro)
            for i, linha in enumerate(reader):
                # PRIMEIRA LINHA HEADER
                if i > 0 and linha[2] and linha[3] and linha[4] and linha[5]:
                    self.codigo_produto.append(linha[0])
                    self.nome_produto.append(linha[1])
                    self.preco_custo.append(float(linha[2].replace(',', '.')))
                    self.preco_venda.append(float(linha[3].replace(',', '.')))
                    self.quantidade_estoque.append(int(linha[4]))
                    self.quantidade_demanda.append(int(linha[5]))
                # LINHA DINHEIRO
                if linha[1] and not linha[2]:
                    self.dinheiro_total = float(linha[1].replace(',', '.'))
            self.quantide_produtos = len(self.codigo_produto)

