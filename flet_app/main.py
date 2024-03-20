import asyncio
import websockets
import flet as ft
import time

uri = "ws://<ESP32_IP>:81"  # Replace <ESP32_IP> with the actual IP address of your ESP32
async def websocket_client(message):

    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(message)
    except asyncio.TimeoutError:
        print("Timeout occurred while waiting for a response from the ESP32.")
    except websockets.exceptions.ConnectionClosed:
        print("The connection to the ESP32 was closed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")








def main(page: ft.Page):
    page.horizontal_alignment="center"
    page.vertical_alignment="center"

    page.window_width=340
    page.window_height=650




    page.fonts = {
        "SevenSegment": "fonts/Seven Segment.ttf",  # Replace with your font file name
    }
    splash_container = ft.Container(

         ft.Image(
                src=f"im/splash.gif",
                width=310,
                height=600,
                fit=ft.ImageFit.FILL,
                border_radius=35,

            )

    )
    # Add the container to the page
    page.add(splash_container)

    # Update the page to show the splash screen
    page.update()

    # Wait for a few seconds
    time.sleep(4)

    # Remove the splash screen container
    page.remove(splash_container)

    def button_clicked1(e):
        asyncio.run(websocket_client("Task1"))

    def button_clicked2(e):
        asyncio.run(websocket_client("Task2"))
    def button_clicked3(e):
        asyncio.run(websocket_client("stop"))

    def update_counter(page, txt_counter, counter_value):
        txt_counter.value = str(counter_value)
        page.update()

    async def listen_for_counter_updates(page, txt_counter):

        async with websockets.connect(uri) as websocket:
            while True:
                counter_value = await websocket.recv()
                update_counter(page, txt_counter, counter_value)

    # Create a text widget to display the counter
    txt_counter = ft.Text(value="00", size=100, color="#4AE41C", font_family="SevenSegment")

    # Create the stack with the buttons and the text counter
    st = ft.Stack(
        [
            ft.Image(
                src="im/glow.png",
                width=340,
                height=600,
                fit=ft.ImageFit.FILL,
                border_radius=35,
            ),
            ft.Column(
                [
                    ft.ElevatedButton(
                        "BLUE LED",
                        width=250,
                        on_click=button_clicked1,
                        style=ft.ButtonStyle(shape=ft.StadiumBorder(), padding=10, bgcolor="#4AE41C"),
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                left=30,
                top=0,
                bottom=60,
                right=0
            ),
            ft.Column(
                [
                    ft.ElevatedButton(
                        "RED LED",
                        width=250,
                        on_click=button_clicked2,
                        style=ft.ButtonStyle(shape=ft.StadiumBorder(), padding=10, bgcolor="#4AE41C")
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                left=30,
                top=35,
                bottom=0,
                right=0
            ),
            ft.Column(
                [
                    ft.ElevatedButton(
                        "stop",
                        width=250,
                        on_click=button_clicked3,
                        style=ft.ButtonStyle(shape=ft.StadiumBorder(), padding=10, bgcolor="#4AE41C")
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                left=30,
                top=130,
                bottom=0,
                right=0
            ),
            ft.Column(
                [txt_counter],
                alignment=ft.MainAxisAlignment.CENTER,
                left=107,
                top=0,
                bottom=300,
                right=0
            ),
        ],
    )

    page.add(st)
    asyncio.run(listen_for_counter_updates(page, txt_counter))


ft.app(target=main,assets_dir="assets")



