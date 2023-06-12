"""InputThread."""

from rich.markdown import Markdown
from threading import Thread
import requests
import os
import json
import elements


class UserInputThread(Thread):
    def __init__(self, ws, console, spinner):
        Thread.__init__(self)
        self.ws = ws
        self.console = console
        self.spinner = spinner

    def update_console(self, message):
        # This method will update the console with the cat's response message
        self.console.print("\n")
        self.console.rule("🐱 [bold magenta]CHESHIRE CAT:[/bold magenta] ", style="magenta")
        self.console.print(Markdown(message))

    def run(self):
        while True:
            self.console.print("\n")
            self.console.rule("👤 [bold]HUMAN[/bold]", style="white")
            user_input = input()

            # Check for exit command
            if user_input.startswith("/"):
                command = user_input.split()[0]
                if command == "/exit" or command == "/close":
                    self.console.print("\n")
                    self.console.rule("🛑 [bold red]CLOSING CONNECTION...[/bold red]", style="red")
                    self.ws.close()  # Close the websocket connection
                    self.console.print(elements._goodbye(), justify="center")
                    os._exit(1)  # Exit the program

                elif command == "/help":
                    self.console.print("\n")
                    self.console.rule("[bold yellow] :robot: AVAILABLE COMMANDS[/bold yellow]", style="yellow")
                    self.console.print(elements._help())

                elif command.startswith("/send"):
                    # Check for valid file path
                    try:
                        file_path = user_input.split()[1]
                    except IndexError:
                        self.console.print("\n")
                        self.console.rule("⚠️  [bold yellow]WARNING![/bold yellow]", style="yellow")
                        self.console.print(
                            "Too few arguments! Command: [i yellow]/send path/to-your/file.txt[/i yellow]",
                            justify="center",
                        )
                        continue

                    rabbithole_url = "http://localhost:1865/rabbithole/"

                    if os.path.isfile(file_path):
                        if not file_path.endswith((".txt", ".pdf", ".md")):
                            self.console.print("\n")
                            self.console.rule("⚠️  [bold yellow]WARNING![/bold yellow]", style="yellow")
                            self.console.print("File type not supported", justify="center")
                        else:
                            with open(file_path, "rb") as f:
                                files = {"file": (os.path.basename(file_path), f, "text/plain")}

                                headers = {
                                    "accept": "application/json",
                                }

                                response = requests.post(rabbithole_url, headers=headers, files=files)

                                self.console.print("\n")
                                self.console.rule(":robot: [bold yellow]INFO[/bold yellow]", style="yellow")
                                self.console.print(response.json()["info"], justify="center")
                    else:
                        self.console.print("\n")
                        self.console.rule("⚠️  [bold yellow]WARNING![/bold yellow]", style="yellow")
                        self.console.print("No valid file found", justify="center")

                elif command.startswith("/link"):
                    command_args = user_input.split()[1:]
                    if len(command_args) != 1:
                        self.console.print("\n")
                        self.console.rule("⚠️  [bold yellow]WARNING![/bold yellow]", style="yellow")
                        self.console.print(
                            "Too few or missing arguments! Command: [i yellow]/link https://pieroit.github.io/cheshire-cat/[/i yellow]",
                            justify="center",
                        )
                    else:
                        link = command_args[0]
                        if not link.startswith(("http://", "https://")):
                            self.console.print("\n")
                            self.console.rule("⚠️  [bold yellow]WARNING![/bold yellow]", style="yellow")
                            self.console.print(
                                "Invalid link format: must start with 'http://' or 'https://'", justify="center"
                            )
                        else:
                            try:
                                parsed_link = requests.get(link).url
                                data = {"url": parsed_link, "chunk_size": 400, "chunk_overlap": 100}
                                headers = {"Content-Type": "application/json", "Accept": "application/json"}
                                response = requests.post(
                                    "http://localhost:1865/rabbithole/web/", headers=headers, json=data
                                )
                                self.console.print(response.json()["info"])
                            except requests.exceptions.RequestException:
                                self.console.print("\n")
                                self.console.rule("⚠️  [bold red]WARNING![/bold red]", style="yellow")
                                self.console.print("Error: Failed to parse link", justify="center")
                else:
                    # User entered a non-/ command, break out of the loop and send the message
                    break
            else:
                # User entered a message, break out of the loop and send the message
                break

        # Send the user input as a message to the cat
        self.spinner.start()
        self.ws.send(json.dumps({"text": user_input}))

        # Wait for the cat's response
        self.waiting_for_input = True

        def stop(self):
            self.waiting_for_input = False
