from __future__ import annotations

import platform
import os

from dataclasses import dataclass
from pathlib import Path

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

from modules.documentation.mapper import DocumentMapper


# ============================================================
# APPLICATION
# ============================================================

APP_NAME = "WS.System"
APP_VERSION = "0.1"
APP_DESCRIPTION = "Enterprise Network & Cybersecurity Framework"

console = Console()


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ASCII_FILE = (
    BASE_DIR
    / "assets"
    / "ASCII.txt"
)


# ============================================================
# ASCII LOGO
# ============================================================

def load_ascii_logo():

    try:

        return ASCII_FILE.read_text(
            encoding="utf-8"
        ).rstrip("\r\n")

    except FileNotFoundError:

        return "WS.SYSTEM"


ASCII_LOGO = load_ascii_logo()


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
    ),

    Module(
        "Windows",
        "Ferramentas para análise e administração de sistemas Windows.",
        1
    )
]


# ============================================================
# WINDOWS TOOLS
# ============================================================

WINDOWS_TOOLS = [

    Module(
        "Folder Mapper",
        "Mapeia recursivamente uma pasta e identifica sua estrutura e extensões.",
        1
    )
]


# ============================================================
# APPLICATION STATE
# ============================================================

class ApplicationState:

    def __init__(self):

        self.selected_index = 0
        self.windows_selected_index = 0

        self.view = "main"

        self.message = ""

    # --------------------------------------------------------
    # CURRENT MODULE
    # --------------------------------------------------------

    @property
    def selected_module(self):

        if self.view == "windows":

            return WINDOWS_TOOLS[
                self.windows_selected_index
            ]

        return MODULES[
            self.selected_index
        ]

    # --------------------------------------------------------
    # MAIN MENU
    # --------------------------------------------------------

    def next_module(self):

        if self.view == "windows":

            self.windows_selected_index = (
                self.windows_selected_index + 1
            ) % len(WINDOWS_TOOLS)

            return

        self.selected_index = (
            self.selected_index + 1
        ) % len(MODULES)

    def previous_module(self):

        if self.view == "windows":

            self.windows_selected_index = (
                self.windows_selected_index - 1
            ) % len(WINDOWS_TOOLS)

            return

        self.selected_index = (
            self.selected_index - 1
        ) % len(MODULES)

    # --------------------------------------------------------
    # WINDOWS MENU
    # --------------------------------------------------------

    def open_windows(self):

        self.view = "windows"
        self.windows_selected_index = 0
        self.message = ""

    def close_windows(self):

        self.view = "main"
        self.message = ""

    # --------------------------------------------------------
    # MESSAGE
    # --------------------------------------------------------

    def set_message(self, message):

        self.message = message


state = ApplicationState()


# ============================================================
# SYSTEM INFORMATION
# ============================================================

def get_system_information():

    return {

        "os": (
            f"{platform.system()} "
            f"{platform.release()}"
        ),

        "python": platform.python_version(),

        "architecture": platform.machine()
    }


# ============================================================
# HEADER
# ============================================================

def create_header():

    logo = Text(
        ASCII_LOGO,
        style="bold cyan",
        no_wrap=True,
        overflow="crop"
    )

    information = Text(
        no_wrap=True
    )

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
        ratio=4,
        justify="left",
        vertical="middle",
        no_wrap=True
    )

    header_content.add_column(
        ratio=1,
        justify="left",
        vertical="middle",
        no_wrap=True
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

    if state.view == "main":

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

        title = "[bold cyan]MODULES[/]"

    else:

        content.append(
            "  ← Windows\n\n",
            style="bold cyan"
        )

        for index, module in enumerate(WINDOWS_TOOLS):

            if index == state.windows_selected_index:

                content.append(
                    f"  ► {module.name}\n",
                    style="bold black on cyan"
                )

            else:

                content.append(
                    f"    {module.name}\n",
                    style="white"
                )

        title = "[bold cyan]WINDOWS[/]"

    return Panel(
        content,
        title=title,
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

    os.system("cls" if os.name == "nt" else "clear")

    console.print(
        create_interface()
    )


# ============================================================
# DOCUMENT MAPPER
# ============================================================

def run_document_mapper():

    console.clear()

    console.print(
        Panel.fit(
            "[bold cyan]WS.SYSTEM[/]\n"
            "[white]WINDOWS / FOLDER MAPPER[/]",
            border_style="cyan"
        )
    )

    console.print()

    console.print(
        "[dim]Informe o caminho completo da pasta que deseja mapear.[/]"
    )

    console.print()

    path_input = input(
        "Caminho: "
    ).strip()

    if not path_input:

        state.set_message(
            "Nenhum caminho informado."
        )

        return

    try:

        mapper = DocumentMapper(
            path_input
        )

        console.print()

        console.print(
            f"[cyan]Pasta selecionada:[/cyan]\n"
            f"{mapper.root}"
        )

        console.print()

        confirmation = input(
            "Deseja iniciar o mapeamento? [S/N]: "
        ).strip().lower()

        if confirmation != "s":

            state.set_message(
                "Mapeamento cancelado."
            )

            return

        console.print()

        console.print(
            "[yellow][*] Analisando estrutura...[/yellow]"
        )

        output = (
            Path.home()
            / "Desktop"
            / "mapeamento.txt"
        )

        mapper.save(output)

        stats = mapper.statistics()

        console.print()

        console.print(
            "[bold green][OK] Mapeamento concluído![/bold green]"
        )

        console.print()

        console.print(
            f"[cyan]Pasta:[/cyan] {mapper.root}"
        )

        console.print(
            f"[cyan]Pastas:[/cyan] {stats['directories']}"
        )

        console.print(
            f"[cyan]Arquivos:[/cyan] {stats['files']}"
        )

        console.print(
            f"[cyan]Relatório:[/cyan] {output}"
        )

        state.set_message(
            f"Mapeamento concluído: "
            f"{stats['files']} arquivos."
        )

    except Exception as error:

        state.set_message(
            f"Erro no mapeamento: {error}"
        )

        console.print()

        console.print(
            f"[bold red][ERRO][/bold red] {error}"
        )

    console.print()

    input(
        "Pressione ENTER para voltar..."
    )


# ============================================================
# ACTIONS
# ============================================================

def open_module():

    if state.view == "main":

        module = state.selected_module

        if module.name == "Windows":

            state.open_windows()

        else:

            state.set_message(
                f"Módulo '{module.name}' selecionado."
            )

        return

    if state.view == "windows":

        tool = state.selected_module

        if tool.name == "Folder Mapper":

            run_document_mapper()

        else:

            state.set_message(
                f"Ferramenta '{tool.name}' selecionada."
            )


# ============================================================
# HELP
# ============================================================

def show_help():

    if state.view == "main":

        state.set_message(
            "↑↓ navegar | ENTER abrir módulo | Q sair"
        )

    else:

        state.set_message(
            "↑↓ navegar | ENTER executar | ESC voltar"
        )


# ============================================================
# BACK
# ============================================================

def go_back():

    if state.view == "windows":

        state.close_windows()

    else:

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

    event.app.exit(
        result="open"
    )


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

    while True:

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

        result = application.run()

        if result == "open":

            open_module()

            continue

        break


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