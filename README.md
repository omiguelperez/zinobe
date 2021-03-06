# zinobe

## Test description

|  Region | City Name |  Languaje | Time  |
|---|---|---|---|
|  Africa | Angola  |  AF4F4762F9BD3F0F4A10CAF5B6E63DC4CE543724 | 0.23 ms  |
|   |   |   |   |
|   |   |   |   |

Desarrolle una aplicacion en python que genere la tabla anterior teniendo las siguientes consideraciones:

1. De https://rapidapi.com/apilayernet/api/rest-countries-v1, obtenga todas las regiones existentes.
2. De https://restcountries.eu/ Obtenga un pais por region apartir de la region optenida del punto 1.
3. De https://restcountries.eu/ obtenga el nombre del idioma que habla el pais y encriptelo con SHA1
4. En la columna Time ponga el tiempo que tardo en armar la fila (debe ser automatico)
5. La tabla debe ser creada en un DataFrame con la libreria PANDAS
6. Con funciones de la libreria pandas muestre el tiempo total, el tiempo promedio, el tiempo minimo y el maximo que tardo en procesar toda las filas de la tabla.
7. Guarde el resultado en sqlite.
8. Genere un Json de la tabla creada y guardelo como data.json
9. La prueba debe ser entregada en un repositorio git.


**Es un plus si:**
* No usa famework
* Entrega Test Unitarios
* Presenta un diseño de su solucion.


## Run

This app is dockerized, you can run it with the following command:

`docker-compose up`

Once you run this command you will see in the console an output like that:

```bash
omiguelperez/zinobe [ docker-compose up ]
Starting python ... done
Attaching to python
python         | total time: 1.9329781532287598
python         | average time: 0.32216302553812665
python         | min time: 0.28493309020996094
python         | max time: 0.3455798625946045
python exited with code 0
```

Also, two files will be created in the `out` directory:

- `data.json` this file contains formatted execution results for first country for each region.
- `db.sqlite3` the db contains all execution logs through the time

## Test

You must run the tests inside the docker container with the command bellow:

`docker-compose run --rm zinobe-test pytest`

Once you run the test command you'll see an output like bellow:

```bash
omiguelperez/zinobe [ docker-compose run --rm zinobe-test pytest ]
Creating zinobe_zinobe-test_run ... done
=========================== test session starts ===========================
platform linux -- Python 3.9.5, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /app
collected 1 item                                                           

test/test_etl.py .                                                   [100%]
============================ 1 passed in 0.36s ============================
```