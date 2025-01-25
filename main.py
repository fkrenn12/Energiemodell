import json
import time
import flet as ft
from serial_comm import serial_client
from simulator import Simulator
import threading


def main(page: ft.Page):
    def click_start(e=None):
        print('Start Button clicked')
        text.value = "Start Button Clicked"
        s1.run()
        page.update()

    def click_stop(e=None):
        print('Stop Button clicked')
        text.value = "Stop Button Clicked"
        s1.stop()
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
            payload = json.loads(payload)
            solar_power = payload['solar_power']
            text.value = solar_power
            page.update()

    lock = threading.Lock()
    page.title = "Energiemodell"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = ft.Padding(3, 3, 3, 0)
    page.margin = ft.Margin(0, 0, 0, 0)
    page.scroll = "adaptive"

    start_button = ft.ElevatedButton(content=ft.Text("Start simulation"),
                                     on_click=click_start,
                                     style=ft.ButtonStyle(bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE}),
                                     )

    stop_button = ft.ElevatedButton(content=ft.Text("Stop simulation"),
                                    on_click=click_stop,
                                    style=ft.ButtonStyle(bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE}),
                                    )

    page.add(ft.Row([start_button, stop_button], alignment=ft.MainAxisAlignment.SPACE_AROUND))
    page.add(ft.Text("PWM Einstellung"))
    page.add(ft.Slider(on_change=slider_change))
    text = ft.Text("Hier erscheint Ausgabetext")
    page.add(text)

    page.update()
    serial_client.register_callback(serial_input)
    # serial_client.open(port='COM2', baud_rate=115200)
    # serial_client.write()
    s1.register_callback(simulator_input)


s1 = Simulator()

ft.app(target=main)
