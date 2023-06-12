#!/usr/bin/python3
"""Main."""
from events import Events
import elements
from websocket import WebSocketApp
from rich.console import Console
from halo import Halo


# TODO: Add a check for the notification string in order to not print them when the user input thread is open
# last_notification = ""


def cat_chat():
    console = Console()

    spinner = Halo(text="The Cheshire Cat is thinking...", text_color="yellow", spinner="clock")
    event = Events(spinner, console)
    try:
        # Create websocket connection
        ws = WebSocketApp(
            "ws://localhost:1865/ws",
            on_message=event.on_message,
            on_error=event.on_error,
            on_open=event.on_open,
            on_ping=event.on_ping,
            on_close=event.on_close,
        )
        # Keep running the connection
        ws.run_forever()

    except Exception as e:
        console.print_exception()
        console.print(elements._error(e))


cat_chat()  # TODO: Keep reconnecting to the chat in case of errors or disconnection
