"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

from time import strptime
import config as cf
import model
import csv
from datetime import datetime as datetime
import time
import tracemalloc


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def newController(tipo, mapTipo, load):
    """
    Crea una instancia del modelo
    O(1)
    """
    control = {
        'model': None
    }
    control['model'] = model.newCatalog(tipo, mapTipo, load)
    return control
# Funciones para la carga de datos

def loadData(control,  memflag=True, id='small'):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    '''O(N)'''
    start_time = getTime()

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    catalog = control['model']
    streamers = {"amazon_prime":"Amazon","disney_plus":"Disney","hulu":"Hulu","netflix":"Netflix"}
    valores =[]
    for i in streamers:
        titles = loadTitles(catalog, i, id)
        valores.append(titles)

    for i in streamers:
        sortTitle(catalog,streamers[i])

    valores.append(model.genreSize(catalog)) # Ojo con este =)
    valores.append(model.directorSize(catalog))

    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return valores, delta_time, delta_memory
    else:
        return valores, delta_time

def loadTitles(catalog,streamer,archivo):
    '''O(N)'''
    moviesfile = cf.data_dir + 'Streaming/{}_titles-utf8-{}.csv'.format(streamer,archivo)
    input_file = csv.DictReader(open(moviesfile, encoding='utf-8'))
    streamers = {"amazon_prime":"Amazon","disney_plus":"Disney","hulu":"Hulu","netflix":"Netflix"}
    streamer = streamers[streamer] 
    for title in input_file:
        title["streamer"] = streamer
        model.addTitles(catalog, title,streamer)
        if title['type'] == 'Movie':
            title["streamer"] = streamer
            model.addMovies(catalog, title)
        elif title['type'] == 'TV Show':
            title["streamer"] = streamer
            model.addMovies(catalog, title,False)
    return model.titleSize(catalog,streamer)

# Funciones de ordenamiento
def sortTitle(catalog,streamer):
    '''O(N^{3/2})'''
    return model.sortTitle(catalog,streamer) 


def selectionSort(catalog):
    '''O(N^2)'''
    return model.selection(catalog['model'])

def insertionSort(catalog):
    '''O(N^2)'''
    return model.insertion(catalog['model'])

def shellsort(catalog):
    '''O(N^{3/2})'''
    return model.shellSort(catalog['model'])

def mergesort(catalog):
    '''O(NlogN)'''
    return model.mergeSort(catalog['model'])

def quicksort(catalog):
    '''O(N^2)'''
    return model.quickSort(catalog['model'])

def sortGenres(catalog):
    '''O(N^{3/2})'''
    return model.sortGenres(catalog) 

def sortGenresBySize(generos):
    '''O(N^{3/2})'''
    return model.sortGenresBySize(generos) 

def sortActor(catalog,streamer):
    '''O(N^{3/2})'''
    return model.sortActor(catalog,streamer)

def sortDirectors(catalog):
    '''O(N^{3/2})'''
    return model.sortDirectors(catalog)

# Funciones de consulta sobre el catálogo
def requerimiento1(catalog,lb,ub):
    '''O(NlogN)'''
    if all([(isinstance(i,(str))) and (len(i)==4) for i in [lb,ub]]):
        lb = datetime.strptime(lb,"%Y")
        ub = datetime.strptime(ub,"%Y")
        if lb<=ub:
            return model.requerimiento1(catalog,lb,ub)
        else:
            print("\nError\n")
    else:
        print("\nError\n")

def requerimiento2(catalog,lb,ub):
    '''O(NlogN)'''
    formato_dar = "%B {}d, %Y".format("%")
    lb = datetime.strptime(lb,formato_dar)
    ub = datetime.strptime(ub,formato_dar)
    for i in [lb,ub]:
        print(i)
    if lb<=ub:
        return model.requerimiento2(catalog,lb,ub)
    else:
        print("\nError\n")  

def requerimiento5(catalog,pais):
    '''O(NlogN)'''
    return model.requerimiento5(catalog,pais)

def moviesSize(control):
    '''O(1)'''
    catalog = control['model']
    return model.moviesSize(catalog)

def buscar_peliculas_por_actor(control, actor):
    '''O(N)'''
    return model.buscarActor(control["model"], actor)

def movieSublist(catalog, pos, numelem):
    '''O(1)'''
    return model.movieSublist(catalog, pos, numelem)

def getFirstTitles(control,streamer):
    '''O(1)'''
    firstTitles = model.getFirstTitles(control['model'],streamer)
    return firstTitles

def getLastTitles(control,streamer):
    '''O(1)'''
    lastTitles = model.getLastTitles(control['model'],streamer)
    return lastTitles

def getTitles(list,position,number):
    '''O(1)'''
    return model.getTitles(list,position,number)

def getFirstTitlesByGenreOrDir(titulos):
    '''O(1)'''
    firstTitles = model.getFirstTitlesByGenreOrDir(titulos)
    return firstTitles 

def getLastTitlesByGenreOrDir(titulos):
    '''O(1)'''
    firstTitles = model.getLastTitlesByGenreOrDir(titulos) 
    return firstTitles 

def getLastTitlesByGenre(titulos):
    '''O(1)'''
    firstTitles = model.getLastTitlesByGenre(titulos) 
    return firstTitles 

def getTitlesByGenre(control, genrename):
    '''O(1)'''
    genero = model.getTitlesByGenre(control['model'], genrename)
    return genero

def getGenresSize(genres):
    '''O(N)'''
    return model.getGenresSize(genres)

def getTopGenres(genres, number):
    '''O(N)'''
    return model.getTopGenres(genres, number)

def getSizeByGenre(genrename):
    '''O(1)'''
    return model.getSizeByGenre(genrename)

def getMoviesByDirector(catalog, directorname):
    '''O(1)'''
    return model.getMoviesByDirector(catalog, directorname)

def encontrarRepetidosG(directors):
    '''O(N)'''
    return model.encontrarRepetidosG(directors)

def encontrarRepetidosS(directors):
    '''O(N)'''
    return model.encontrarRepetidosS(directors)


# Funciones para medir tiempos de ejecucion


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed


# Funciones para medir la memoria utilizada


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
