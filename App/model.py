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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import time 
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as sel
from DISClib.Algorithms.Sorting import quicksort as qu
from DISClib.Algorithms.Sorting import mergesort as mg
assert cf
from datetime import datetime as datetime

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog(tipo = 'ARRAY_LIST', mapTipo = 'CHAINING', load = 4):
    """
    Inicializa el catálogo de libros. Crea una lista vacia para guardar
    todos los libros, adicionalmente, crea una lista vacia para los autores,
    una lista vacia para los generos y una lista vacia para la asociación
    generos y libros. Retorna el catalogo inicializado.
    O(1)
    """
    catalog = {'titlesAmazon': None,
               'titlesDisney': None,
               'titlesHulu': None,
               'titlesNetflix': None,
               'movieTitles': None,
               'genres':None,
               'actors' : None,
               'directors' : None, 
               
               }

    #catalog['movieTitles'] = lt.newList(tipo)
    
    streamers = ["Amazon","Disney","Hulu","Netflix"]
    for streamer in streamers:
        catalog["titles{}".format(streamer)] = lt.newList(tipo)
    catalog['movieTitles'] = lt.newList(tipo)
    catalog['showTitles'] = lt.newList(tipo)
    catalog['actors'] = mp.newMap(10000,
                                   maptype= mapTipo,
                                   loadfactor= load,
                                   comparefunction=compareactor)  
    catalog['genres'] = mp.newMap(10000,
                                   maptype= mapTipo,
                                   loadfactor= load,
                                   comparefunction=compareGenre)
    catalog['directors'] = mp.newMap(10000,
                                   maptype= mapTipo,
                                   loadfactor= load,
                                   comparefunction=compareDirectors)



    
    return catalog

# Funciones para agregar informacion al catalogo
def addTitles(catalog, title, streamer):
    '''O(1)'''
    lt.addLast(catalog['titles{}'.format(streamer)], title)
    
    directors = title['director'].split(",")
    
    addGenre(catalog,title)

    actor = title["cast"].split(",")
    for a in actor: 
        addActor(catalog,a.strip(),title)
        
    directors = title['director'].split(",")
    for director in directors:
        addDirector(catalog, director.strip(), title)
    return catalog

def addMovies(catalog, title, movie=True):
    '''O(1)'''
    if movie:
        lt.addLast(catalog['movieTitles'], title)
    else:
        lt.addLast(catalog['showTitles'], title)
    return catalog

def addGenre(catalog,title):
    '''O(1)'''
    generos = catalog['genres'] 
    generos_titulo = [i.strip() for i in title["listed_in"].split(",")] 
    for g in generos_titulo: 
        if not mp.contains(generos,g):
            genero = newGenre(g) 
            mp.put(generos,g,genero) 
    return catalog

def addActor(catalog,nameactor,title):
    '''O(1)'''
    actores = catalog['actors'] 
    # actor = [i.strip() for i in title["cast"].split(",")] 
    # for a in actor: 
    if not mp.contains(actores,nameactor):
            act = newActor(nameactor)
            mp.put(actores,nameactor,act)
    else: 
            act = me.getValue(mp.get(actores,nameactor))
    if title["type"] == "Movie": 
        lt.addLast(act["peliculas"],title) 
    else: 
        lt.addLast(act["shows"],title)  
    return actores  

def addDirector(catalog, directorname, title):
    '''O(1)'''
    directors = catalog['directors']
    if not mp.contains(directors,directorname):
        infodirector = newDirector(directorname)
        mp.put(directors,directorname,infodirector)
    else: 
        infodirector = me.getValue(mp.get(directors,directorname))
    
    if title["type"] == "Movie": 
        lt.addLast(infodirector["peliculas"],title) 
    else: 
        lt.addLast(infodirector["shows"],title)

    generos = title["listed_in"].split(",")
    for g in generos:
        lt.addLast(infodirector["genres"],g)
        
    return directors

