import sys

alfabetol = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N',
             'Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z']

'''
Función que convierte un texto dado y devuelve el texto pero con los indices de 
cada letra correspondiente
'''
def convierteTexto(texto):
	#convertimos a cada letra del texto en un arreglo
        listaIndiceTexto = list(texto)
	#lista que contiene los indeces del texto (la igualamos a list(texto) para que tubiera la misma longitud
	#que el arreglo de caracteres)
        listaIndex = list(texto)
        for i in range(len(listaIndiceTexto)):
                listaIndex[i] = alfabetol.index(listaIndiceTexto[i])
        return listaIndex

'''
Función que crea nuestra matriz, está dada por listas de listas.
'''
def crea(l, n, m):
        mtx = []
        c = 0
        for i in range(n):
                lAux = []
                for j in range(m):
                        lAux.append(l[c])
                        c = c + 1
                mtx.append(lAux)
        return mtx

'''
Función que multiplica dos matrices, sacamos el módulo que es nuestro alfabeto.
'''
def multiplica(A, B):
        n = len(B)
        m = len(B[0])
        
        C=[[0 for j in range(m)] for i in range(n)]

        for h in range(len(C)):
                for i in range(len(A)):
                        a = 0
                        for j in range(len(B[0])):
                             a = a + A[i][j] * B[h][j]
                        C[h][i] = a%27
        return C

'''
Función que cifra el mensaje dada una matriz.
'''
def cifrado(m):
        s = ''
        for i in range(len(m)):
                for j in range(len(m[0])):
                        s = s + alfabetol[m[i][j]]
        return s

'''
Función que obtiene el inverso modular de un número.
'''
def inversoMod(a, b):
        for i in range(b):
                if (((i*a)%b) == 1):
                        return i
        return -1

'''
Función que calcula el determinante de una matriz de 2x2.
'''
def determinante(m):
        d = (m[0][0]*m[1][1])-(m[0][1]*m[1][0])
        return d%27
        
'''
Función que obtiene la adjunta de una matriz de 2x2.
'''
def adjunta(m):
        ad = [[0,0],[0,0]]
        ad[0][0] = m[1][1]
        ad[1][1] = m[0][0]
        ad[1][0] = m[1][0]*-1
        ad[0][1] = m[0][1]*-1
        return ad

'''
Función que obtiene la inversa de una matriz de 2x2.
'''
def inversa22(m):
        d = determinante(m)
        im = inversoMod(d,27)
        inv = [[0,0],[0,0]]
        adj = adjunta(m)
        inv[0][0] = adj[0][0]*im%27
        inv[0][1] = adj[0][1]*im%27
        inv[1][0] = adj[1][0]*im%27
        inv[1][1] = adj[1][1]*im%27
        return inv

'''
Función que obtiene la inversa de una matriz de 3x3, a mano porque no pudimos
implementar para nxn.
'''
def inversa33(m):
        c = [[0,0,0],[0,0,0],[0,0,0]]
        d=((m[0][0]   * ((m[1][1] * m[2][2]) - (m[1][2] * m[2][1])))-
              (m[0][1]* ((m[1][0] * m[2][2]) - (m[2][0] * m[1][2])))+
              (m[0][2]* ((m[1][0] * m[2][1]) - (m[2][0] * m[1][1]))));
        de = inversoMod(d,27)
        if (de != 0):
                u=(((m[1][1]  * m[2][2] - m[2][1] * m[1][2])) * de);
                v=((-(m[1][0] * m[2][2] - m[2][0] * m[1][2])) * de);
                w=((m[1][0]   * m[2][1] - m[2][0] * m[1][1])) * de;
                x=(-(m[0][1]  * m[2][2] - m[2][1] * m[0][2])) * de;
                y=((m[0][0]   * m[2][2] - m[2][0] * m[0][2])) * de;
                z=(-(m[0][0]  * m[2][1] - m[2][0] * m[0][1])) * de;
                r=((m[0][1]   * m[1][2] - m[1][1] * m[0][2])) * de;
                s=(-(m[0][0]  * m[1][2] - m[1][0] * m[0][2])) * de;
                t=((m[0][0]   * m[1][1] - m[1][0] * m[0][1])) * de;
                c[0][0]=int(u)%27;
                c[0][1]=int(x)%27;
                c[0][2]=int(r)%27;
                c[1][0]=int(v)%27;
                c[1][1]=int(y)%27;
                c[1][2]=int(s)%27;
                c[2][0]=int(w)%27;
                c[2][1]=int(z)%27;
                c[2][2]=int(t)%27;
                return c
        else:
                return None

'''
Función recursiva que calcula el máximo común divisor de dos números.
'''
def mcd(a, b):
        if (b == 0):
                return a
        else:
                return mcd(b, a%b)

'''
Función que cifra un mensaje de una matriz de 2x2.
'''
def cifra22(t,k):
        arrayC = convierteTexto(k)
        arrayT = convierteTexto(t)
        matC = crea(arrayC,2,2)
        det = determinante(matC)
        matM = crea(arrayT,int(len(t)/2),2)
        if (mcd(int(det), 27)) == 1:
                return cifrado(multiplica(matC, matM))
        return "No se puede invertir"
        
'''
Función que cifra un mensaje de una matriz de 3x3. No pudimos hacerlo general.
'''
def cifra33(t,k):
        arrayC = convierteTexto(k)
        arrayT = convierteTexto(t)
        matC = crea(arrayC,3,3)
        matM = crea(arrayT,int(len(t)/3),3)
        return cifrado(multiplica(matC, matM))

'''
Función que decifra un mensaje dada una clave para una matriz de 2x2.
'''
def descifra22(t,k):
        arrayC = convierteTexto(k)
        arrayT = convierteTexto(t)
        matll = crea(arrayC,2,2)
        inv = inversa22(matll)
        matM = crea(arrayT, int(len(arrayT)/2), 2)
        return cifrado(multiplica(inv, matM))

'''
Función que decifra un mensaje dada una clave para una matriz de 3x3.
'''
def descifra33(t,k):
        arrayC = convierteTexto(k)
        arrayT = convierteTexto(t)
        inv = inversa33(crea(arrayC,3,3))
        matM = crea(arrayT,int(len(arrayT)/3),3)
        return cifrado(multiplica(inv, matM))

'''
Lógica del programa, pide un argumento. Y luego los datos
C para cifrar.
D para descifrar.
'''
def main():
        '''
        Galeana Araujo Emiliano
        Jardines Mendoza César Eduardo
        Sánchez de la Rosa César Gustavo
        '''
        if (len(sys.argv) < 2):
                print('Faltan argumentos')
                exit()
                
        if (sys.argv[1] == 'C'):
                c = input('Ingrese la clave...')
                m = input('Ingrese el mensaje... ')
                print('El mensaje cifrado, es el siguiente')
                texto = convierteTexto(c)
                if (len(texto) == 9):
                        print(cifra33(m,c))
                elif (len(texto) == 4):
                        print(cifra22(m,c))
                else:
                        print('Intenta con una contraseña válida.')
                        exit()
                                
        elif (sys.argv[1] == 'D'):
                c = input('Ingrese la clave...')
                m = input('Ingrese el mensaje... ')
                print('El mensaje cifrado, es el siguiente')
                texto = convierteTexto(c)
                if (len(texto) == 9):
                        print(descifra33(m,c))
                else:
                        print(descifra22(m,c))       
                                
        else:
                print('Error, bandera inválida, pruebe con:')
                print('C - para cifrar')
                print('D - para descifrar')


main()
