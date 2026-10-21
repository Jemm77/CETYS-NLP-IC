from nicegui import ui
import joblib
import sys
from pathlib import Path
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

buzon_spam = {}
buzon = {}
modelo = joblib.load(r"./models/spam_pipeline.joblib")
messages = {}
now = datetime.now()



def save_msg():
    datos_json = json.dumps(messages, indent=4, ensure_ascii=False)
    with open('messages.json', 'w', encoding='utf-8') as outfile:
        outfile.write(datos_json)


def enviar(remi, dest, cont) -> None:
    if not dest.value or not cont.value:
        ui.notify('Completa destinatario y contenido.', color='negative')
        return

    clas = modelo.predict([cont.value])[0]

    spam = clas == 1 
    destino = buzon_spam if spam else buzon
    destino.setdefault(dest.value, []).append(
        {"Remitente": remi.value, "Mensaje": cont.value}
    )
    messages.setdefault(dest.value, []).append({
    "from": remi.value,
    "mes": cont.value,
    "date": now.strftime("%Y-%m-%d"),   
    "hour": now.strftime("%H:%M:%S"),    
    "spam": int(clas),
})
    save_msg()



def mostrar(origen: dict, dest, contenedor, etiqueta: str, color: str) -> None:
    contenedor.clear()
    nombre = dest.value
    with contenedor:
        if not nombre:
            ui.label('Por favor, ingresa un destinatario válido.').classes('text-red-500 italic')
            return

        mensajes = origen.get(nombre)
        if not mensajes:
            ui.label(f'No hay mensajes registrados para "{nombre}".').classes('text-gray-500 italic')
            return

        for m in mensajes:
            with ui.card().classes('w-full p-4 shadow-sm'):
                with ui.row().classes('items-center justify-between w-full'):
                    ui.label(f"Remitente: {m['Remitente']}").classes('font-semibold')
                    ui.badge(etiqueta, color=color)
                ui.separator().classes('my-2')
                ui.label(m['Mensaje']).classes('whitespace-pre-line')


@ui.page('/')
def principal() -> None:
    ui.label('Correo local').classes('text-2xl font-bold mx-auto mt-4')

    with ui.column().classes('w-full max-w-2xl mx-auto'):
        with ui.tabs().classes('w-full') as tabs:
            t_enviar = ui.tab('Enviar', icon='send')
            t_bandeja = ui.tab('Bandeja de entrada', icon='inbox')
            t_spam = ui.tab('Spam', icon='report')

        with ui.tab_panels(tabs, value=t_enviar).classes('w-full'):
            with ui.tab_panel(t_enviar):
                remitente = ui.input('Remitente').props('outlined dense').classes('w-full')
                destinatario = ui.input('Destinatario').props('outlined dense').classes('w-full')
                contenido = ui.textarea('Contenido').props('outlined').classes('w-full')
                ui.button('Enviar', icon='send',
                          on_click=lambda: enviar(remitente, destinatario, contenido))

            with ui.tab_panel(t_bandeja):
                res_bandeja = ui.column().classes('w-full gap-3')
                with ui.row().classes('w-full items-center no-wrap'):
                    des_bandeja = ui.input('Destinatario').props('outlined dense').classes('flex-grow')
                    ui.button('Abrir bandeja',
                              on_click=lambda: mostrar(buzon, des_bandeja, res_bandeja,
                                                       'Bandeja Principal', 'primary'))

            with ui.tab_panel(t_spam):
                res_spam = ui.column().classes('w-full gap-3')
                with ui.row().classes('w-full items-center no-wrap'):
                    des_spam = ui.input('Destinatario').props('outlined dense').classes('flex-grow')
                    ui.button('Abrir spam', color='negative',
                              on_click=lambda: mostrar(buzon_spam, des_spam, res_spam,
                                                       'Spam', 'negative'))


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(title='Correo local', reload=False)