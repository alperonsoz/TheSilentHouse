from rich.console import Console
from rich.style import Style
import time

# printing

console = Console()

# styles
titleStyle = Style(color="red", bold=True)
descStyle = Style(color="cyan")
actionStyle = Style(color="green")
warningStyle = Style(color="yellow")
errorStyle = Style(color="magenta")
dialogueStyle = Style(color="blue", italic=True)

# slow print
def slow_print(message, delay=0.02, style=None):
    for char in message:
        console.print(char, end="", style=style)
        time.sleep(delay)
    console.print("")

def print_title(message):
    console.print("")
    console.print("=" * 50, style=titleStyle)
    console.print(message, style=titleStyle)
    console.print("=" * 50, style=titleStyle)
    console.print("")

def print_desc(message):
    slow_print(message, delay=0.015, style=descStyle)

def print_action(message):
    slow_print(message, delay=0.02, style=actionStyle)

def print_warning(message):
    console.print(message, style=warningStyle)

def print_error(message):
    console.print(message, style=errorStyle)

def print_dialogue(message):
    slow_print(message, delay=0.02, style=dialogueStyle)

# help
def print_help():
    console.print("")
    console.print("--- COMMANDS ---", style=titleStyle)
    console.print("look         - look around", style=actionStyle)
    console.print("go [place]   - move somewhere", style=actionStyle)
    console.print("go back      - return to previous spot", style=actionStyle)
    console.print("take [item]  - pick up something", style=actionStyle)
    console.print("open [item]  - open something", style=actionStyle)
    console.print("read [item]  - read something", style=actionStyle)
    console.print("use [item]   - interact with something", style=actionStyle)
    console.print("inv          - check your items", style=actionStyle)
    console.print("save         - save game", style=actionStyle)
    console.print("quit         - exit", style=actionStyle)
    console.print("----------------", style=titleStyle)
    console.print("TIP: Keep commands short (max 3 words)", style=warningStyle)
    console.print("TIP: You can type item names directly", style=warningStyle)
    console.print("")
