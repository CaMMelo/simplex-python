import copy


# REQUISITO 2
# matrizes são vetores de vetores
# operações seguem abaixo

def gera_identidade(n):
	return [[int(x == y) for x in range(n)] for y in range(n)]

def fatora_lu(A):

	U = copy.deepcopy(A)
	n = len(A)
	L = gera_identidade(n)

	for j in range(n-1):
		for i in range(j+1, n):
			L[i][j] = U[i][j]/U[j][j]
			for k in range(j+1, n):
				U[i][k] -= L[i][j]*U[j][k]
			U[i][j] = 0

	return L, U

def inv(A):

	A = copy.deepcopy(A)
	m = len(A)
	n = 2*m

	I = gera_identidade(m)

	for i, j in enumerate(A):
		j += I[i]

	for i in range(m):
		maxvalor = i
		for k in range(i+1,m):
			if abs(A[k][i])>abs(A[maxvalor][i]):
				maxvalor = k
		A[i],A[maxvalor] = A[maxvalor],A[i]
		if abs(A[i][i]) <= 0:
			raise Exception('Matriz singular.')
		for k in range(i+1,m):
			c=A[k][i]/A[i][i]
			for x in range(i,n):
				A[k][x] -= A[i][x]*c
	for i in range(m-1,-1,-1):
		c=A[i][i]
		for k in range(i):
			for j in range(n-1,i-1,-1):
				A[k][j] -= A[i][j]*A[k][i]/c
		A[i][i] /= c
		for k in range(m,n):
			A[i][k] /= c
	

	for linha in A:
		for i in range(m):
			del linha[0]

	return A

def transp(A):
	return [[x[i] for x in A] for i in range(len(A[0]))]

def prod_escalar(alpha, A):
	return [[alpha * x for x in linha] for linha in A]

def prod_matricial(A, B):
	m = len(A)
	k = len(B)
	n = len(B[0])

	mat = []

	for i in range(m):
		vet = []
		for j in range(n):
			soma = 0
			for x in range(k):
				soma += A[i][x]*B[x][j]
			vet.append(soma)
		mat.append(vet)

	return mat

	return [[sum([A[i][x]*B[x][j] for x in range(k)]) for j in range(n)] for i in range(m)]