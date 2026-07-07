from pyfiglet import Figlet
from rich.console import Console

console = Console()

def show_banner():
    banner = Figlet(font="slant")
    console.print(f"[bold cyan]{banner.renderText('WS.System')}[/]")
    console.print("[bold white]Enterprise Network & Cybersecurity Framework[/]\n")