"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

import config as cf
from tabulate import tabulate 
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from prettytable import PrettyTable 
import time


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
default_limit = 1000
sys.setrecursionlimit(default_limit*100)

#Funciones de inicio
def newController(tipo='ARRAY_LIST', mapTipo = 'CHAINING', load = 4):
    """
    Se crea una instancia del controlador
    """
    control = controller.newController(tipo, mapTipo, load)
    return control

def loadData(control,mem, archivo = "small"):
    """
    Solicita al controlador que cargue los datos en el modelo
    O(N)
    """
    
    charge = controller.loadData(control, mem, archivo)
    return charge

control = newController()
#Funciones de menús de información

def printMenu():
    '''O(1)'''
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- Listar las peliculas estrenadas en un periodo de tiempo")
    print("2- Listar programas de televisión agregados en un periodo de tiempo")
    print("3- Encontrar contenido donde participa un actor")
    print("4- Encontrar contenido por un genero especifico")
    print("5- Encontrar contenido producido en un país")
    print("6- Encontrar contenido con un director involucrado")
    print("7- Listar el top (N) de los generos con más contenido")
    print("8- Listar el top (N) de los actores con más participaciones en contenido")
    print("9- Ordenamientos de contenido")
    print("10- Salir del menú")

def printEleccionLista():
    '''O(1)'''
    print("\nElija la representación de lista que desea")
    print("1- Linked List")
    print("2- Array List")

def printEleccionArchivo0():
    '''O(1)'''
    print("\nElija una opción\n")
    print("1- Cargar un archivo diferente")
    print("2- Obtener una sublista")

def printEleccionArchivo1():
    '''O(1)'''
    print("\nElija el tamaño de archivo que desea cargar")
    print("1- small")
    print("2- 05pct")
    print("3- 10pct")
    print("4- 20pct")
    print("5- 30pct")
    print("6- 50pct")
    print("7- 80pct")
    print("8- large")

def printEleccionAlgoritmo():
    '''O(1)'''
    print("\nElija el algoritmo que desea usar")
    print("1- Selection")
    print("2- Insertion")
    print("3- Shell")
    print("4- Merge")
    print("5- Quick")

def printTipoMap():
    '''O(1)'''
    print("\nElija la representación de mapa que desea")
    print("1- Chaining")
    print("2- Probing")

#Funciones de obtener o dar formato a la información
def printFirstTitles(titulos,palabra):
    '''O(N)'''
    size = lt.size(titulos) 
    tabular =[]
    if size:
        #palabra = "Amazon Prime"
        for titulo in lt.iterator(titulos): 
            titulo = [titulo['show_id'], palabra, titulo['title'],titulo['type'], titulo['director'], titulo['country'], titulo['date_added'], titulo['cast'], titulo['release_year'], titulo['rating'], titulo['duration'], titulo['listed_in'], titulo['description']]
            tabular.append(titulo)
        return tabular
       
    else:
        print('No se encontraron películas en {}'.format(palabra))

def printLastTitles(titulos,palabra):
    '''O(N)'''
    size = lt.size(titulos)
    tabular =[]
    if size:
        #palabra = "Amazon Prime"
        for titulo in lt.iterator(titulos):
            titulo = [titulo['show_id'], palabra, titulo['title'], titulo['type'], titulo['director'], titulo['cast'], titulo['country'], titulo['date_added'], titulo['release_year'], titulo['rating'], titulo['duration'], titulo['listed_in'], titulo['description']]
            tabular.append(titulo)
        return tabular
    else:
        print('No se encontraron películas en {}'.format(palabra))

def pegarTablas(lista):
    '''O(N)'''
    x = PrettyTable()
    x.field_names = ["Show ID", "Streamer", "Titulo", "Tipo de contenido", "Director", "Cast", "Pais", "Fecha añadida", "Año de estreno", "Rating", "Duración", "Género", "Descripción"]
    x.max_width = 10
    x.hrules = True
    x.align = "l"
    listado =lista[0]
    for i in range(1, len(lista)):
        listado = listado + lista[i]
    #print(tabulate(listado, tablefmt='grid', headers=["Streamer", "Titulo", "Año de estreno", "Rating", "Duración"]))
    x.add_rows(listado)
    print(x)

