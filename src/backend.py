from fastapi import FastAPI
import joblib
import sys
from pathlib import Path
import json
from datetime import datetime
import uvicorn


app = FastAPI()

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

buzon_spam = {}
buzon = {}
modelo = joblib.load('./models/spam_pipeline.joblib')
el_json = Path("mensajes.json")

# Para cargar los mensajes que ya teniamos

def cargar_json():
    if el_json.exists():
      with open(el_json, "r", encoding="utf-8") as f:
        return json.load(f)
    return {}

messages = cargar_json()

# Reconstruimos el diccionario con base al JSON

for dest, msgs in messages.items():
  for m in msgs:
    target = buzon_spam if m["spam"] == 1 else buzon
    target.setdefault(dest, []).append(
        {"Remitente": m["from"], "Mensaje": m["mes"], "Fecha": m["date"], "Hora": m["hour"]}
    )

def save_msg():
    datos_json = json.dumps(messages, indent=4, ensure_ascii=False)
    with open(el_json, 'w', encoding='utf-8') as outfile:
        outfile.write(datos_json)



@app.post("/api/enviar")
def enviar(datos: dict) -> None:

    remitente = datos.get("remitente")
    destinatario = datos.get("destinatario")
    contenido = datos.get("contenido")

    now = datetime.now()
    clas = modelo.predict([contenido])[0]

    spam = clas == 1 
    destino = buzon_spam if spam else buzon
    destino.setdefault(destinatario, []).append(
    {
        "Remitente": remitente,
        "Mensaje": contenido,
        "Fecha": now.strftime("%Y-%m-%d"),
        "Hora": now.strftime("%H:%M:%S"),
    }
)
    messages.setdefault(destinatario, []).append({
    "from": remitente,
    "mes": contenido,
    "date": now.strftime("%Y-%m-%d"),   
    "hour": now.strftime("%H:%M:%S"),    
    "spam": int(clas),
    })
    save_msg()

    return {"status": "ok", "spam": bool(spam)}


@app.get("/api/mostrar/{destinatario}")
def mostrar(destinatario:str) -> None:
   return {
        "bandeja": buzon.get(destinatario,[]),
        "spam": buzon_spam.get(destinatario,[]),
   }

uvicorn.run(app, host="127.0.0.1", port=8000)
   
   