# Funciones para creacion de datos

def newGenre(name):
    '''O(1)'''
    genre = {'genero': "", 'titulos': None, 'movies': None, 'shows' : None}
    genre['genero'] = name
    # genre['titulos'] = lt.newList()
    # genre['movies'] = lt.newList()
    # genre['shows'] = lt.newList()
    return genre

def newActor(nameactor):
    '''O(1)'''
    actors = {"actor": "", "peliculas": None, "shows": None}
    actors["actor"] = nameactor 
    actors["peliculas"] = lt.newList("ARRAY_LIST") 
    actors["shows"] = lt.newList("ARRAY_LIST")
    return actors 

def newDirector(name):
    '''O(1)'''
    director = {'nombre': "", 'movies': None, 'shows': None, 'titles': None, 'genres': None, 'streamers': None}
    director['nombre'] = name
    director['movies'] = lt.newList('ARRAY_LIST')
    director['shows'] = lt.newList('ARRAY_LIST')
    director['titles'] = lt.newList('ARRAY_LIST')
    director['genres'] = lt.newList('ARRAY_LIST')
    director['streamers'] = lt.newList('ARRAY_LIST')
    return director

# Funciones de consulta

def requerimiento1(catalog,lb,ub):
    '''O(NlogN + N) = O(NlogN)'''
    variables = ['type','release_year','title','duration','streamer','director','cast']
    sl,dt = mergeSort(catalog["model"])
    listado = lt.newList("ARRAY_LIST")
    for element in lt.iterator(sl):
        anho = element["release_year"]
        rel_year = datetime.strptime(anho,"%Y")
        if (rel_year>=lb) & (rel_year<=ub):
            elemento_a_incluir = {i:element[i] for i in variables}
            lt.addLast(listado,elemento_a_incluir)
    return(listado)

def requerimiento2(catalog,lb,ub):
    '''O(NlogN + N) = O(NlogN)'''
    variables = ['type','title','date_added','duration','release_year','streamer','director','cast']
    sl,dt = mergeSort(catalog["model"],"showTitles",cmpShowsByReleaseYear)
    listado = lt.newList("ARRAY_LIST")
    for element in lt.iterator(sl):
        if element["date_added"] != "":
            fecha = datetime.strptime(element["date_added"],"%Y-%m-%d") 
            if (fecha>=lb) & (fecha<=ub):
                elemento_a_incluir = {i:element[i] for i in variables}
                lt.addLast(listado,elemento_a_incluir)
    #print(listado)
    return(listado)

def requerimiento5(catalog,pais):
    '''O(NlogN + N) = O(NlogN)'''
    variables = ['type','title','release_year','director','streamer','duration','cast','country','listed_in','description']
    slm,dtm = mergeSort(catalog["model"],"movieTitles",cmpReq5)
    sls,dts = mergeSort(catalog["model"],"showTitles",cmpReq5)
    lm = lt.newList("ARRAY_LIST")
    ls = lt.newList("ARRAY_LIST")
    lista = lt.newList("ARRAY_LIST")
    hola = {}
    for element in lt.iterator(slm):
        if element['country'] == pais:
            elemento_a_incluir = {i:element[i] for i in variables}
            lt.addLast(lm,elemento_a_incluir)
            lt.addLast(lista,elemento_a_incluir)
    for element in lt.iterator(sls):
        if element['country'] == pais:
            elemento_a_incluir = {i:element[i] for i in variables}
            lt.addLast(ls,elemento_a_incluir)
            lt.addLast(lista,elemento_a_incluir)
    hola['var'] = lista
    lista,baa = mergeSort(hola,"var",cmpReq5)
    return [lm,ls,lista]



