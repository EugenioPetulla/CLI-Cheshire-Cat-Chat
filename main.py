import os
import json
import elements
from threading import Thread
from websocket import WebSocketApp
import readline
from rich.console import Console
from rich.markdown import Markdown
from halo import Halo

spinner = Halo(text='The Cheshire Cat is thinking...', text_color='yellow', spinner='clock')

class UserInputThread(Thread):
    def __init__(self, ws):
        Thread.__init__(self)
        self.ws = ws

    def update_console(self, message):
        # This method will update the console with the cat's response message
        console.print("\n")
        console.rule("🐱 [bold magenta]CHESHIRE CAT:[/bold magenta] ", style="magenta")
        console.print(Markdown(message))

    def run(self):
        while True:
            console.print("\n")
            console.rule("👤 [bold]HUMAN[/bold]", style="white")
            user_input = input()

            # Check for exit command
            if user_input.startswith('/'):
                command = user_input.split()[0]
                if command == '/exit' or command == '/close':
                    console.print("\n")
                    console.rule("🛑 [bold red]CLOSING CONNECTION...[/bold red]")
                    self.ws.close()  # Close the websocket connection
                    console.print(elements.goodbye(), justify="center")
                    os._exit(1)  # Exit the program
                elif command == '/help':
                    console.print("\n")
                    console.rule("[bold yellow] :robot: AVAILABLE COMMANDS[/bold yellow]")
                    console.print(elements.help())
                else:
                    # User entered a non-/ command, break out of the loop and send the message
                    break
            else:
                # User entered a message, break out of the loop and send the message
                break

        # Send the user input as a message to the cat
        spinner.start()
        self.ws.send(json.dumps({"text": user_input}))

        # Wait for the cat's response
        self.waiting_for_input = True

        def stop(self):
            self.waiting_for_input = False



def on_message(ws, message):
    # Stop the spinner and print the cat's response
    spinner.stop()
    spinner.clear()

    user_thread = UserInputThread(ws)
    cat_response = json.loads(message)
    user_thread.update_console(cat_response["content"])

    # Start the user input thread to ask for new input from the user
    user_thread.start()


def on_error(ws, error):
    # Check if the error message contains the string "WebSocketApp' object has no attribute 'pong'"
    if "WebSocketApp' object has no attribute 'pong'" in str(error):
        return
    # Otherwise, print the error message
    console.print(elements.error(error))


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
        console.print(elements.error(e))

# Creating a console for rich output
console = Console()

cat_chat()  # TODO: Keep reconnecting to the chat in case of errors or disconnection
