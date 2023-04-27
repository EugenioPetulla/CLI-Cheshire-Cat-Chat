import os
import json
import elements
from threading import Thread
from websocket import WebSocketApp
import readline
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich.markdown import Markdown


class UserInputThread(Thread):
    def __init__(self, ws):
        Thread.__init__(self)
        self.ws = ws
        self.waiting_for_input = False

    def update_console(self, message):
        # This method will update the console with the cat's response message
        console.print(f"🐱 [bold magenta]CHESHIRE CAT:[/bold magenta] ", end="")
        console.print(Markdown(message))

    def run(self):
        # Wait for user input only if not already waiting for input
        if not self.waiting_for_input:
            self.waiting_for_input = True
            # TODO: evaluate a ruler for separate chat console.rule("", style="white")
            user_input = Prompt.ask(Text("\n👤 HUMAN", style="bold"))

            # Check for exit command
            if user_input in ('/exit', '/close'):
                console.print("[i yellow]Closing connection...[/i yellow]")
                self.ws.close()  # Close the websocket connection
                console.print(elements.goodbye(), justify="center")
                os._exit(1)  # Exit the program

            # Send the user input as a message to the cat
            console.print("[i yellow]The Cheshire Cat is thinking...[/i yellow]")
            self.ws.send(json.dumps({"text": user_input}))

    def stop(self):
        self.waiting_for_input = False


def on_message(ws, message):
    # Stop the thread when we are not waiting for user input
    user_thread = UserInputThread(ws)
    user_thread.stop()

    # Receiving and printing the cat's response
    cat_response = json.loads(message)
    user_thread.update_console(cat_response["content"])

    # Start the user input thread to ask for new input from the user
    user_thread = UserInputThread(ws)
    user_thread.start()


def on_error(ws, error):
    # Check if the error message contains the string "WebSocketApp' object has no attribute 'pong'"
    if "WebSocketApp' object has no attribute 'pong'" in str(error):
        return
    # Otherwise, print the error message
    console.print("[red bold]Error: " + str(error) + "[/red bold]")


def on_ping(ws, ping_data):
    # Send a pong response
    ws.pong()


def on_open(ws):
    # Send a full welcome message when connected
    console.print(elements.greetings(), justify="center")

    # Request user input to start the conversation
    user_thread = UserInputThread(ws)
    user_thread.start()


# TODO: Def an on_close() function
def cat_chat():
    try:
        # Create websocket connection
        ws = WebSocketApp('ws://localhost:1865/ws',
                          on_message=on_message,
                          on_error=on_error,
                          on_open=on_open,
                          on_ping=on_ping)
        # Keep running the connection
        ws.run_forever()

    except Exception as e:
        console.print_exception()
        console.print("[red bold]Error: " + str(e) + "[/red bold]")


# Creating a console for rich output
console = Console()

cat_chat()  # TODO: Keep reconnecting to the chat in case of errors or disconnection
