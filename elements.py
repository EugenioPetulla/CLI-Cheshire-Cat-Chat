from rich.console import Console

def greetings():
    output = "\n[bold green]🍃 😺 The Cheshire Cat has spawned!!! 😺 🍃 [/bold green]\n\n"
    output += "*****************************************\n"
    output += "| [i]Would you tell me, please,            |\n"
    output += "| which way I ought to go from here?[/i]    |\n"
    output += "*****************************************\n"
    output += "| [i]The Cheshire Cat: That depends a      |\n"
    output += "| good deal on where you want to get to.[/i]|\n"
    output += "*****************************************\n"
    output += "\n:robot: [bold yellow]Type[/bold yellow] [i]/help[/i] [yellow]to receive the list of available commands[/yellow]\n"

    return output

def goodbye():
    output = "\n[bold red]🍃 😺 The Cheshire Cat walks away!!! 😺 🍃 [/bold red]\n\n"
    output += "*****************************************\n"
    output += "| [i]Farewell, dear wanderer.              |\n"
    output += "| Remember to keep your curiosity and   |\n"
    output += "| inquisitive spirit alive, and perhaps |\n"
    output += "| one day you too will find your way    |\n"
    output += "|                 back to Wonderland.[/i]   |\n"
    output += "*****************************************\n"

    return output


def error(error):
    return "[red bold]Error: " + str(error) + "[/red bold]"

def help():
    output = "- /help: Show this help message\n"
    output += "- /exit: Exit the chat\n"
    output += "- /send [i yellow]/path/to-your/file.txt[/i yellow]: Make the cat ingest a .txt, .md or .pdf file\n"
    output += "- /link [i yellow]https://pieroit.github.io/cheshire-cat/[/i yellow] : Make the cat ingest a website page"

    return output