def formato(listadoFirst, listadoLast):
    '''O(N)'''
    contador = 1
    for listado in [listadoFirst, listadoLast]:
        if contador == 1:
            palabra1 = "Los 3 primeros titulos por servicio de Streaming"
            contador += 1
        else:
            palabra1 = "Los 3 ultimos titulos por servicio de Streaming"
        print("\n"*2 + "---{}---".format(palabra1) + "\n"*2)
        pegarTablas(listado)
    print("\n"*2 + "-"*50 + "\n"*2)

def moviesSublist(catalog, pos, numelem):
    '''O(1)'''
    return controller.movieSublist(catalog, pos, numelem)

def checklist(catalog, pos, numelem):
    '''O(1)'''
    size = lt.size(catalog['model']['movieTitles'])
    if pos + numelem <= size +1:
        return True
    else:
        return False

def moviesSize(control):
    '''O(1)'''
    return controller.moviesSize(control)

def getTitles(list,position,number):
    '''O(1)'''
    return controller.getTitles(list,position,number)

def requerimiento1(catalog,lb,ub):
    '''O(NlogN)'''
    return controller.requerimiento1(catalog,lb,ub)

def requerimiento2(catalog,lb,ub):
    '''O(NlogN)'''
    return controller.requerimiento2(catalog,lb,ub)

def requerimiento5(catalog,pais):
    '''O(NlogN)'''
    return controller.requerimiento5(catalog,pais)

def printGenreData(genre, genrename):
    '''O(N)'''
    x = PrettyTable()
    y = PrettyTable()
    if genre:
        titulos = controller.sortGenres(genre['titulos'])

        print('Genero encontrado: ' + genre['genero'])
        print('Total de titulos por genero: ' + str(lt.size(genre['titulos'])))
        primeros = controller.getFirstTitlesByGenreOrDir(titulos)
        ultimos = controller.getLastTitlesByGenreOrDir(titulos)
        tamano = controller.getSizeByGenre(genre)
        print('Cantidad de peliculas para ' + str(genrename) + ': ' + str(tamano[0]))
        print('Cantidad de shows para ' + str(genrename) + ': ' + str(tamano[1]))

        print('Estos son los 3 primeros titulos: ')
        x.field_names = ['Titulo','Año de estreno', 'Director', 'Streamer', 'Duración', 'Cast', 'País', 'Género', 'Descripción']
        x.max_width = 25
        x.hrules = True
        x.align = "l"
        for title in lt.iterator(primeros):
            x.add_row([title['title'], title['release_year'], title['director'], title['streamer'], title['duration'], title['cast'], title['country'], title['listed_in'], title['description']])
        print(x)
        print('Estos son los 3 ultimos titulos: ')
        y.field_names = ['Titulo','Año de estreno', 'Director', 'Streamer', 'Duración', 'Cast', 'País', 'Género', 'Descripción']
        y.max_width = 25
        y.hrules = True
        y.align = "l"
        for title in lt.iterator(ultimos):
            y.add_row([title['title'], title['release_year'], title['director'], title['streamer'], title['duration'], title['cast'], title['country'], title['listed_in'], title['description']])
        print(y)
    else:
        print('No se encontraron titulos para este género')

def printGenreTopN(genres, topN):
    '''O(N)'''
    w = PrettyTable()
    w.field_names = ['Genero','Número de titulos', 'Tipo', 'Streamer']
    w.max_width = 25
    w.hrules = True
    w.align = "l"
    listageneros = controller.getGenresSize(genres)
    generos = controller.sortGenresBySize(listageneros) 
    top = controller.getTopGenres(generos, topN)
    for i in lt.iterator(top):
        titulos = 'Amazon: ' + str(i[4]) + '\n Disney: ' + str(i[5]) + '\n Hulu: ' + str(i[6]) + '\n Netflix: ' + str(i[7])
        cantidad = 'Peliculas: ' + str(i[2]) + '\n Shows: ' + str(i[3])
        w.add_row([i[0], i[1], cantidad, titulos])
    print(w)

