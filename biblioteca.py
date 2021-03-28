from math import inf
from heapq import *
from grafo import *
from queue import*
from random import choice

def dijkstra(grafo, origen, index):

    dist = {}
    padre = {}
    for v in grafo:
        dist[v] = inf
    dist[origen] = 0
    padre[origen] = None
    heap = []
    heappush(heap, (origen, dist[origen]))

    while heap:
        v, dist_v = heappop(heap)
        for w in grafo.obt_adyacentes(v):
            if dist_v + grafo.obt_peso(v, w)[index] < dist[w]:
                dist[w] = dist_v + grafo.obt_peso(v, w)[index]
                padre[w] = v
                heappush(heap, (w, dist[w]))

    return padre, dist

def cargar_grafo(grafo, lista):
    for elemento in lista:
        grafo.agregar_vertice(elemento)

def prim(grafo, index):

    vertice = grafo.obt_random()
    visitados = set()
    visitados.add(vertice)
    heap = []

    for w in grafo.obt_adyacentes(vertice):
        heappush(heap, (grafo.obt_peso(vertice, w)[index], vertice, w))

    arbol = Grafo()
    cargar_grafo(arbol, grafo.obt_vertices())

    while heap:
        _, v, w = heappop(heap)
        if w in visitados:
            continue
        arbol.agregar_arista(v, w, grafo.obt_peso(v, w))
        visitados.add(w)
        for x in grafo.obt_adyacentes(w):
            if x not in visitados:
                heappush(heap, (grafo.obt_peso(w, x)[index], w, x))

    return arbol

def orden_topologico(grafo):

    resul = []
    grados = {}
    pila = []

    for v in grafo:
        grados[v] = 0
    for v in grafo:
        for w in grafo.obt_adyacentes(v):
            grados[w] += 1
    for v in grafo:
        if grados[v] == 0:
            pila.append(v)

    while len(pila) > 0:
        v = pila.pop()
        resul.append(v)
        for w in grafo.obt_adyacentes(v):
            grados[w] -= 1
            if grados[w] == 0:
                pila.append(w)

    return resul

def bfs(grafo, origen):

    visitados = set()
    padres = {}
    orden = {}
    cola = Queue()
    visitados.add(origen)
    padres[origen] = None
    orden[origen] = 0
    cola.put(origen)

    while not cola.empty():
        v = cola.get()
        for w in grafo.obt_adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                padres[w] = v
                orden[w] = orden[v] + 1
                cola.put(w)

    return padres, orden

def ordenar_vertices(vertices):
    lista_aux = []
    for v in vertices:
        if(vertices[v] == inf):
            continue
        lista_aux.append((v,vertices[v]))
    lista_aux.sort(reverse = True, key = lambda x: x[1])
    return lista_aux

def dfs_modificado(grafo, origen, n):
    lista_origen = [origen]
    posiciones = {}
    return _dfs_modificado(grafo, lista_origen, 1, n+1, posiciones)

def _dfs_modificado(grafo, recorrido_temp, n_inicial, n_final, posiciones):

    if n_inicial == n_final and recorrido_temp[0] == recorrido_temp[-1]:
        return recorrido_temp

    if n_inicial < n_final:
        recorrido_aux = recorrido_temp[:]
        ultimo = recorrido_temp[-1]
        for w in grafo.obt_adyacentes(ultimo):
            if w in recorrido_temp and n_inicial < n_final-1:
                continue
            if w in posiciones.get(n_inicial, ()):
                continue
            recorrido_aux.append(w)
            recorrido = _dfs_modificado(grafo, recorrido_aux, n_inicial+1, n_final, posiciones)
            if recorrido:
                return recorrido

    if n_inicial not in posiciones:
        posiciones[n_inicial] = set()

    posiciones[n_inicial].add(recorrido_temp.pop())
    return []

def algoritmo_centralidad(grafo):

    centralidad = {}
    for v in grafo: 
        centralidad[v] = 0

    for v in grafo:
        padres, orden = bfs(grafo,v)
        aux = {}
        for w in grafo: 
            aux[w] = 0
        vertices_ordenados = ordenar_vertices(orden)
        for w, orden in vertices_ordenados:
            if w == v:
                continue
            aux[padres[w]] += 1 + aux[w]
        for w in grafo:
            if w == v:
                continue
            centralidad[w] += aux[w]

    return centralidad

def adyacente_aleatorio(grafo, v):
    adyacentes = grafo.obt_adyacentes(v)
    return choice(adyacentes)

def random_walk(grafo, largo):
    camino = []
    origen = grafo.obt_random()
    _random_walk(grafo, largo, camino, origen, 0)
    return camino

def _random_walk(grafo, largo, lista, v, contador):
    if contador >= largo:
        return
    lista.append(v)
    siguiente = adyacente_aleatorio(grafo, v)
    _random_walk(grafo, largo, lista, siguiente, contador+1)