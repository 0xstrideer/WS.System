from __future__ import annotations

import platform

from dataclasses import dataclass

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout as PTLayout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl

from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


# ============================================================
# APPLICATION
# ============================================================

APP_NAME = "WS.System"
APP_VERSION = "0.1"
APP_DESCRIPTION = "Enterprise Network & Cybersecurity Framework"

console = Console()


# ============================================================
# MODULES
# ============================================================

@dataclass
class Module:
    name: str
    description: str
    tools: int
    status: str = "Ready"


MODULES = [
    Module(
        "Network",
        "Ferramentas de análise e diagnóstico de rede.",
        6
    ),
    Module(
        "Wireless",
        "Ferramentas para análise de redes sem fio.",
        4
    ),
    Module(
        "Web",
        "Ferramentas de análise e segurança web.",
        8
    ),
    Module(
        "OSINT",
        "Ferramentas para coleta de informações públicas.",
        5
    ),
    Module(
        "Payload",
        "Gerenciamento e análise de payloads.",
        3
    ),
    Module(
        "Report",
        "Geração e gerenciamento de relatórios.",
        2
    )
]


# ============================================================
# APPLICATION STATE
# ============================================================

class ApplicationState:

    def __init__(self):
        self.selected_index = 0
        self.message = ""

    @property
    def selected_module(self):
        return MODULES[self.selected_index]

    def next_module(self):
        self.selected_index = (
            self.selected_index + 1
        ) % len(MODULES)

    def previous_module(self):
        self.selected_index = (
            self.selected_index - 1
        ) % len(MODULES)

    def set_message(self, message):
        self.message = message


state = ApplicationState()


# ============================================================
# SYSTEM INFORMATION
# ============================================================

def get_system_information():

    return {
        "os": f"{platform.system()} {platform.release()}",
        "python": platform.python_version(),
        "architecture": platform.machine()
    }


# ============================================================
# HEADER
# ============================================================

def create_header():

    logo = Text()

    logo.append(
        "██╗    ██╗███████╗   ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗\n"
        "██║    ██║██╔════╝   ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║\n"
        "██║ █╗ ██║███████╗   ███████╗ ╚████╔╝ █████╗     ██║   █████╗  ██╔████╔██║\n"
        "██║███╗██║╚════██║   ╚════██║  ╚██╔╝  ██╔══╝     ██║   ██╔══╝  ██║╚██╔╝██║\n"
        "╚███╔███╔╝███████║   ███████║   ██║   ███████╗   ██║   ███████╗██║ ╚═╝ ██║\n"
        " ╚══╝╚══╝ ╚══════╝   ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝",
        style="bold cyan"
    )

    information = Text()

    information.append(
        f"{APP_NAME}\n",
        style="bold white"
    )

    information.append(
        f"Version {APP_VERSION}\n\n",
        style="bold cyan"
    )

    information.append(
        APP_DESCRIPTION,
        style="white"
    )

    header_content = Table(
        show_header=False,
        box=None,
        expand=True,
        padding=(0, 2)
    )

    header_content.add_column(
        ratio=3,
        justify="left",
        vertical="middle"
    )

    header_content.add_column(
        ratio=2,
        justify="left",
        vertical="middle"
    )

    header_content.add_row(
        logo,
        information
    )

    return Panel(
        header_content,
        border_style="cyan",
        padding=(1, 1)
    )


# ============================================================
# MODULE MENU
# ============================================================

def create_module_menu():

    content = Text()

    for index, module in enumerate(MODULES):

        if index == state.selected_index:

            content.append(
                f"  ► {module.name}\n",
                style="bold black on cyan"
            )

        else:

            content.append(
                f"    {module.name}\n",
                style="white"
            )

    return Panel(
        content,
        title="[bold cyan]MODULES[/]",
        title_align="left",
        border_style="cyan",
        padding=(1, 1)
    )


# ============================================================
# DASHBOARD
# ============================================================

