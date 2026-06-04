# proyecto-da-promo-67-modulo2-team-3
# **PROYECTO MUSICSTREAM: LAS DIVAS DE LA MÚSICA**
Las mujeres en la música a lo largo de los años (desde la década de los 50 del siglo XX hasta la actualidad).

## **DESCRIPCIÓN Y OBJETIVO**
Proyecto sobre las mujeres en la música en el que se hace un recorrido a través de diversas cantantes femeninas desde la década de los 50 hasta la actualidad.
Para la realización de dicho estudio, hemos obtenido información de dos fuentes:
-La API de Deezer: Deezer Web API(es precisor loguearse).
-La API de last.fm (también hay que loguearse y además obtener un API KEY).
De la primera, hemos extraido títulos de canciones, los álbumes en que se integran, si eran colaboraciones, el año de lanzamiento de esas canciones y su género (pop, rock, flamenco…).
De la API de last.fm, hemos sacado la biografía de las cantantes, datos de popularidad y estadísticas de reproducción, así como un listado de artistas similares.
A partir de todos estos datos, construimos una base de datos relacional: `musicstream`, formada por tres tablas: 
-`artistas`
-`canciones`
-`informacion_artistas`
El **objetivo** es poder hacer las consultas que en cada momento concreto nos interesen, con la información y los datos de estas cantantes que tenemos en la base musicstream.

## **TECNOLOGÍAS UTILIZADAS**
- Python
- Pandas
- Numpy
- Jupyter Notebook
- MySQL

## **INSTALACIÓN Y CÓDIGO**
1. Clonar el repositorio.
2. Realizar las instalaciones y las importaciones necesarias:
-Request,
-Pandas,
-Numpy,
-MySQL connector,
-Os,
-Load_dotenv
-Glob
3. Crear un fichero .env con la contraseña de MySQL.
4. Ejecutar el Jupiter Notebook.

Resumen del código utilizado en el Jupiter Notebook:

-Función Def,  ```def conseguir_canciones(artist_name, limit=50)``` 
para obtener la información de Deezer, que contiene: 
- Llamada al endpoint de Deezer:  ```url = "https://api.deezer.com/search"```  
- Límite de 50: para que no busque más de 50 canciones por artista: ```Limit=50``` 
- Try/except: que nos dará error, indicándonos cual, si se produce algún fallo en la petición a Deezer.
- Bucle for que itera por las canciones, creando un diccionario para añadir los datos que necesitamos y finalmente nos devuelve el resultado en un data frame. 
```for cancion in canciones:```  

Se va llamando a la función Def con el nombre de cada intérprete.
-A continuación, se convierten los data frame en ficheros csv y finalmente se concatenan los datos de todas las artistas: ``` pd.concat``` .
-Función Def para obtener la información de last.fm (antes llamada al API KEY), que contiene la petición al endpoint, retornando los datos de las cantantes igualmente en un data frame, que se vuelven a pasar a csv y a concatenar. 

-Try/Except para conectar Python con MySQL, (antes hemos metido la clave de MySQL en un fichero .env) que nos devuelve el error concreto si la conexión es fallida.
-Creación de la base de datos `musicstream`: Try/Except, que contiene la conexión al cursor y que igualmente determina el error si la conexión no es exitosa.
```CREATE DATABASE IF NOT EXISTS musicstream``` 
-Nueva llamada al cursor porque lo necesitaremos posteriormente y apertura de la base de datos para la creación de las tablas a las que va a alojar.
```cursor = connection.cursor()```
```cursor.execute("use musicstream")``` 
-Creación de la primera tabla: `artistas`.
```CREATE TABLE artistas``` 
-Inserción de los datos en la tabla artistas con el correspondiente ```commit```.
-Creación de la segunda tabla: `canciones`.
```CREATE TABLE canciones``` 
-Inserción de datos en la segunda tabla. 
Y ```commit```. 
-Creación de la tercera tabla: `información_artistas`.
```CREATE TABLE informacion_artistas``` 
-Inserción de datos en la tercera tabla y de nuevo```commit```.
-Cerrar el cursor y la conexion entre MySQL y Python.
```cursor.close()```
```conection.close()```
```print("Conexion cerrada")``` 

## **RETOS AFRONTADOS**
La unificación de código, puesto que el equipo lo componen cuatro personas, optándose por elegir el más completo y por hacer aportaciones las demás.
Se afrontó el reto en la inserción de datos en las tablas porque algunos nombres de las cantantes aparecían escritos de forma diferente en distintas partes del código por lo que hubo que corregir en una de las partes del mismo y volver a concatenar.
Por otro lado, algunas intérpretes aparecían repetidas una vez hecha la inserción en la tabla artistas. Se vió que era un tema de colocación del commit. Se cambió, por tanto, al lugar adecuado, y se solucionó el error.
Hubo también un caso de duplicidad de ficheros csv y de extravío de los mismos. Una vez encontrados, se eliminaron los sobrantes y también se resolvió el reto satisfactoriamente, viendo la importancia del orden en el directorio de carpetas.

## **USO**
Realización de consultas a la base de datos musicstream para obtener la información que nos interese en cada momento acerca de las cantantes que están en la misma.

## **NOTA**
En lo referente a la obtención de datos, se sube el código con el nombre de algunas artistas, no de todas porque se considera suficiente para ver como se han obtenido dichos datos. Con el resto de cantantes, bastaría cambiar el nombre y tendríamos sus datos también.

## **AUTORAS**
-Teresa Díaz-Toledo Fernández
-Natividad de María Guerrero Opazo
-Rocío Insunza González
-Cristina Sáenz Llorente