def printActorData(catalog, actor):
    '''O(N)'''
    #Esto es una tupla con las peliculas y los shows
    x = PrettyTable()
    x.field_names=["Type", "title", "release_year", "director", "duration","cast","country","listed_in","description"] 
    x.max_width = 25
    x.hrules = True 
    respuesta = controller.buscar_peliculas_por_actor(catalog, actor) 
    peliculas = lt.getElement(respuesta,1)
    shows = lt.getElement(respuesta,2)
    act = lt.getElement(respuesta,0) 
    datos = []
    
    i = 1
    for titulos in lt.iterator(act["titles"]):
         if i <= 3 or i > lt.size(act["titles"])-3:  
          titulo = [titulos["type"], titulos["title"],titulos["release_year"],titulos["director"],titulos["duration"],titulos["cast"],titulos["country"], titulos["listed_in"], titulos["description"]]
          datos.append(titulo)
          i +=1 
    for titulos in lt.iterator(act["shows"]): 
          titulo = [titulos["type"], titulos["title"],titulos["release_year"],titulos["director"],titulos["duration"],titulos["cast"],titulos["country"], titulos["listed_in"], titulos["description"]]
          datos.append(titulo)
    print(tabulate([["Movie",peliculas],["Shows", shows]]))
    x.add_rows(datos)
    print(x) 

def printDirectorData(director,directorname):
    '''O(N^{3/2})'''
    titulosnum = []
    x = PrettyTable()
    y = PrettyTable()
    w = PrettyTable()
    if director:
        print('Director buscado: ' + director['nombre'] + '\n')
        mov = controller.sortDirectors(director['peliculas'])
        sho = controller.sortDirectors(director['shows'])
        titulos = controller.sortDirectors(director['titles'])
        peliculas = ['Movies', lt.size(director['peliculas'])]
        shows = ['Shows', lt.size(director['shows'])]
        titulosnum.append(peliculas)
        titulosnum.append(shows)
        print(tabulate(titulosnum, headers= ['Tipo', 'Cantidad'], tablefmt='grid') + '\n')
        datosRepe = controller.encontrarRepetidosG(director)
        datosRepeS = controller.encontrarRepetidosS(director)
        datosGeneros = []
        datosStreamers = []
        for clave in datosRepe:
            value = datosRepe[clave]
            datosGeneros.append([clave, value])
        print('Estos son los géneros en los que aparece el director ' + director['nombre'])
        print('\n' + tabulate(datosGeneros, headers=['Genero', 'Número de titulos'], tablefmt='grid'))
        for clave in datosRepeS:
            value = datosRepeS[clave]
            datosStreamers.append([clave, value])
        print('Estos son los servicios de streaming en los que aparece el director ' + director['nombre'])
        print(tabulate(datosStreamers, headers=['Streamer', 'Número de titulos'], tablefmt='grid'))
            
        if (peliculas[1] + shows[1]) > 6:
            primerost = controller.getFirstTitlesByGenreOrDir(titulos)
            ultimost = controller.getLastTitlesByGenreOrDir(titulos)
            print('Estos son los 3 primeros titulos: ')
            x.field_names = ['Titulo','Año de estreno', 'Director', 'Streamer', 'Duración', 'Cast', 'País', 'Género', 'Descripción']
            x.max_width = 10
            x.hrules = True
            x.align = "l"
            for title in lt.iterator(primerost):
                x.add_row([title['title'], title['release_year'], title['director'], title['streamer'], title['duration'], title['cast'], title['country'], title['listed_in'], title['description']])
            print(x)
            print('Estos son los 3 ultimos titulos: ')
            y.field_names = ['Titulo','Año de estreno', 'Director', 'Streamer', 'Duración', 'Cast', 'País', 'Género', 'Descripción']
            y.max_width = 10
            y.hrules = True
            y.align = "l"
            for title in lt.iterator(ultimost):
                y.add_row([title['title'], title['release_year'], title['director'], title['streamer'], title['duration'], title['cast'], title['country'], title['listed_in'], title['description']])
            print(y)
        else:
            print('Estos son los titulos: ')
            w.field_names = ['Titulo','Año de estreno', 'Director', 'Streamer', 'Duración', 'Cast', 'País', 'Género', 'Descripción']
            w.max_width = 10
            w.hrules = True
            w.align = "l"
            for title in lt.iterator(titulos):
                w.add_row([title['title'], title['release_year'], title['director'], title['streamer'], title['duration'], title['cast'], title['country'], title['listed_in'], title['description']])
            print(w)
    else:
        print('No se encontro el director')
    
