from rich.markdown import Markdown
from rich.console import Console
import sys
from IPython.display import Markdown as IPMarkdown, display, update_display

console = Console()

def is_jupyter():
    """Detect if the script is running in a Jupyter Notebook."""
    return "ipykernel" in sys.modules

def print_markdown_response(response):
    """Prints AI response as Markdown using Rich in terminal or Jupyter Notebook."""
    if is_jupyter():
        display(IPMarkdown(response))
    else:
        console.print(Markdown(response))
