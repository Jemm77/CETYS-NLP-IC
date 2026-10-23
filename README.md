Repositorio del segundo proyecto de la materia de Inteligencia computacional

Es necesario descargar el data set de SMS Spam Collection de UCI del siguiente 
https://archive.ics.uci.edu/dataset/228/sms%2Bspam%2Bcollection y colocarlo en una carpeta dentro del proyecto llamada "data"


Para la ejecuccion correcta de este proyecto es necesario utilizar python dentro de un entorno virtual.
Dentro de la terminal ejecutar los siguientes comandos:

python3.14 -m venv .venv
source .venv/bin/activate
python3.14 -m pip install -r requirements.txt

Antes de poder correr la aplicacion de mensajes puede que sea necesario ejecutar el modelo de clasificacion.
para entrenearlo ejecutar los siguientes comandos en la terminal

Si en su repositorio no se encuentra la carpeta models agregela con el siguiente comando en la terminal

mkdir models

python src/load_data.py
python src/preprocessors.py

El siguiente comando es opcional de ejecutar, se usa para hacer comparaciones con TFIDF
python -m src.tfidf

python -m src.train

El modelo ahora esta entrenado.

Para la aplicacion se debe lanzar el servidor y despues la aplicacion 

python src/backend.py 

Ejectutar en otra terminal

python src/app.py

