import copy


class Matriz:
    """
    Classe que trata o tipo 'Matriz' com uma lista de listas
    e realiza as operações necessarias para o simplex.
    """

    def __init__(self, matriz=None):
        self.matriz = [] if not matriz else matriz

    def transposta(self):
        """Retorna a matriz transposta da self.matriz"""
        m_trans = []

        for j in range(len(self.matriz[0])):
            m_trans.append([])

        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[i])):
                m_trans[j].append(self.matriz[i][j])

        return m_trans

    def produto_escalar(self, escalar):
        """Retorna a matriz (self.matriz) multiplicada por
        um produto escalar"""
        m_prod = []

        for i in range(len(self.matriz)):
            m_prod.append([])
            for j in range(len(self.matriz[i])):
                m_prod[i].append((self.matriz[i][j]*escalar))

        return m_prod

    def __mul__(self, m2):
        """Retorna o produto matricial entre duas matrizes"""
        m_prod = []

        for i in range(len(self.matriz)):
            m_prod.append([])
            for j in range(len(m2.matriz[0])):
                soma = 0
                for k in range(len(self.matriz[0])):
                    soma += self.matriz[i][k] * m2.matriz[k][j]
                m_prod[i].append(soma)

        return m_prod

    def pivo(self, matriz):
        """TODO REMOVER ARGUMENTO MATRIZ, UTILIZAR SELF.MATRIZ"""
        maior = matriz[1][0]
        indice = 1
        n = len(matriz)
        for i in range(n):
            for j in range(n):
                if (i >= (j + 1)) and (abs(matriz[i][j]) > abs(maior)):
                    maior = matriz[i][j]
                    indice = i

        return indice

    def decLU(self, mat):
        """
        TODO REMOVER ARGUMENTO MATRIZ USAR PROPRIO SELF.MATRIZ
        TODO ARRUMAR OPERAÇÃO, PARECE NAO ESTAR FUNCIONANDO
        """
        matriz = copy.deepcopy(mat)
        pivot = []
        n = len(matriz)
        for i in range(n - 1, -1, -1):
            pivot.append(i)
        for j in range(n - 1):
            p = self.pivo(matriz)
            if (p != j):
                for k in range(n):
                    t = matriz[j][k]
                    matriz[j][k] = matriz[p][k]
                    matriz[p][k] = t
                m = pivot[j]
                pivot[j] = pivot[p]
                pivot[p] = m
            if (abs(matriz[j][j]) != 0):
                for i in range(j + 1, n):
                    mult = float(matriz[i][j] / matriz[j][j])
                    matriz[i][j] = mult
                    for k in range(j + 1, n):
                        matriz[i][k] = matriz[i][k] - (mult * matriz[j][k])

        up = []
        lo = []
        for i in range(n):
            up.append([])
            lo.append([])
            for j in range(n):
                if i == j:
                    up[i].append(matriz[i][j])
                    lo[i].append(1)
                elif i < j:
                    up[i].append(matriz[i][j])
                    lo[i].append(0)
                else:
                    lo[i].append(matriz[i][j])
                    up[i].append(0)

        return (up, lo, pivot)

    def subSucessPivotal(self,matriz, b, pivot):
        n = len(matriz)
        y = []
        for i in range(n):
            y.append(0)
        k    = pivot[0]
        y[0] = b[k]
        for i in range(1,n):
            soma = 0
            for j in range(i):
                soma += float(matriz[i][j]*y[j])
            k = pivot[i]
            y[i] = float(b[k] - soma)

        return y

    def subRetro(self,matriz,y):
        n = len(matriz)
        x = []
        for i in range(n):
            x.append(0)
        x[n-1] = float(y[n-1]/matriz[n-1][n-1])
        for i in range(n-2,-1,-1):
            soma = 0
            for j in range(i+1,n):
                soma += float(matriz[i][j]*x[j])
            x[i] = float(float(y[i]-soma)/matriz[i][i])

        return x

    def gaussJordan(self,mat):
        """
        TODO REMOVER MAT(USAR SELF.MATRIZ)
        TODO CONCERTAR FUNÇÃO (RESULTADO ERRADO)
        """

        matriz = copy.deepcopy(mat)
        m = len(matriz)
        n = len(matriz[0])
        for i in range(m-1):
            for j in range(i+1,m):
                mult = float(matriz[j][i]/matriz[i][i])
                for k in range(n):
                    matriz[j][k] -= float(mult*matriz[i][k])
        for i in range(m-1,0,-1):
            for j in range(i-1,-1,-1):
                mult = float(matriz[j][i]/matriz[i][i])
                for k in range(n):
                    matriz[j][k] -= float(mult*matriz[i][k])


        for i in range(m):
            for j in range(n):
                matriz[i][j] /= matriz[i][i]

        return matriz

    def __str__(self):
        return str(self.matriz)


if __name__ == '__main__':
    aux = [
        [1, 3, 5],
        [4, 3, 2],
        [5, 10, 5]
    ]

    aux2 = [
        [2, 2, 3],
        [3, 1, 2],
        [4, 4, 4]
    ]

    gaus = [
        [1, 3, 4, 3],
        [2, 7, 3, -7],
        [2, 8, 6, -4]
    ]

    m1 = Matriz(aux)
    m2 = Matriz(aux2)

    a,b,c = m1.decLU(aux)


    print("MATRIZ: "+str(gaus))
    print("RESULTADO GAUS: "+str(m1.gaussJordan(gaus)))