# App final: contador de tareas pendientes
# Objetivo: mantener un dato derivado (el contador) sincronizado con el estado.
import flet as ft


def main(page: ft.Page):
    page.title = "Lista de tareas"
    page.padding = 20

    titulo = ft.Text("Mis tareas", size=30, weight=ft.FontWeight.BOLD)
    nueva_tarea = ft.TextField(label="Nueva tarea", expand=True, on_submit=lambda e: añadir_tarea(e))
    #2. Le ponemos el color rojo para que sea rojo desde el inicio, ya que empieza por 0 tareas.
    contador = ft.Text("Tareas pendientes: 0", color=ft.Colors.RED)
    tareas = ft.Column()

    def actualizar_contador(e=None):
        # controls[0] de cada fila es el Checkbox; value=False => pendiente
        pendientes = sum(1 for fila in tareas.controls if not fila.controls[0].value)
        contador.value = f"Tareas pendientes: {pendientes}"

        #2. Si hay 0 tareas, es decir ninguna, el texto sigue rojo si hay más de 0 cambia a verde.
        if (pendientes) == 0:
            contador.color = ft.Colors.RED
        else:
            contador.color = ft.Colors.GREEN
        page.update()

    def eliminar_tarea(fila):
        tareas.controls.remove(fila)
        actualizar_contador()

    #4. Función para poder guardar el cambio una vez editada la tarea
    def guardar_tarea(fila, campo):
        texto = campo.value.strip()

        if not texto:
            campo.error = "Escribe una tarea"
            page.update()
            return

        for otra_fila in tareas.controls:
            if otra_fila != fila and otra_fila.controls[0].label.lower() == texto.lower():
                campo.error = "Esta tarea ya existe"
                page.update()
                return

        fila.controls[0] = ft.Checkbox(
                label=texto,
                expand=True,
                on_change=actualizar_contador
            )
        page.update()

    #4. Función para modificar una tarea.
    def modificar_tarea(fila):

        texto = fila.controls[0]

        campo = ft.TextField(
            value=texto.label,
            expand=True,
            on_submit=lambda e: guardar_tarea(fila, campo)
        )
        fila.controls[0] = campo
        page.update()

    def añadir_tarea(e):
        texto = nueva_tarea.value.strip()

        if not texto:
            nueva_tarea.error = "Escribe una tarea"
            page.update()
            return
        
        #1. Evitar que se repitan tareas, además añado un sombreado en rojo a la tarea en la fila donde está duplicada.
        for fila in tareas.controls:
            fila.controls[0].label_style = None
            if fila.controls[0].label.lower() == texto.lower():
                fila.controls[0].label_style = ft.TextStyle(bgcolor=ft.Colors.RED_100)
                nueva_tarea.error = "Esta tarea ya existe"
                page.update()
                return

        nueva_tarea.error = None
        fila = ft.Row()
        fila.controls = [
            # on_change se dispara al marcar/desmarcar el checkbox
            ft.Checkbox(label=texto, expand=True, on_change=actualizar_contador),

            #4. Añadimos botón para editar, se añade en fila.controls para que cada tarea (fila) tenga su botón editar.
            ft.IconButton(
                icon=ft.Icons.EDIT,
                icon_color=ft.Colors.BLUE_400,
                on_click=lambda e: modificar_tarea(fila),
            ),
            
            ft.IconButton(
                icon=ft.Icons.DELETE,
                icon_color=ft.Colors.RED_400,
                on_click=lambda e: eliminar_tarea(fila),
            ),
        ]
        tareas.controls.append(fila)
        nueva_tarea.value = ""
        actualizar_contador()

    #3. Creamos una función para borrar las tareas completadas/marcadas.
    def borrar_completadas(e):
        for fila in tareas.controls[:]:
            if fila.controls[0].value:
                tareas.controls.remove(fila)
        actualizar_contador()

    boton = ft.Button(content="Añadir", on_click=añadir_tarea)

    #3. Creamos el botón que ejecute la función al pulsarlo y lo añadimos al page.
    boton_borrar = ft.Button(content="Limpiar tareas completadas", on_click=borrar_completadas)

    page.add(titulo, ft.Row([nueva_tarea, boton]), contador, tareas, boton_borrar)


ft.run(main)