# Funciones para medir tiempos de ejecucion
def getTime():
    '''O(1)'''
    return float(time.perf_counter()*1000)

def deltaTime(start, end):
    '''O(1)'''
    elapsed = float(end - start)
    return elapsed

def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False

#catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        #O(N)
        tipo = "ARRAY_LIST"
        #printEleccionLista()
        #input_lista = input('Seleccione una opción para continuar\n')
        #if input_lista == "1":
        #    tipo = 'SINGLE_LINKED'
        #    control = newController(tipo)
        #elif input_lista == "2":
        #    tipo = "ARRAY_LIST"
        #    control = newController(tipo)
        printEleccionArchivo1()
        input_archivo = input('Seleccione una opción para continuar\n')
        if input_archivo == "1":
            id = "small"
        elif input_archivo == "2":
            id = "5pct"
        elif input_archivo == "3":
            id = "10pct"
        elif input_archivo == "4":
            id = "20pct"
        elif input_archivo == "5":
            id = "30pct"
        elif input_archivo == "6":
            id = "50pct"
        elif input_archivo == "7":
            id = "80pct"
        elif input_archivo == "8":
            id = "large"
        else:
            print("\nDebe elegir una opción válida\n")
            break
        print("\nSe ha realizado la elección de archivo a cargar.\n")

        printTipoMap()
        input_tipo_map = input('Seleccione el tipo de mapa que desea: ')
        if input_tipo_map == "1":
            mapT = "CHAINING"
        elif input_tipo_map == "2":
            mapT = "PROBING"
        else:
            print("\nDebe elegir una opción válida\n")
            break
        print("\nSe ha realizado la elección de tipo de mapa a cargar.\n")

        input_load = float(input('¿Con qué factor de carga desea trabajar?: '))
        
        control = newController(tipo, mapT, input_load)
        mem = input('¿Desea medir memoria? (True/False) ')
        mem = castBoolean(mem)

        print("Cargando información de los archivos ....")

        charge = loadData(control, mem, id)
        tiempo = charge[1]
        streamers = {"Amazon":0,"Disney":1,"Hulu":2,"Netflix":3}
        for i in streamers:
             print('Titulos cargados de {}: \n'.format(i)+ str(charge[0][streamers[i]]))
        titulosFirst = {streamer:controller.getFirstTitles(control,streamer) for streamer in streamers}
        titulosLast = {streamer:controller.getLastTitles(control,streamer) for streamer in streamers}
        listadoFirst = [printFirstTitles(titulosFirst[i],i) for i in titulosFirst]
        listadoLast = [printLastTitles(titulosLast[i],i) for i in titulosLast]
        formato(listadoFirst,listadoLast)
        if mem:
            memoria = charge[2]
            print("Tiempo de ejecución: ", tiempo, " Memoria: ", memoria )
        else:
            print("Tiempo de ejecución: ", tiempo)

    elif inputs == "1":
        #O(NlogN)
        start_time = getTime()

        print("Introduzca a continuación los límites del periodo a consultar. Recuerde que sus respuestas deben ser años y estar en formato AAAA. \n Antes de ejecutar esta opción, asegurese de haber cargado el tamaño de archivo que desea.\n")
        lb = input("Año límite inferior: ")
        ub = input("Año limite superior: ")
        req_1_listado = requerimiento1(control,lb,ub)
        n_peliculas = lt.size(req_1_listado)
        print("\nEn el peridodo {}-{} se encontraron {} peliculas.\n\nLas principales peliculas se resumen en el siguiente recuadro:\n".format(lb,ub,n_peliculas))
        first = list(getTitles(req_1_listado,"f",3))
        last = list(getTitles(req_1_listado,"l",3))
        definitivo = [i.values() for i in first+last]
        print(tabulate(definitivo, tablefmt='grid', headers=['type','release_year','title','duration','streamer','director','cast']))

        end_time = getTime()
        delta_time = deltaTime(start_time, end_time)
        print("Delta tiempo requerimiento: {}".format(delta_time))

    elif inputs == "2": 
        #O(NlogN)
        start_time = getTime()

        print("Introduzca a continuación los límites del periodo a consultar. Recuerde que sus respuestas deben ser años y estar en formato '%'B '%'d, '%'Y. \n Antes de ejecutar esta opción, asegurese de haber cargado el tamaño de archivo que desea.\n")
        lb = input("Límite inferior: ")
        ub = input("Limite superior: ")
        req_2_listado = requerimiento2(control,lb,ub)
        n_shows = lt.size(req_2_listado)
        print("\nEn el peridodo {}-{} se encontraron {} shows de TV.\n\nLos principales shows se resumen en el siguiente recuadro:\n".format(lb,ub,n_shows))
        first = list(getTitles(req_2_listado,"f",3))
        last = list(getTitles(req_2_listado,"l",3))
        definitivo = [i.values() for i in first+last]
        print(tabulate(definitivo, tablefmt='grid', headers=['type','title','date_added','duration','release_year','streamer','director','cast']))
        #loadData(control) # Revisar si esto era solo para hacer pruebas

        end_time = getTime()
        delta_time = deltaTime(start_time, end_time)
        print("Delta tiempo requerimiento: {}".format(delta_time))
    
    elif inputs == "3":
        #O(N)
        start_time = getTime()

        actor = input("Nombre del actor que desea conocer: ")
        printActorData(control ,actor) 

        end_time = getTime()
        delta_time = deltaTime(start_time, end_time)
        print("Delta tiempo requerimiento: {}".format(delta_time))
    
    elif inputs == "4":
        #O(1)
        start_time = getTime()

        genrename = input("Genero a buscar: ")
        genero = controller.getTitlesByGenre(control, genrename)
        printGenreData(genero, genrename)

        end_time = getTime()
        delta_time = deltaTime(start_time, end_time)
        print("Delta tiempo requerimiento: {}".format(delta_time))
    
    elif inputs == "5":
        #O(NlogN)
        start_time = getTime()

        print("Introduzca a continuación el país que quiere consultar.\n Antes de ejecutar esta opción, asegurese de haber cargado el tamaño de archivo que desea.\n")
        pais = input("Escriba el país: ")
        lm,ls,lista = requerimiento5(control,pais)
        n_m = lt.size(lm)
        n_s = lt.size(ls)
        n = lt.size(lista)
        first = list(getTitles(lista,"f",3))
        last = list(getTitles(lista,"l",3))
        definitivo = [list(i.values()) for i in first+last]
        print("\nEl número de titulos por tipo de contenido son:\n")
        print(tabulate([["Movies: ",n_m],["TV Shows: ",n_s]], tablefmt='grid', headers=["Type","Number"]))
        print("\nLos contenidos ordenados son: \n")
        #print(definitivo)
        print(tabulate(definitivo, tablefmt='grid', headers=['type','title','release_year','director','streamer','duration','cast','country','listed_in','description']))

        end_time = getTime()
        delta_time = deltaTime(start_time, end_time)
        print("Delta tiempo requerimiento: {}".format(delta_time))
    
    elif inputs == "6":
        #O(N)
        start_time = getTime()

        directorname = input("Director que desea buscar: ")
        director = controller.getMoviesByDirector(control, directorname)
        printDirectorData(director,directorname) 

        end_time = getTime()
        delta_time = deltaTime(start_time, end_time)
        print("Delta tiempo requerimiento: {}".format(delta_time))
    
    elif inputs == "7":
        #O(1)
        start_time = getTime()

        topN = int(input('Buscando los Top ?: '))
        genres = control['model']['genres']
        printGenreTopN(genres, topN)

        end_time = getTime()
        delta_time = deltaTime(start_time, end_time)
        print("Delta tiempo requerimiento: {}".format(delta_time))
    
    elif inputs == "8":
        pass

    elif int(inputs[0]) == 9:
        printEleccionLista()
        input_lista = input('Seleccione una opción para continuar\n')
        if input_lista == "1":
            tipo = 'SINGLE_LINKED'
            control = newController(tipo)
        elif input_lista == "2":
            tipo = "ARRAY_LIST"
            control = newController(tipo)
        control = newController(tipo)

        print("\nSe ha realizado la elección de la representación de lista. \n")

        printEleccionArchivo0() 
        input_eleccion = input('Seleccione una opción para continuar\n')
        if input_eleccion == "1":
            printEleccionArchivo1()
            input_archivo = input('Seleccione una opción para continuar\n')
            if input_archivo == "1":
                id = "small"
            elif input_archivo == "2":
                id = "5pct"
            elif input_archivo == "3":
                id = "10pct"
            elif input_archivo == "4":
                id = "20pct"
            elif input_archivo == "5":
                id = "30pct"
            elif input_archivo == "6":
                id = "50pct"
            elif input_archivo == "7":
                id = "80pct"
            elif input_archivo == "8":
                id = "large"
            else:
                print("\nDebe elegir una opción válida\n")
                break
            print("\nSe ha realizado la elección de archivo a cargar.\n")
            loadData(control, mem, id)
            #print(moviesSize(control))

        elif input_eleccion == "2":
            input_muestra = int(input('Seleccione un tamaño de muestra válido: \n'))
            input_inicial = int(input('Seleccione una posición de inicio válida: \n'))
            check_lst = checklist(control, input_inicial, input_muestra)
            if check_lst == True:
                moviesSublist(control, input_inicial, input_muestra)
            else:
                print("La posición o el elemento de lista no son válidos.\n")

        printEleccionAlgoritmo()
        input_algoritmo = input("Seleccione una opción: \n")
        if input_algoritmo == "1":
            #O(N^2)
            result = controller.selectionSort(control)
            delta_time = f"{result[1]:.3f}"
            print("Delta tiempo Selection: ", str(delta_time))

        if input_algoritmo == "2":
            #O(N^2)
            result = controller.insertionSort(control)
            delta_time = f"{result[1]:.3f}"
            print("Delta tiempo Insertion: ", str(delta_time))

        if input_algoritmo == "3":
            #O(N^3/2)
            result = controller.shellsort(control)
            delta_time = f"{result[1]:.3f}"
            print("Delta tiempo ShellSort: ", str(delta_time))
        
        if input_algoritmo == "4":
            #O(NlogN)
            result = controller.mergesort(control)
            delta_time = f"{result[1]:.3f}"
            print("Delta tiempo MergeSort: ", str(delta_time))
        
        if input_algoritmo == "5":
            #O(N^2)
            result = controller.quicksort(control)
            delta_time = f"{result[1]:.3f}"
            print("Delta tiempo QuickSort: ", str(delta_time))

    else:
        sys.exit(0)
sys.exit(0)