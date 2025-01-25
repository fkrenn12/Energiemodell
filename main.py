from msvcrt import locking

import flet as ft
from serial_comm import serial_client
from simulator import Simulator
import threading


def main(page: ft.Page):
    def click(e=None):
        print('Button clicked')
        text.value = "Button Clicked"
        page.update()

    def slider_change(e=None):
        print(int(e.control.value * 100))
        text.value = f"Slider {int(e.control.value * 100)}"
        s1.set_solar_power(int(e.control.value * 100))
        page.update()

    def serial_input(payload: str):
        print(f'Readed from serial: {payload}')
        text.value = payload
        page.update()

    def simulator_input(payload: str):
        with lock:
            print(f'Readed from simulator: {payload}')
            text.value = payload
            page.update()

    lock = threading.Lock()
    page.title = "Energiemodell"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = ft.Padding(3, 3, 3, 0)
    page.margin = ft.Margin(0, 0, 0, 0)
    page.scroll = "adaptive"

    page.add(ft.ElevatedButton(content=ft.Text("Click me"),
                               on_click=click,
                               style=ft.ButtonStyle(bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE}),
                               ))
    page.add(ft.Text("PWM Einstellung"))
    page.add(ft.Slider(on_change=slider_change))
    text = ft.Text("Hier erscheint Ausgabetext")
    page.add(text)

    page.update()
    serial_client.register_callback(serial_input)
    # serial_client.open(port='COM2', baud_rate=115200)
    # serial_client.write()
    s1.start()
    s1.register_callback(simulator_input)


s1 = Simulator()
s2 = Simulator()

ft.app(target=main)
