
from httpx import AsyncClient
from nicegui import ui


async def enviar(remi, dest, cont):
  if not dest.value or not cont.value:
    ui.notify("Completa destinatario y contenido.", color="negative")
    return

  async with AsyncClient() as client:
    response = await client.post(
        f"{"http://localhost:8000"}/api/enviar",
        json={
            "remitente": remi.value,
            "destinatario": dest.value,
            "contenido": cont.value,
        },
    )


async def mostrar(dest, contenedor, tipo: str, etiqueta: str, color: str):
  contenedor.clear()
  nombre = dest.value
  with contenedor:
    if not nombre:
      ui.label(
          "Ingresa algo"
      ).classes("text-red-500 italic")
      return

    async with AsyncClient() as client:
      try:
        response = await client.get(f"http://localhost:8000/api/mostrar/{nombre}")
        if response.status_code == 200:
          data = response.json()
          mensajes = data.get(tipo, [])

          if not mensajes:
            ui.label(
                f'No hay mensajes registrados para "{nombre}".'
            ).classes("text-gray-500 italic")
            return

          for m in mensajes:
            with ui.card().classes("w-full p-4 shadow-sm"):
              with ui.row().classes("items-center justify-between w-full"):
                with ui.row().classes("items-center gap-3"):
                  ui.label(f"Remitente: {m['Remitente']}").classes(
                      "font-semibold"
                  )
                  ui.label(f"{m['Fecha']} {m['Hora']}").classes(
                      "text-sm text-gray-500"
                  )
                ui.badge(etiqueta, color=color)
              ui.separator().classes("my-2")
              ui.label(m["Mensaje"]).classes("whitespace-pre-line")
        else:
          ui.label("Error al consultar el servidor.").classes(
              "text-red-500 italic"
          )
      except Exception as e:
        ui.label(f"Error de conexión: {e}").classes("text-red-500 italic")


@ui.page("/")
def principal() -> None:
  ui.label("Correo local").classes("text-2xl font-bold mx-auto mt-4")

  with ui.column().classes("w-full max-w-2xl mx-auto"):
    with ui.tabs().classes("w-full") as tabs:
      t_enviar = ui.tab("Enviar", icon="send")
      t_bandeja = ui.tab("Bandeja de entrada", icon="inbox")
      t_spam = ui.tab("Spam", icon="report")

    with ui.tab_panels(tabs, value=t_enviar).classes("w-full"):
      with ui.tab_panel(t_enviar):
        remitente = ui.input("Remitente").props("outlined dense").classes("w-full")
        destinatario = (
            ui.input("Destinatario").props("outlined dense").classes("w-full")
        )
        contenido = ui.textarea("Contenido").props("outlined").classes("w-full")
        ui.button(
            "Enviar",
            icon="send",
            on_click=lambda: enviar(remitente, destinatario, contenido),
        )

      with ui.tab_panel(t_bandeja):
        res_bandeja = ui.column().classes("w-full gap-3")
        with ui.row().classes("w-full items-center no-wrap"):
          des_bandeja = (
              ui.input("Destinatario")
              .props("outlined dense")
              .classes("flex-grow")
          )
          ui.button(
              "Abrir bandeja",
              on_click=lambda: mostrar(
                  des_bandeja,
                  res_bandeja,
                  "bandeja",
                  "Bandeja Principal",
                  "primary",
              ),
          )

      with ui.tab_panel(t_spam):
        res_spam = ui.column().classes("w-full gap-3")
        with ui.row().classes("w-full items-center no-wrap"):
          des_spam = (
              ui.input("Destinatario")
              .props("outlined dense")
              .classes("flex-grow")
          )
          ui.button(
              "Abrir spam",
              color="negative",
              on_click=lambda: mostrar(
                  des_spam, res_spam, "spam", "Spam", "negative"
              ),
          )


if __name__ in {"__main__", "__mp_main__"}:
  ui.run(port=8080, title="Correo local Frontend", reload=False)