import os
import json
import elements
import requests
from threading import Thread
from websocket import WebSocketApp
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
                    console.rule("🛑 [bold red]CLOSING CONNECTION...[/bold red]", style="red")
                    self.ws.close()  # Close the websocket connection
                    console.print(elements._goodbye(), justify="center")
                    os._exit(1)  # Exit the program

                elif command == '/help':
                    console.print("\n")
                    console.rule("[bold yellow] :robot: AVAILABLE COMMANDS[/bold yellow]", style="yellow")
                    console.print(elements._help())

                elif command.startswith('/send'):
                    # Check for valid file path
                    try:
                        file_path = user_input.split()[1]
                    except IndexError:
                        console.print("\n")
                        console.rule("⚠️  [bold yellow]WARNING![/bold yellow]", style="yellow")
                        console.print("Too few arguments! Command: [i yellow]/send path/to-your/file.txt[/i yellow]", justify="center")
                        continue

                    rabbithole_url = 'http://localhost:1865/rabbithole/'

                    if os.path.isfile(file_path):
                        if not file_path.endswith(('.txt', '.pdf', '.md')):
                            console.print("\n")
                            console.rule("⚠️  [bold yellow]WARNING![/bold yellow]", style="yellow")
                            console.print("File type not supported", justify="center")
                        else:
                            with open(file_path, 'rb') as f:
                                files = {
                                    'file': (os.path.basename(file_path), f, 'text/plain')
                                }

                                headers = {
                                    'accept': 'application/json',
                                }

                                response = requests.post(rabbithole_url, headers=headers, files=files)

                                console.print("\n")
                                console.rule(":robot: [bold yellow]INFO[/bold yellow]", style="yellow")
                                console.print(response.json()["info"], justify="center")
                    else:
                        console.print("\n")
                        console.rule("⚠️  [bold yellow]WARNING![/bold yellow]", style="yellow")
                        console.print("No valid file found", justify="center")

                elif command.startswith('/link'):
                    command_args = user_input.split()[1:]
                    if len(command_args) != 1:
                        console.print("\n")
                        console.rule("⚠️  [bold yellow]WARNING![/bold yellow]", style="yellow")
                        console.print(
                            "Too few or missing arguments! Command: [i yellow]/link https://pieroit.github.io/cheshire-cat/[/i yellow]",
                            justify="center")
                    else:
                        link = command_args[0]
                        if not link.startswith(('http://', 'https://')):
                            console.print("\n")
                            console.rule("⚠️  [bold yellow]WARNING![/bold yellow]", style="yellow")
                            console.print("Invalid link format: must start with 'http://' or 'https://'", justify="center")
                        else:
                            try:
                                parsed_link = requests.get(link).url
                                data = {
                                    'url': parsed_link,
                                    'chunk_size': 400,
                                    'chunk_overlap': 100
                                }
                                headers = {
                                    'Content-Type': 'application/json',
                                    'Accept': 'application/json'
                                }
                                response = requests.post('http://localhost:1865/rabbithole/web/', headers=headers, json=data)
                                console.print(response.json()["info"])
                            except requests.exceptions.RequestException:
                                console.print("\n")
                                console.rule("⚠️  [bold red]WARNING![/bold red]", style="yellow")
                                console.print("Error: Failed to parse link", justify="center")
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

# TODO: Add a check for the notification string in order to not print them when the user input thread is open
# last_notification = ""


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
    console.print(elements._error(error))


def on_ping(ws, ping_data):
    # Send a pong response
    ws.pong()


def on_open(ws):
    # Send a full welcome message when connected
    console.print(elements._greetings(), justify="center")

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
        console.print(elements._error(e))


# Creating a console for rich output
console = Console()


cat_chat()  # TODO: Keep reconnecting to the chat in case of errors or disconnection
