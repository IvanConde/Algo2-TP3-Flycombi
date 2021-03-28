#!/usr/bin/python3
from grafo import *
from biblioteca import *
from math import inf
import csv
import sys

INDICE_TIEMPO = 0
INDICE_PRECIO = 1
INDICE_CANTIDAD_VUELOS = 2

VALOR_RANDOM_WALK_L = 50
VALOR_RANDOM_WALK_K = 150

def imprimir_camino(camino):
    for i in range(len(camino)-1):
        print("{} -> ".format(camino[i]), end = "")
    print(camino[-1])

def imprimir_camino_centralidad(camino, n):
    for i in range(n-1):
        print("{}, ".format(camino[i][0]), end = "")
    print("{}".format(camino[n-1][0]))

def cargar_itinerario(grafo, ruta_archivo):
    with open(ruta_archivo, newline = '') as archivo:
        linea = csv.reader(archivo)
        cargar_grafo(grafo, next(linea))
        for conexiones in linea:
            grafo.agregar_arista(conexiones[0], conexiones[1])

def itinerario(ruta_archivo, grafo, dic_ciudades):
    grafo_itinerario = Grafo(True)
    cargar_itinerario(grafo_itinerario, ruta_archivo)
    ciudades_itinerario = orden_topologico(grafo_itinerario)
    print(", ".join(ciudades_itinerario))
    for ciudad in range(len(ciudades_itinerario)-1):
        origen = ciudades_itinerario[ciudad]
        destino = ciudades_itinerario[ciudad + 1]
        camino_escalas(origen, destino, grafo, dic_ciudades)

def vacaciones(origen, n, grafo, dic_ciudades):
    recorrido_vacaciones = []
    origenes = dic_ciudades[origen]
    for origen in origenes:
        recorrido_vacaciones = dfs_modificado(grafo, origen, int(n))
        if recorrido_vacaciones:
            break
    if len(recorrido_vacaciones) <= int(n):
        print("No se encontro recorrido")
    else:
        imprimir_camino(recorrido_vacaciones)

def nueva_aerolinea(ruta_archivo, grafo):
    arbol_tm = prim(grafo, INDICE_PRECIO)
    with open(ruta_archivo, "w", newline = '') as archivo:
        linea = csv.writer(archivo, delimiter = ',')
        visitados = set()
        for v in arbol_tm:
            visitados.add(v)
            for w in arbol_tm.obt_adyacentes(v):
                if w in visitados:
                    continue
                peso = arbol_tm.obt_peso(v, w)
                linea.writerow([v, w, peso[INDICE_TIEMPO], peso[INDICE_PRECIO], peso[INDICE_CANTIDAD_VUELOS]])
    print("OK")

def centralidad_aprox(n, grafo):
    aux = {}
    n_aux = int(n)
    for v in grafo:
        aux[v] = 0
    for i in range(VALOR_RANDOM_WALK_K):
        camino = random_walk(grafo, VALOR_RANDOM_WALK_L)
        for v in camino:
            aux[v] += 1
    cent = ordenar_vertices(aux)
    imprimir_camino_centralidad(cent, n_aux)

def centralidad(n, grafo):
    n_aux = int(n)
    cent = algoritmo_centralidad(grafo)
    cent_ordenados = ordenar_vertices(cent)
    imprimir_camino_centralidad(cent_ordenados, n_aux)

def camino_escalas(origen, destino, grafo, dic_ciudades):

    origines = dic_ciudades[origen]
    destinos = dic_ciudades[destino]
    caminos = []
    mejor_orden = inf
    dest_actual = None
    mejor_padre = {}
    camino_optimo = []

    for i in origines:
        padres, orden = bfs(grafo, i)
        caminos.append([padres, orden])

    for j in destinos:
        for padre, orden in caminos:
            if orden[j] < mejor_orden:
                mejor_padre = padre
                mejor_orden = orden[j]
                dest_actual = j

    while dest_actual != None:
        camino_optimo.append(dest_actual)
        dest_actual = mejor_padre[dest_actual]

    camino_optimo.reverse()
    imprimir_camino(camino_optimo)

def camino_mas(modo, origen, destino, grafo, dic_ciudades):

    if modo == "rapido":
        modo = INDICE_TIEMPO
    elif modo == "barato":
        modo = INDICE_PRECIO

    origines = dic_ciudades[origen]
    destinos = dic_ciudades[destino]
    caminos = []
    mejor_padre = {}
    mejor_dist = inf
    dest_actual = None
    camino_optimo = []

    for i in origines:
        padres, dist = dijkstra(grafo, i, modo)
        caminos.append([padres, dist])

    for j in destinos:
        for padre, dist in caminos:
            if dist[j] < mejor_dist:
                mejor_padre = padre
                mejor_dist = dist[j]
                dest_actual = j

    while dest_actual != None:
        camino_optimo.append(dest_actual)
        dest_actual = mejor_padre[dest_actual]

    camino_optimo.reverse()
    imprimir_camino(camino_optimo)

def cargar_grafo_principal(grafo, dic_ciudades):
    with open(sys.argv[1], 'r') as aeropuertos:
        linea = csv.reader(aeropuertos, delimiter = ',')
        for fila in linea:
            if fila[0] in dic_ciudades:
                dic_ciudades[fila[0]].append(fila[1])
            else: 
                dic_ciudades[fila[0]] = [fila[1]]
            grafo.agregar_vertice(fila[1])
    with open(sys.argv[2], 'r') as vuelos:
        linea = csv.reader(vuelos, delimiter = ',')
        for fila in linea:
            grafo.agregar_arista(fila[0], fila[1], [int(fila[2]), int(fila[3]), int(fila[4])])

def listar_operaciones():
    print("camino_mas")
    print ("camino_escalas")
    print ("centralidad")
    print ("centralidad_aprox")
    #print ("pagerank")
    print ("nueva_aerolinea")
    #print (recorrer_mundo)
    #print (recorrer_mundo_aprox)
    print ("vacaciones")
    print ("itinerario")
    #print (exportar_kml)
    return True

def ejecutar_comando(comando, argumentos, grafo, dic_ciudades):
    if comando == "listar_operaciones":
        listar_operaciones()
    elif comando == "camino_mas":
        camino_mas(argumentos[0], argumentos[1], argumentos[2], grafo, dic_ciudades)
    elif comando == "camino_escalas":
        camino_escalas(argumentos[0], argumentos[1], grafo, dic_ciudades)
    elif comando == "centralidad":
        centralidad(argumentos[0], grafo)
    elif comando == "centralidad_aprox":
        centralidad_aprox(argumentos[0], grafo)
    elif comando == "nueva_aerolinea":
        nueva_aerolinea(argumentos[0], grafo)
    elif comando == "vacaciones":
        vacaciones(argumentos[0], argumentos[1], grafo, dic_ciudades)
    elif comando == "itinerario":
        itinerario(argumentos[0], grafo, dic_ciudades)
    else:
        pass

def obtener_comando(linea, grafo, dic_ciudades):
    linea_leida = linea.rstrip().split(" ", 1)
    comando = linea_leida[0]
    argumentos = None
    if len(linea_leida) == 2:
        argumentos = linea_leida[1].split(',')
    ejecutar_comando(comando, argumentos, grafo, dic_ciudades)

def main():
    if len(sys.argv) == 3:
        grafo = Grafo()
        dic_ciudades = {}
        cargar_grafo_principal(grafo, dic_ciudades)
        for linea in sys.stdin:
            obtener_comando(linea, grafo, dic_ciudades)
    else:
        print("Error en cantidad de parametros.")
        sys.exit()

if __name__ == "__main__":
    main()