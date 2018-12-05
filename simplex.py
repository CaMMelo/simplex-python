from entrada_saida import Entrada
from matriz import Matriz


class Simplex:
    def __init__(self, arquivo):
        self.entrada = Entrada(arquivo)
        self.vetor_c = []
        self.vetor_b = []
        self.matriz_a = []
        self.vars = [0 for x in range(self.entrada.quantide_produtos)]

        self.vars_base = []

        self.build()

    def build(self):
        """
        Gera a matriz A e o vetor B
        """
        qtd_vars = 3*self.entrada.quantide_produtos+1
        n = self.entrada.quantide_produtos

        # VETOR C
        for i in range(0, self.entrada.quantide_produtos):
            self.vetor_c.append(self.entrada.preco_custo[i] - self.entrada.preco_venda[i])

        aux = [0 for i in range(0,n+1)]
        self.vetor_c += aux

        aux = [100000 for i in range(0,n)]
        self.vetor_c += aux

        # primeira linha
        # restrição dinheiro
        aux = []
        aux += self.entrada.preco_custo
        aux += [1]
        aux += [0 for x in range(0, 2*n)]

        self.vetor_b.append(self.entrada.dinheiro_total)
        self.matriz_a.append(aux)

        # calcular base inicial
        self.vars_base.append(n)

        # restricao de demanda
        for i in range(0, n):
            aux = [0 for x in range(0, 3 * n + 1)]
            aux[i] = 1
            aux[n+i] = -1
            aux[2*n+i] = 1

            self.vars_base.append(2*n+i)
            self.vetor_b.append(self.entrada.quantidade_demanda[i] - self.entrada.quantidade_estoque[i])

            self.matriz_a.append(aux)


if __name__ == '__main__':
    s = Simplex('entrada.csv')
    print(s.matriz_a)
    print(s.vars_base)