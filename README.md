## TMS script
## Indice
1. [Informacion](#Informacion)
2. [Tecnologías](#tecnologías)
3. [Instalación](#Instalación)
4. [Funciones](#Funciones)
5. [Pendiente](#Pendiente)
### Informacion
***
Script para agregar paquetes a rutas de entregas y quitar paquetes que se encuentren en estas a través de Google sheets
## Tecnologías
***
Librerias y tecnologías utilizadas:
* [Python](https://www.python.org/doc/) Version 3.10
* [Selenium](https://www.selenium.dev/documentation/): Version 4.8.0
* [Gspread](https://docs.gspread.org/en/v5.7.0/): Version 5.7.2
* [Oauth2client](https://pypi.org/project/oauth2client/): Version 4.1.3
* [Requests](https://requests.readthedocs.io/en/latest/): Version 2.28.2
* [Pip](https://pypi.org/project/pip/) Version 22.0.2
* [VirtualEnv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment) Version 20.17.1

## Instalación
***
Para utilizar el script realice lo siguiente: 
```
$ git clone https://github.com/joaquinreyero/clicOH.git
$ cd ../path/to/the/file
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ cd add_package
$ python3 main.py
```
Acceder y cargar datos en la [sheet](https://docs.google.com/spreadsheets/d/1gsEMX7k610Wdv98WpxIrsezxR94qDknzKntZ0sBHTcU/edit#gid=0&fvid=1238780444)
## Funciones
***
El programa dispone de dos funciones principales:
1. **Agregar paquetes a rutas de entrega** 
2. **Desactivar route details**

## Agregar paquetes a rutas de entrega:
La funcion toma de la sheet rutas y paquetes de las respectivas columnas, agregar los
paquetes de ser posible, sincroniza las rutas y deja el paquete en un estado valido para volverse a rutear. De no ser 
posible alguna de las acciones nos muestra el error que tiene.
### **Condiciones**:
1. El tipo de ruta a la que deseamos agregar paquetes debe ser de **entrega**
2. La ruta debe que deseamos agregar el paquete tener el estado **traveling**
3. La ruta debe **existir**
4. El paquete debe **existir**
5. El paquete debe estar en alguno de los siguientes estados: **traveling_mid_mile** , **on_lookup_batch**, **1st_mile**, **ready**, **at_destination**, **dispatched** o **last_mile**
6. El paquete **no** debe estar ya **incluido** en la ruta.

## Desactivar route details
La funcion toma de la sheet rutas y paquetes de las respectivas columnas, desactiva los routes details que se requieran
y deja los paquetes en un estado valido para rutearse nuevamente, siempre y cuando estos estados no sean: canceled, delivered o arrived.

### Condiciones:
1. La ruta del route detail a desactivar debe **existir** 
2. El paquete que deseamos quitar debe **existir**
3. El paquete que se desea eliminar debe **estar en la ruta** que nos envian

***
## Pendiente

1. **Testing**
2. **Robustez**
2. **Refactor** 
3. **Mejorar tiempos de ejecución**
5. **Hacer alguna metrica**
