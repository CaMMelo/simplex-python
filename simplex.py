import entrada_saida
import matriz
import sys


SOLUCAO_INEXISTENTE = 1
SOLUCAO_ILIMITADA = 2
SOLUCAO_MULTIPLAS = 3
SOLUCAO_OTIMA = 4


class Simplex:
    
    def __init__(self, A, b, c, vars_base):
        
        self.A = A
        self.b = matriz.transp(b)
        self.c = c
        self.vars_base = vars_base
        
        # dimensões da matriz A
        self.n = len(A)
        self.m = len(A[0])
    
    def gera_base(self):

        self.B = [[0 for x in range(self.n)] for x in range(self.n)]
        self.c_base = [[ self.c[0][i] for i in self.vars_base ]]
        
        for i, linha in enumerate(self.A):
            for k, j in enumerate(self.vars_base):
                self.B[i][k] = linha[j]

        self.inv_B = matriz.inv(self.B)
    
    # requisito 3
    def solucao_basica_factivel(self):
        return matriz.prod_matricial(self.inv_B, self.b)
    
    # requisito 4
    def calcula_custo_reduzido(self, var):
        vetor_direcao = self.calcula_vetor_direcao(var)
        return self.c[0][var] + matriz.prod_matricial(self.c_base, vetor_direcao)[0][0]
    
    # requisito 5
    def calcula_vetor_direcao(self, var):
        vet = [[linha[var]] for linha in self.A]
        return matriz.prod_escalar(-1, matriz.prod_matricial(self.inv_B, vet))
    
    # requisito 6
    def calcula_theta(self, x_base, direcao):
        theta = float('inf')
        ind = -1

        d = matriz.transp(direcao)[0]
        x = matriz.transp(x_base)[0]

        for i, j, k in zip(self.vars_base, x, d):
            if k < 0:
                theta = min(theta, -j/k)
                ind = i
        
        return theta, ind
    
    def solve(self):

        self.gera_base()
        
        while True:

            # PASSO 1: calculando solução básica inicial
            x = self.solucao_basica_factivel()

            # PASSO 2: calcula custo reduzido dos indices não basicos
            variaveis_nao_basicas = [x for x in filter(lambda x: x not in self.vars_base, range(self.m))]
            custo_reduzido = [self.calcula_custo_reduzido(v) for v in variaveis_nao_basicas]

            j = [x for x in zip(variaveis_nao_basicas, custo_reduzido)]
            j = [x for x in filter(lambda x: x[1] < 0, j)]

            try:
                j = min(j, key=lambda x: x[1])[0]
            except:
                self.resultado = matriz.transp(x)[0] # guarda a solução
                return SOLUCAO_OTIMA

            # PASSO 3: calcula vetor u
            direcao = self.calcula_vetor_direcao(j)

            if len([x for x in filter(lambda x: x[0] < 0, direcao)]) == 0:
                return SOLUCAO_ILIMITADA

            # PASSO 4: calcula theta
            theta, k = self.calcula_theta(x, direcao)

            # passo 5: mudança de base
            # REQUISITO 7
            for m, n in enumerate(self.vars_base):
                if n == k:
                    self.vars_base[m] = j

            self.vars_base.sort()

            self.gera_base()


if __name__ == '__main__':

    entrada = entrada_saida.read_entrada(sys.argv[1])

    A, b, c, v = entrada.simplex_params()

    simp = Simplex(A, b, c, v)

    result = simp.solve()


    # REQUISITO 8/9
    if result == SOLUCAO_INEXISTENTE:
        print('NAO FOI POSSIVEL RESOLVER O SISTEMA')
    elif result == SOLUCAO_ILIMITADA:
        print('O SISTEMA POSSUI SOLUÃO ILIMITADA')
    elif result == SOLUCAO_MULTIPLAS:
        print('O SISTEMA POSSUI MULTIPLAS SOLUÇÕES')
    elif result == SOLUCAO_OTIMA:
        print('SOLUÇÃO OTIMA ENCONTRADA')
        resultado = entrada.avalia_solucao_simplex(simp.resultado, simp.vars_base)
        entrada.gera_relatorio(resultado, sys.argv[2])