def create_dashboard():

    module = state.selected_module
    system = get_system_information()

    table = Table(
        show_header=False,
        box=None,
        expand=True,
        padding=(0, 1)
    )

    table.add_column(
        style="bold cyan",
        width=24
    )

    table.add_column(
        style="white"
    )

    table.add_row(
        "Nome:",
        module.name
    )

    table.add_row(
        "Status:",
        "[bold green]● Ready[/]"
    )

    table.add_row(
        "",
        ""
    )

    table.add_row(
        "Descrição:",
        module.description
    )

    table.add_row(
        "",
        ""
    )

    table.add_row(
        "Sistema Operacional:",
        system["os"]
    )

    table.add_row(
        "Arquitetura:",
        system["architecture"]
    )

    table.add_row(
        "Python:",
        system["python"]
    )

    table.add_row(
        "Ferramentas:",
        str(module.tools)
    )

    table.add_row(
        "Módulos Carregados:",
        str(len(MODULES))
    )

    if state.message:

        table.add_row(
            "",
            ""
        )

        table.add_row(
            "Mensagem:",
            f"[yellow]{state.message}[/]"
        )

    return Panel(
        table,
        title="[bold cyan]Dashboard[/]",
        title_align="left",
        border_style="cyan",
        padding=(1, 1)
    )


# ============================================================
# FOOTER
# ============================================================

def create_footer():

    footer = Text()

    footer.append(
        " ↑↓ ",
        style="bold black on cyan"
    )

    footer.append(
        " Navegar   "
    )

    footer.append(
        " ENTER ",
        style="bold black on cyan"
    )

    footer.append(
        " Abrir   "
    )

    footer.append(
        " ESC ",
        style="bold black on cyan"
    )

    footer.append(
        " Voltar   "
    )

    footer.append(
        " F1 ",
        style="bold black on cyan"
    )

    footer.append(
        " Ajuda   "
    )

    footer.append(
        " Q ",
        style="bold black on cyan"
    )

    footer.append(
        " Sair"
    )

    return Panel(
        Align.center(footer),
        border_style="cyan"
    )


# ============================================================
# INTERFACE
# ============================================================

def create_interface():

    layout = Layout()

    layout.split_column(

        Layout(
            create_header(),
            name="header",
            size=10
        ),

        Layout(
            name="body"
        ),

        Layout(
            create_footer(),
            name="footer",
            size=3
        )
    )

    layout["body"].split_row(

        Layout(
            create_module_menu(),
            name="modules",
            ratio=1
        ),

        Layout(
            create_dashboard(),
            name="dashboard",
            ratio=3
        )
    )

    return layout


# ============================================================
# RENDER
# ============================================================

def render():

    console.clear()

    console.print(
        create_interface()
    )


# ============================================================
# ACTIONS
# ============================================================

def open_module():

    module = state.selected_module

    state.set_message(
        f"Módulo '{module.name}' selecionado."
    )


def show_help():

    state.set_message(
        "↑↓ navegar | ENTER abrir | ESC voltar | Q sair"
    )


def go_back():

    state.set_message(
        "Você já está no menu principal."
    )


# ============================================================
# KEYBOARD
# ============================================================

kb = KeyBindings()


@kb.add("down")
def handle_down(event):

    state.next_module()
    state.set_message("")

    render()

    event.app.invalidate()


@kb.add("up")
def handle_up(event):

    state.previous_module()
    state.set_message("")

    render()

    event.app.invalidate()


@kb.add("enter")
def handle_enter(event):

    open_module()

    render()

    event.app.invalidate()


@kb.add("escape")
def handle_escape(event):

    go_back()

    render()

    event.app.invalidate()


@kb.add("f1")
def handle_f1(event):

    show_help()

    render()

    event.app.invalidate()


@kb.add("q")
def handle_quit(event):

    event.app.exit()


@kb.add("c-c")
def handle_ctrl_c(event):

    event.app.exit()


# ============================================================
# RUN DASHBOARD
# ============================================================

def run_dashboard():

    render()

    application = Application(
        layout=PTLayout(
            Window(
                FormattedTextControl("")
            )
        ),
        key_bindings=kb,
        full_screen=False,
        mouse_support=False
    )

    application.run()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:

        run_dashboard()

    except KeyboardInterrupt:

        pass

    finally:

        console.clear()

        console.print(
            Panel(
                Align.center(
                    Text(
                        f"{APP_NAME} encerrado.",
                        style="bold cyan"
                    )
                ),
                border_style="cyan"
            )
        )