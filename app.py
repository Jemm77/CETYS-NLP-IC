
from nicegui import ui




def enviar() -> None:
    #implementar Envier
    pass


def abrir_bandeja() -> None:
    #implementar Bandeja
    pass


def abrir_spam() -> None:
    #implementar spam
    pass



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
                ui.input('Remitente').props('outlined dense').classes('w-full')
                ui.input('Destinatario').props('outlined dense').classes('w-full')
                ui.textarea('Contenido').props('outlined').classes('w-full')
                ui.button('Enviar', icon='send', on_click=enviar)

            with ui.tab_panel(t_bandeja):
                with ui.row().classes('w-full items-center no-wrap'):
                    ui.input('Destinatario').props('outlined dense').classes('flex-grow')
                    ui.button('Abrir bandeja', on_click=abrir_bandeja)
                ui.column().classes('w-full gap-3')  # aquí irán los resultados

            with ui.tab_panel(t_spam):
                with ui.row().classes('w-full items-center no-wrap'):
                    ui.input('Destinatario').props('outlined dense').classes('flex-grow')
                    ui.button('Abrir spam', on_click=abrir_spam, color='negative')
                ui.column().classes('w-full gap-3')  # aquí irán los resultados


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(title='Correo local', reload=False)