import time

from rich.console import Console
from rich.progress import Progress


def input_with_prefill(prompt="", prefill=""):
    return input(f"Line 3: {prompt}").strip()


console = Console()

# Print two lines of info. This is important info for the user.
console.print("Line 1: Print some important info.")
console.print("Line 2: Print some more important info.")

with Progress(console=console, transient=True) as progress:
    # Do some work and analysize stuff...
    task_a = progress.add_task("Analyzing your fridge...")
    task_b = progress.add_task("Analyzing bottom fridge drawer...")
    task_c = progress.add_task("Analyzing left corner of drawer...")  # <-- [1] Try out-commenting.
    time.sleep(0.5)

    # We want to ask the user something, so hide the progress bars.
    progress.stop()

    # Ask the user.
    favorite_food = input_with_prefill(prompt="Favorite Food? ", prefill="Pizza")

    #progress.print()  # <-- [2] Try remove comment.
    #progress.print()  # <-- [2] Try remove comment.

    # Now that we have the answer we can show the progress bars again and keep processing
    progress.start()
    time.sleep(0.5)

    # Print the result of the analysis.
    progress.print(f"Line 4: Favorite food is {favorite_food}.")