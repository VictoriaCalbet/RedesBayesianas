import pgmpy
import networkx
from pgmpy.models import BayesianModel
from pgmpy.inference import VariableElimination
import random
import numpy
import pgmpy.factors.discrete as pgmf  # Tablas de probabilidades condicionales y factores de probabilidad

'''
 Método para obtener el grafo.
 Parámetros: numero de filas, columnas y minas.
 Return: grafo construido
 '''


def obtener_grafo_minas(tam_filas, tam_colum, num_minas):
    minas = []
    x = bool(0)  # False
    grafo = []
    nmin = num_minas
    # generamos un grafo con x por defecto.
    for i in range(tam_filas):
        grafo.append([])
        for j in range(tam_colum):
            grafo[i].append((x))
    # mientras el numero de minas sea mayor que 0 calculámos el grafo con un valor en la variable x que se correcto
    while (nmin > 0):
        for p in range(0, num_minas):
            a = random.randint(0, tam_filas - 1)
            b = random.randint(0, tam_colum - 1)
            var = (a, b)
            # sacamos una casilla al azar, comprobamos que no la hayamos utilizado ya
            if var not in minas:
                if nmin > 0:
                    nmin -= 1
                    minas.append((a, b))
                    for i in range(len(grafo)):
                        for j in range(len(grafo[i])):
                            # del grafo obtenido al principio del método. recorremos hasta encontrar la casilla que portará la mina
                            if i == a and j == b:
                                # actuaizamos x a true
                                x = bool(1)
                                # actuaizamos la casilla
                                grafo[i][j] = (x)
    return grafo


'''
 Método que añade las aristas al método.
 Parámetros: array donde concatenará las aristas además de una posición concreta i,j
 Return: Array
 '''


def add_edge_model(res, i, j):
    x = str(i) + "," + str(j)  # Almacenamos en X la posicion i,j como una cadena
    res.append(('num_vecinos' + x, x))  # Creamos una arista entre num_vecinosx -> x
    res.append(('sum_vecinos' + x, x))  # Creamos una arista entre sum_vecinosx -> x
    return res


'''
 Método que crea el modelo.
 Parámetro número de :filas, columnas y minas del tablero del buscaminas
 Return: modelo bayesiano completo
'''


def create_model(tam_filas, tam_colum, num_minas):
    grafo = obtener_grafo_minas(tam_filas, tam_colum, num_minas)
    model = BayesianModel()
    p = []
    # Recorremos el grafo y obtenemos un array con los vertices que formarán una arista
    for i in range(len(grafo)):
        for j in range(len(grafo[i])):
            p = add_edge_model(p, i, j)

    model.add_edges_from(ebunch=p)  # Añadimos el array p como aristas al modelo
    model = add_tabular_cpd(model, grafo, tam_filas,
                            tam_colum)  # Define la tabla de distribución de probabilidad condicional del modelo
    return model


'''
 Calcula el número de vecinos que tiene una casilla i,j.
 Parámetros: posición de la casilla i,j número de filas y columnas.
 Return: integer con el número de vecinos
'''


def calcular_vecinos(i, j, tam_filas, tam_colum):
    if i == 0 and j == 0 or i == 0 and j == tam_colum - 1 or i == tam_filas - 1 and j == 0 or i == tam_filas - 1 and j == tam_colum - 1:
        vecinos = 3
        return vecinos
    elif i == 0 or j == 0 or i == tam_filas - 1 or j == tam_colum - 1:
        vecinos = 5
        return vecinos
    else:
        vecinos = 8
    return vecinos


'''
 Metodo para crear los distribución de probabilidad condicional.
 Parámetros = modelo, grado, numero de filas, numero de columnas
 Return modelo con la distribución añadida
'''


def add_tabular_cpd(model, grafo, tam_filas, tam_colum):
    for i in range(len(grafo)):
        for j in range(len(grafo[i])):
            vecinos = calcular_vecinos(i, j, tam_filas,
                                       tam_colum)  # Obtenemos el número de vecinos que tiene la casilla i,j
            nodo = str(i) + "," + str(j)  # Obtenemos el nodo como un string
            vec = vecinos + 1
            vec_s = vecinos * 5 + 1
            res = []
            vec_res = []
            t = 0
            # Calculamos la probabilidad de cada casilla según el número de vecinos y la suma de minas adyacentes.
            while t < vec:
                r = t / vecinos
                for it in range((vecinos * 5) + 1):
                    operacion = round(r + it / (vecinos * 5), 2)
                    res.append(operacion / 2)  # ya que hemos sumado dos probabilidades con rango 0-1 dividimos entre 2
                vec_res.append(1)
                t += 1
            vec_res = numpy.array(vec_res) / numpy.array(vec_res).sum(axis=0, keepdims=1)
            vec_res_sum = probabilidaSumaVecinos(vecinos)
            res_inv = list(reversed(res))
            casilla_CPD = pgmf.TabularCPD(nodo, 2, [res, res_inv], ['sum_vecinos' + nodo, 'num_vecinos' + nodo],
                                          [vec_s, vec])
            casilla_CPD_vecinos = pgmf.TabularCPD('num_vecinos' + nodo, vec, [vec_res])
            casilla_CPD_sumVecinos = pgmf.TabularCPD('sum_vecinos' + nodo, vec_s, [vec_res_sum])
            model.add_cpds(casilla_CPD, casilla_CPD_vecinos, casilla_CPD_sumVecinos)

    return model


