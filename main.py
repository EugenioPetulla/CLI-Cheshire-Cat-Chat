import json
import elements
from rich import print
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from websocket import WebSocketApp


def user_message(ws):
    # Ask the user for their response and send it through the websocket
    user_input = Prompt.ask(Text("\n👤 HUMAN", style="bold"))
    ws.send(json.dumps({"text": user_input}))

def on_message(ws, message):
    # Receiving and printing the cat's response
    cat_response = json.loads(message)
    print("\n🐱 [bold magenta]CHESHIRE CAT: [/bold magenta][bold]" + cat_response["content"] + "[/bold]")
    user_message(ws)


def on_error(ws, error):
    # Check if the error message contains the string "WebSocketApp' object has no attribute 'pong'"
    if "WebSocketApp' object has no attribute 'pong'" in str(error):
        return
    # Otherwise, print the error message
    console.print("[red bold]Error: " + str(error) + "[/red bold]")


def on_close(ws):
    # Send disconnected message if disconnected
    console.print("[bold red]Disconnected from chat[/bold red]")


def on_ping(ws, ping_data):
    # Send a pong response
    ws.send("pong")


def on_open(ws):
    # Send a full welcome message when connected
    console.print(elements.greetings())

    # Taking user input and sending it through the websocket
    user_message(ws)


def cat_chat():
    try:
        # Create websocket connection
        ws = WebSocketApp('ws://localhost:1865/ws',
                          on_message=on_message,
                          on_error=on_error,
                          on_close=on_close,
                          on_open=on_open,
                          on_ping=on_ping)
        # Keep running the connection
        ws.run_forever()

    except Exception as e:
        console.print_exception()
        console.print("[red bold]Error: " + str(e) + "[/red bold]")


# Creating a console for rich output
console = Console()

cat_chat() # Keep reconnecting to the chat in case of errors or disconnection
