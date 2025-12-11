import csv


def heapify(lista, largo, actual, columna):
    mayor = actual
    pos1 = 2 * actual + 1  
    pos2 = 2 * actual + 2  

    if pos1 < largo and lista[pos1][columna] > lista[mayor][columna]:
        mayor = pos1

    if pos2 < largo and lista[pos2][columna] > lista[mayor][columna]:
       
        mayor = pos2

    if mayor != actual:
        lista[actual], lista[mayor] = lista[mayor], lista[actual]
        heapify(lista, largo, mayor, columna)


def heapsort(lista, columna):
    largo = len(lista)

    inicio = largo // 2 - 1
    for i in range(inicio, -1, -1):
        heapify(lista, largo, i, columna)

    for fin in range(largo - 1, 0, -1):
        lista[0], lista[fin] = lista[fin], lista[0]
        heapify(lista, fin, 0, columna)

    return lista


def leer_csv(ruta):
    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        filas = list(lector)
        columnas = lector.fieldnames
        return columnas, filas


