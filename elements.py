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
    output += "- /exit: Exit the chat"

    return output