# CETYS-NLP-IC
Repositorio del segundo proyecto de la materia de Inteligencia computacional

Para la ejecuccion correcta de este proyecto es necesario utilizar python dentro de un entorno virtual.
Dentro de la terminal los siguientes comandos

python3.14 -m venv .venv
source .venv/bin/activate
python3.14 -m pip install -r requirements.txt

Antes de poder correr la aplicacion de mensajes puede que sea necesario ejecutar el modelo de clasificacion.
para entrenearlo ejecutar los siguientes comandos en la terminal

python load_data.py
python -m src.preprocessors.py
python -m src.tfidf.py
python -m src.train.py

El modelo ahora esta entrenado