def buscarActor(catalog,actor):
    '''O(N)'''
    peliculas = 0
    shows = 0
    datos = lt.newList("ARRAY_LIST")
    #Esto es un diccionario de diccionarios
    act = me.getValue(mp.get(catalog["actors"],actor))
    if act:
        peliculas = lt.size(act["peliculas"])
        shows = lt.size(act["shows"]) 
    sa.sort(act["peliculas"],ordernarpeliculas)
    sa.sort(act["shows"],ordernarpeliculas)   

    lt.addLast(datos,peliculas)
    lt.addLast(datos,shows)
    lt.addLast(datos,act) 
    return datos 



def encontrarRepetidosG(directors):
    '''O(N)'''
    lugar = directors['genres']
    repe = {}
    for genero in lt.iterator(lugar):
        if genero in repe:
            repe[genero] += 1
        else:
            repe[genero] = 1
    return repe

def encontrarRepetidosS(directors):
    '''O(N)'''
    lugar = directors['streamers']
    repe = {}
    for genero in lt.iterator(lugar):
        if genero in repe:
            repe[genero] += 1
        else:
            repe[genero] = 1
    return repe

def getFirstTitles(catalog,streamer):
    '''O(1)'''
    titles = catalog['titles{}'.format(streamer)]
    firstTitles = lt.newList()
    for cont in range(1, 4):
        title = lt.getElement(titles, cont)
        lt.addLast(firstTitles, title)
    return firstTitles

def getLastTitles(catalog,streamer):
    '''O(1)'''
    titles = catalog['titles{}'.format(streamer)]
    lastTitles = lt.newList()
    for cont in range((titleSize(catalog,streamer) - 3), (titleSize(catalog,streamer) )):
        title = lt.getElement(titles, cont)
        lt.addLast(lastTitles, title)
    return lastTitles

def getTitles(list,position,number=3):
    '''O(1)'''
    listsize = lt.size(list)
    showingTitles = lt.newList()
    while listsize<number:
        number-=1
    if position == "f":
        recorrido = range(1, number+1)
    elif position =="l":
        recorrido = range((listsize - number), listsize)
    for cont in recorrido:
        title = lt.getElement(list, cont)
        lt.addLast(showingTitles, title)
    return lt.iterator(showingTitles)

def getTitlesByGenre(catalog, genrename):
    '''O(1)'''
    posgenre = lt.isPresent(catalog['genres'], genrename)
    if posgenre > 0:
        genre = lt.getElement(catalog['genres'], posgenre)
        return genre
    return None

def getFirstTitlesByGenreOrDir(titulos):
    '''O(1)'''
    first = lt.newList()
    for cont in range(1,4):
        title = lt.getElement(titulos, cont)
        lt.addLast(first, title)
    return first

def getLastTitlesByGenreOrDir(titulos):
    '''O(1)'''
    last = lt.newList()
    size = lt.size(titulos)
    for cont in range((size -2), (size + 1)):
        title = lt.getElement(titulos, cont)
        lt.addLast(last, title)
    return last

def getTopGenres(genres, number):
    '''O(N)'''
    top = lt.newList()
    for cont in range(1, number +1):
        genero = lt.getElement(genres, cont)
        lt.addLast(top, genero)
    return top

def getMoviesByDirector(catalog, name):
    '''O(1)'''
    lugar = catalog['model']['directors']
    
    posdir = lt.isPresent(lugar, name)
    if posdir > 0:
        director = lt.getElement(lugar, posdir)
        return director
    return None

def titleSize(catalog,streamer):
    '''O(1)'''
    return lt.size(catalog['titles{}'.format(streamer)])

def moviesSize(catalog):
    '''O(1)'''
    return lt.size(catalog['movieTitles'])

def genreSize(catalog):
    '''O(1)'''
    return lt.size(catalog['genres'])

