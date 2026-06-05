# 🎵 MUSICSTREAM: LAS DIVAS DE LA MÚSICA

Las mujeres en la música a lo largo de los años (desde la década de los 50 del siglo XX hasta la actualidad).

## 📌 Descripción del proyecto

**MusicStream: Las Divas de la Música** es un proyecto sobre las mujeres en la música en el que se hace un recorrido a través de diversas cantantes femeninas desde la década de los 50 hasta la actualidad.
A través de distintas APIs musicales, se recopilan datos sobre artistas femeninas de diferentes décadas para construir una base de datos relacional que permita analizar:

* La evolución de los géneros musicales.
* El impacto y popularidad de las artistas.
* La aparición de colaboraciones musicales.
* La evolución del consumo musical femenino.
* Las diferencias entre generaciones de artistas.

El proyecto combina extracción de datos, limpieza, transformación, almacenamiento en SQL y análisis mediante consultas.

---

# 🎯 Objetivos

El objetivo principal del proyecto es construir una base de datos relacional llamada `musicstream` que permita realizar consultas y análisis sobre mujeres artistas en la música a lo largo del tiempo.

Algunas preguntas que se pretenden responder son:

* ¿Las artistas actuales llegan a más público que las antiguas?
* ¿Qué géneros dominaron cada década?
* ¿Las colaboraciones musicales son más frecuentes hoy en día?
* ¿Qué artistas tienen mayor impacto en reproducciones?
* ¿Cómo ha evolucionado el consumo musical femenino?

---

# 🛠️ Tecnologías utilizadas

* Python
* Pandas
* NumPy
* Jupyter Notebook
* MySQL
* APIs REST
* Deezer API
* Last.fm API

---

# 📂 Estructura de la base de datos

La base de datos `musicstream` está formada por tres tablas principales:

## Tabla `artistas`

Contiene la información básica de cada cantante.

| Campo          | Tipo    |
| -------------- | ------- |
| id_artista     | INT     |
| nombre_artista | VARCHAR |

---

## Tabla `canciones`

Contiene información sobre canciones, álbumes y colaboraciones.

| Campo           | Tipo    |
| --------------- | ------- |
| id_cancion      | INT     |
| id_artista      | INT     |
| titulo_cancion  | VARCHAR |
| titulo_album    | VARCHAR |
| tipo            | VARCHAR |
| año_lanzamiento | INT     |
| genero          | VARCHAR |
| id_genero       | INT     |

---

## Tabla `informacion_artistas`

Contiene estadísticas y datos adicionales obtenidos desde Last.fm.

| Campo              | Tipo   |
| ------------------ | ------ |
| id_info            | INT    |
| id_artista         | INT    |
| biografia          | TEXT   |
| listeners          | BIGINT |
| playcount          | BIGINT |
| artistas_similares | TEXT   |

---

# 🌐 Fuentes de datos

## Deezer API

De Deezer se obtuvieron:

* Títulos de canciones.
* Álbumes.
* Tipo de lanzamiento.
* Colaboraciones.
* Géneros musicales.
* Año de lanzamiento.

Endpoint utilizado:

```python
https://api.deezer.com/search
```

---

## Last.fm API

De Last.fm se extrajeron:

* Biografías de artistas.
* Número de listeners.
* Playcount.
* Artistas similares.

Endpoint utilizado:

```python
http://ws.audioscrobbler.com/2.0/
```

Método utilizado:

```python
artist.getInfo
```

---

# ⚙️ Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/usuario/proyecto-da-promo-67-modulo2-team-3.git
```

---

## 2. Instalar dependencias

```bash
pip install pandas numpy requests mysql-connector-python python-dotenv
```

---

## 3. Crear archivo `.env`

Crear un fichero `.env` con la contraseña de MySQL:

```env
MYSQL_PASSWORD=tu_contraseña
```

---

## 4. Ejecutar Jupyter Notebook

```bash
jupyter notebook
```

---

# 🧠 Funcionamiento del proyecto

## Extracción de datos desde Deezer

Se creó una función para obtener información de canciones y álbumes:

```python
def conseguir_canciones(artist_name, limit=50)
```

La función:

* Llama a la API de Deezer.
* Obtiene hasta 50 canciones por artista.
* Extrae:

  * canciones
  * álbumes
  * género
  * colaboraciones
  * año de lanzamiento
* Devuelve la información en un DataFrame.

Posteriormente:

* cada DataFrame se exporta a CSV.
* todos los CSV se concatenan usando:

```python
pd.concat()
```

---

## Extracción de datos desde Last.fm

Se creó otra función para obtener:

* biografía
* listeners
* playcount
* artistas similares

usando:

```python
artist.getInfo
```

La información también se exporta a CSV y posteriormente se concatena.

---

## Creación de la base de datos

Se realizó la conexión entre Python y MySQL mediante:

* `mysql.connector`
* variables de entorno (`dotenv`)
* bloques `try/except`

Creación de la base de datos:

```sql
CREATE DATABASE IF NOT EXISTS musicstream;
```

---

## Creación de tablas

Se crearon las tablas:

```sql
CREATE TABLE artistas;
CREATE TABLE canciones;
CREATE TABLE informacion_artistas;
```

---

## Inserción de datos

Los datos de los CSV fueron insertados desde Python mediante:

* lectura con pandas
* bucles `for`
* queries `INSERT INTO`
* `commit()` para guardar cambios

---

# 📊 Ejemplos de consultas realizadas

* Género dominante por década.
* Artistas con más colaboraciones.
* Evolución de álbumes por época.
* Relación entre listeners y playcount.
* Diversidad musical por artista.
* Impacto musical por generaciones.

---

# 🚧 Retos afrontados

## Unificación del código

El proyecto fue desarrollado por cuatro integrantes, por lo que fue necesario:

* unificar estilos de código
* fusionar funciones
* organizar estructuras comunes

---

## Duplicados y errores en nombres

Algunos nombres de artistas aparecían escritos de forma distinta entre distintos datasets, lo que generaba errores en las relaciones entre tablas.

Fue necesario:

* limpiar datos
* corregir nombres
* regenerar CSVs

---

## Inserción duplicada de artistas

Se detectaron duplicados en la tabla `artistas` debido a la ubicación incorrecta de `commit()`.

El problema se resolvió reorganizando la inserción de datos.

---

## Gestión de archivos CSV

Hubo problemas de duplicidad y pérdida de archivos CSV, lo que puso de manifiesto la importancia de una correcta organización de carpetas y control de versiones.


📝 Nota

En lo referente a la obtención de datos, el repositorio incluye únicamente el código de extracción de algunas artistas representativas, ya que se considera suficiente para mostrar el funcionamiento del proceso completo de extracción y tratamiento de datos.

Para obtener información del resto de artistas, bastaría con modificar el nombre de la cantante en las funciones ya desarrolladas.

Somos conscientes de que el proceso podría haberse optimizado mediante una función automatizada capaz de extraer los datos de todas las artistas de forma simultánea, reduciendo considerablemente la cantidad de código repetido. Sin embargo, se optó por una aproximación más manual y controlada debido a limitaciones de tiempo y para minimizar el riesgo de pérdida de datos ante posibles fallos de ejecución, cierres inesperados de Python o problemas del equipo durante la extracción masiva de información.

Por ello, se priorizó la estabilidad del proceso y la correcta obtención de los datos frente a una automatización más compleja.

---

# 👩‍💻 Autoras

* Teresa Díaz-Toledo Fernández
* Natividad de María Guerrero Opazo
* Rocío Insunza González
* Cristina Sáenz Llorente