import csv

# REQUISITO 8:
# A classe Entrada recebe os parametros do modelo desenvolvido
# O metodo simplex_params converte a entrada para a forma padrão
# do simplex, construindo as colunas adicionais da matriz A por
# meio do big-M


M = 10**200 # valor do big M


class Entrada:

    preco_custo = []
    preco_venda = []
    quantidade_estoque = []
    quantidade_demanda = []
    codigo_produto = []
    nome_produto = []
    dinheiro_total = 0.0
    quantidade_produtos = 0

    # REQUISITO 1
    def simplex_params(self):

        n = self.quantidade_produtos
        n_vars = 3*n + 1

        c = [self.preco_custo[i] - self.preco_venda[i] for i in range(n)]
        c += [0 for i in range(n+1)]
        c += [M for i in range(n)]
        c = [c,]

        vars_base = [n] + [2*n+i+1 for i in range(n)]

        b = [[self.dinheiro_total] + [ self.quantidade_demanda[i] - self.quantidade_estoque[i] for i in range(n) ]]

        A = [
            self.preco_custo + [1] + [0 for i in range(2*n)],
        ]

        for i in range(n):
            v = [0 for i in range(n_vars)]
            v[i], v[n+i+1], v[2*n+i+1] = 1, -1, 1
            A.append(v)

        return A, b, c, vars_base

    def avalia_solucao_simplex(self, resultado, vars_base):

        vet = [0 for i in range(self.quantidade_produtos)]

        for n, i in enumerate(vars_base):
            if i < self.quantidade_produtos:
                vet[i] = int(resultado[n])

        return vet

    # REQUISITO 10
    def gera_relatorio(self, solucao, filepath='out.txt'):

        with open(filepath, 'w+') as outfile:
            outfile.write('você deverá comprar:\n')

            custo = 0
            lucro = 0

            for i, qtd in enumerate(solucao):
                outfile.write(f'{qtd:<7} {self.nome_produto[i]}.\n')

                custo += qtd * self.preco_custo[i]
                lucro += qtd * (self.preco_venda[i] - self.preco_custo[i])

            outfile.write(f'\nA compra tera um custo de R${custo:.2f}.\n')
            outfile.write(f'Restarão R${self.dinheiro_total - custo:.2f} ao final das compras.\n')
            outfile.write(f'O lucro esperado com a venda dos produtos é de R${lucro:.2f}.\n')


# REQUISITO 1
def read_entrada(filepath):

    entrada = Entrada()

    with open(filepath, 'r') as ficheiro:
        reader = csv.reader(ficheiro)
        for i, linha in enumerate(reader):
            # PRIMEIRA LINHA HEADER
            if i > 0 and linha[2] and linha[3] and linha[4] and linha[5]:
                entrada.codigo_produto.append(linha[0])
                entrada.nome_produto.append(linha[1])
                entrada.preco_custo.append(float(linha[2].replace(',', '.')))
                entrada.preco_venda.append(float(linha[3].replace(',', '.')))
                entrada.quantidade_estoque.append(int(linha[4]))
                entrada.quantidade_demanda.append(int(linha[5]))
            # LINHA DINHEIRO
            if linha[1] and not linha[2]:
                entrada.dinheiro_total = float(linha[1].replace(',', '.'))
        entrada.quantidade_produtos = len(entrada.codigo_produto)

    return entrada