def getGenresSize(genres):
    '''O(N)'''
    generos= lt.newList()
    genero = {'nombre': '', 'size': None, 'sizeMov': None, 'sizeShow': None, 'amazon': None, 'disney': None, 'hulu': None, 'netflix': None}
    for i in lt.iterator(genres):
        amazon = 0
        disney = 0
        hulu = 0
        netflix = 0
        genero['nombre'] = i['genero']
        genero['size'] =lt.size(i['titulos'])
        genero['sizeMov'] = lt.size(i['movies'])
        genero['sizeShow'] = lt.size(i['shows'])
        for title in lt.iterator(i['titulos']):
            if title['streamer'] == 'Amazon':
                amazon += 1
            elif title['streamer'] == 'Disney':
                disney += 1
            elif title['streamer'] == 'Hulu':
                hulu += 1
            else:
                netflix += 1
        genero['amazon'] = amazon
        genero['disney'] = disney
        genero['hulu'] = hulu
        genero['netflix'] = netflix
        
        lt.addLast(generos, [genero['nombre'], genero['size'], genero['sizeMov'], genero['sizeShow'], genero['amazon'], genero['disney'], genero['hulu'], genero['netflix']])
    return generos

def directorSize(catalog):
    '''O(1)'''
    return lt.size(catalog['directors'])


def getSizeByGenre(genre):
    '''O(1)'''
    peliculas = lt.size(genre['movies'])
    shows = lt.size(genre['shows'])
    return peliculas, shows

# Funciones utilizadas para comparar elementos dentro de una lista
def compareGenre(genero, entry):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    generoentry = me.getKey(entry)
    if (genero == generoentry):
        return 0
    elif (genero > generoentry):
        return 1
    else:
        return -1

def comparetitles(title1, title2):
    '''O(1)'''
    if title1['release_year'] < title2['release_year'] or title1['release_year'] > title2['release_year']:
        return (title1['release_year'] < title2['release_year'])
    else:
        return (title1['title'] < title2['title'])


def compareDirectors(dir1, dir):
    '''O(1)'''
    if dir1.lower() == dir['nombre'].lower():
        return 0
    elif dir1.lower() > dir['nombre'].lower():
        return 1
    return -1

def comparegenres(genre1, genre):
    '''O(1)'''
    if genre1.lower() == genre['genero'].lower():
        return 0
    elif genre1.lower() > genre['genero'].lower():
        return 1
    return -1

def compareactor(nombreactor, actor):
    '''O(1)'''
    authentry = me.getKey(actor) 
    if nombreactor == authentry:
        return 0 
    elif nombreactor > authentry:
        return 1
    else:
        return -1

def ordernarpeliculas(movie1,movie2):
    '''O(1)'''
    if movie1['title'] < movie2['title'] or movie1['title'] > movie2['title']:
        return (movie1['title'] < movie2['title'])
    elif movie1['release_year'] < movie2['release_year'] or movie1['release_year'] > movie2['release_year']:
        return (movie1['release_year'] < movie2['release_year'])
    else:
        return (movie1['duration'] < movie2['duration'])  
        

def cmpGenres(title1, title2):
    '''O(1)'''
    if title1['title'] < title2['title'] or title1['title'] > title2['title']:
        return (title1['title'] < title2['title'])
    elif title1['release_year'] < title2['release_year'] or title1['release_year'] > title2['release_year']:
        return (title1['release_year'] < title2['release_year'])
    else:
        return (title1['director'] < title2['director'])

def cmpGenresBySize(genre1, genre2):
    '''O(1)'''
    if genre1[1] < genre2[1] or genre1[1] > genre2[1] :
        return genre1[1] > genre2[1] 
    else:
        return genre1[0] < genre2[0]

def cmpMoviesByReleaseYear(movie1, movie2):
    '''O(1)'''
    if movie1['release_year'] < movie2['release_year'] or movie1['release_year'] > movie2['release_year']:
        return (movie1['release_year'] < movie2['release_year'])
    elif movie1['release_year'] == movie2['release_year']:
        if movie1['title'] < movie2['title'] or movie1['title'] > movie2['title']:
            return (movie1['title'] < movie2['title'])
        else:
            return (movie1['duration'] < movie2['duration'])

