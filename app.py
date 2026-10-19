from nicegui import ui
import joblib

buzon_spam = {}
buzon = {}
modelo = joblib.load("spam_pipeline.joblib")

def enviar(remi,dest,cont) -> None:
    contenido = cont.value
    clas = modelo.predict(contenido)
    if clas == 1:
        buzon_spam.update({ dest.value: {"Remitente": remi.value, "Mensaje": cont.value} })
    else:
        buzon.update({ dest.value: {"Remitente": remi.value, "Mensaje": cont.value} })


def abrir_bandeja(dest) -> None:
    destinatario_normal =dest.value

    if not destinatario_normal:
            ui.label('Por favor, ingresa un destinatario válido.').classes('text-red-500 italic')
            return

    mensaje = buzon.get(destinatario_normal)

    if not mensaje:
        ui.label(f'No hay mensajes registrados para "{destinatario_normal}".').classes('text-gray-500 italic')
        return

    with ui.card().classes('w-full p-4 bg-blue-50 border-l-4 border-blue-500 shadow-sm'):
        with ui.row().classes('items-center justify-between w-full'):
            ui.label(f"Remitente: {mensaje['Remitente']}").classes('font-semibold text-blue-900')
            ui.badge('Bandeja Principal', color='primary')
        ui.separator().classes('my-2')
        ui.label(mensaje['Mensaje']).classes('text-gray-700 whitespace-pre-line')


def abrir_spam(dest) -> None:
    destinatario_normal =dest.value

    if not destinatario_normal:
            ui.label('Por favor, ingresa un destinatario válido.').classes('text-red-500 italic')
            return

    mensaje = buzon_spam.get(destinatario_normal)

    if not mensaje:
        ui.label(f'No hay mensajes registrados para "{destinatario_normal}".').classes('text-gray-500 italic')
        return

    with ui.card().classes('w-full p-4 bg-blue-50 border-l-4 border-blue-500 shadow-sm'):
        with ui.row().classes('items-center justify-between w-full'):
            ui.label(f"Remitente: {mensaje['Remitente']}").classes('font-semibold text-blue-900')
            ui.badge('Bandeja Principal', color='primary')
        ui.separator().classes('my-2')
        ui.label(mensaje['Mensaje']).classes('text-gray-700 whitespace-pre-line')




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
                remitente = (ui.input('Remitente').props('outlined dense').classes('w-full'))
                destinatario = (ui.input('Destinatario').props('outlined dense').classes('w-full'))
                contenido = (ui.textarea('Contenido').props('outlined').classes('w-full'))
                ui.button('Enviar', icon='send', on_click=enviar(remitente,destinatario,contenido))

            with ui.tab_panel(t_bandeja):
                with ui.row().classes('w-full items-center no-wrap'):
                    des_god = (ui.input('Destinatario').props('outlined dense').classes('flex-grow'))
                    ui.button('Abrir bandeja', on_click=abrir_bandeja(des_god))
                ui.column().classes('w-full gap-3')  # aquí irán los resultados

            with ui.tab_panel(t_spam):
                with ui.row().classes('w-full items-center no-wrap'):
                    des_slop = (ui.input('Destinatario').props('outlined dense').classes('flex-grow'))
                    ui.button('Abrir spam', on_click=abrir_spam(des_slop), color='negative')
                ui.column().classes('w-full gap-3')  # aquí irán los resultados


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(title='Correo local', reload=False)