'''
Método con el que obtendremos cuál es la casilla con menor probabilidad para encontrar mina, casilla que podremos clickear. 
Parámetros: modelo, evidencias con formáto: evidencias = [(i,j),num_vecinos,suma_vecinos]
Return: Diccionario con la siguiente casilla a clicar formato {nodo: probabilidad}
'''


def getBox(model, evidencias):
    dictResul = {}  # Diccionario que almacenará el nodo a clickear y la probabilidad de no obtener mina en ese nodo
    contador = 0
    it = 0
    for it in range(len(evidencias)):  # Recorro la lista casteada de las claves
        posIt = evidencias[it]
        nodo = posIt[0]  # Obtenemos el nodo en forma de tupla
        nodoString = str(nodo[0]) + "," + str(nodo[1])  # obtenemos el nodo en forma de string
        vecinos = posIt[1]  # Obtenemos el número de vecinos con evidencias al rededor del nodo
        suma = posIt[2]  # Obtenemos la suma de las evidencias de los vecinos
        clave_num_vecinos = 'num_vecinos' + nodoString  # Construimos las claves para el diccionario con el formato para que el código funcione correctamente
        clave_sum_vecinos = 'sum_vecinos' + nodoString
        dic = {clave_num_vecinos: vecinos, clave_sum_vecinos: suma}
        # Llamo al método de eliminar variable y le asocio el nodo y la lista de evidencias
        proba = eliminaVariable(model, nodoString, dic)

        if it < len(evidencias):
            contador = proba
            it += 1
            dictResul[nodoString] = contador
            # Devuelve el nodo que contenga la menor probabilidad de obtener mina.
            maximo = max(dictResul, key=lambda k: dictResul[k])
            l = []
            for (k, v) in dictResul.items():
                l.append([k, v])
                for i in range(len(l)):
                    pos = l[i]
                    if maximo in pos:
                        v = l[i]

    # Formato que se mostrará por consola
    prob = " Probabilidad de minas "
    print(prob.center(50, "="))
    print('\nCasilla a clickear: ' + '\033[4m' + 'Probabilidad' + '\033[0m' + ' de no obtener mina ---> ' +
          str(v))


'''
Método que elimina la variable
Parámetros: modelo, nodo, diccionario con formato dicc = {nu_veinosi,j : 1, sum_vecinosi,j:2}
Return integer con la probabilidad de no tener mina
'''


def eliminaVariable(model, node, dicc):
    # Se llama a la clase VariableElimination de la librería pgmpy asociada al modelo
    modelo_elimina = VariableElimination(model)
    # Usamos el método "query" al cuál se le pasa una lista de nodos y una lista de evidencias
    consulta = modelo_elimina.query([node], dicc)
    con = consulta[node].values  # Obtenemos los valores, las probabilidades, asociadas a si tiene mina o no.
    # De esta forma, obtenemos solamente el valor asociado a la probabilidad que no haya mina. En el caso
    # de haber querido mostrar la probabilidad asociada a obtener mina, habria sido así: res = con[0]
    res = con[1]
    if res != 0:  # Comprobamos que la probabilidad obtenida teniendo en cuenta la evidencia conoida es distinta de 0
        res -= 0.05  # restamos a la probabilidad 0.05 para que el resultado no pueda llegar a ser un 100%
        # ya que esta probabilidad es calculada a partir de una evidencia dada y puede no ser correcta
    return res  # Devuelve el valor asociado a la probabilidad de no obtener mina


'''
Método que devuelve el array con la probabilidad con respecto a la suma de minas adyacentes a los vecinos.
Parámetros: número de vecinos
Return: Array de tamaño vecinos*5 con la probabilidad
'''


def probabilidaSumaVecinos(vecinos):
    sum_res = []
    it = 0
    # suponemos que como máximo la suma de vecinos adyacentes será = vecinos*2
    for it in range((vecinos * 5) + 1):
        sum_res.append(1)
        it += 1
    sum_res = numpy.array(sum_res) / numpy.array(sum_res).sum(axis=0, keepdims=1)
    return sum_res