def cmpDirectors(title1, title2):
    '''O(1)'''
    if title1['release_year'] < title2['release_year'] or title1['release_year'] > title2['release_year']:
        return (title1['release_year'] < title2['release_year'])
    elif title1['title'] < title2['title'] or title1['title'] > title2['title']:
        return (title1['title'] < title2['title'])
    else:
        return (title1['duration'] < title2['duration'])


def cmpShowsByReleaseYear(show1, show2):
    '''O(1)'''
    DA1 = show1['date_added'] 
    DA2 = show2['date_added']
    if DA1<DA2 or DA1>DA2:
        return DA1<DA2
    else:
        T1 = show1["title"]
        T2 = show2["title"]
        if T1<T2 or T1>T2:
            return T1<T2
        else:
            DUR1 = int(show1["duration"].split()[0])
            DUR2 = int(show2["duration"].split()[0])
            if DUR1<DUR2 or DUR1>DUR2:
                return DUR1<DUR2
            else:
                return True

def cmpReq5(C1,C2):
    '''O(1)'''
    T1 = C1['title']
    T2 = C2['title']
    if T1<T2 or T1>T2:
        return T1<T2
    else:
        RY1 = int(C1['release_year'])
        RY2 = int(C2['release_year'])
        if RY1==RY2:
            D1 = C1['director']
            D2 = C2['director']
            if D1==D2:
                return False
            else:
                return D1<D2
        else:
            return RY1<RY2

# Funciones de ordenamiento

def sortTitle(catalog,streamer):
    '''O(N^{3/2})'''
    mg.sort(catalog['titles{}'.format(streamer)], comparetitles)

def sortGenres(catalog):
    '''O(N^{3/2})'''
    return mg.sort(catalog, cmpGenres)

def sortGenresBySize(generos):
    '''O(N^{3/2})'''
    return mg.sort(generos, cmpGenresBySize)

       
def sortActor(catalog,streamer):
    '''O(N^{3/2})'''
    mg.sort(catalog['titles{}'.format(streamer)], ordernarpeliculas) 

def sortDirectors(catalog):
    '''O(N^{3/2})'''
    return mg.sort(catalog, cmpDirectors)

#Funciones algoritmos de ordenamiento
def selection(catalog,var = 'movieTitles',cmpfun = cmpMoviesByReleaseYear):
    '''O(N^2)'''
    start_time = getTime()
    sorted_list = sel.sort(catalog[var], cmpfun)
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return sorted_list, delta_time

def insertion(catalog,var = 'movieTitles',cmpfun = cmpMoviesByReleaseYear):
    '''O(N^2)'''
    start_time = getTime()
    sorted_list = ins.sort(catalog[var], cmpfun)
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return sorted_list, delta_time

def shellSort(catalog,var = 'movieTitles',cmpfun = cmpMoviesByReleaseYear):
    '''O(N^{3/2})'''
    start_time = getTime()
    sorted_list = sa.sort(catalog[var], cmpfun)
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return sorted_list, delta_time

def mergeSort(catalog,var = 'movieTitles',cmpfun = cmpMoviesByReleaseYear):
    '''O(NlogN)'''
    start_time = getTime()
    sorted_list = mg.sort(catalog[var], cmpfun)
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return sorted_list, delta_time

def quickSort(catalog,var = 'movieTitles',cmpfun = cmpMoviesByReleaseYear):
    '''O(N^2)'''
    start_time = getTime()
    sorted_list = qu.sort(catalog[var], cmpfun)
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return sorted_list, delta_time

#Creación de sublista para lista de películas
def movieSublist(catalog, pos, numelem):
    # O(1)
   return lt.subList(catalog['model']['movieTitles'], pos, numelem)

# Funciones para medir tiempos de ejecucion
def getTime():
    '''O(1)'''
    return float(time.perf_counter()*1000)


def deltaTime(start, end):
    '''O(1)'''
    elapsed = float(end - start)
    return elapsed
