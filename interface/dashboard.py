from rich.console import Console, Group
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from rich.table import Table
from prompt_toolkit import Application
from prompt_toolkit.layout import Layout as PTLayout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings


console = Console()


modules = [
    {
        "name": "Network",
        "description": "Ferramentas de análise e diagnóstico de rede.",
        "tools": 6
    },
    {
        "name": "Wireless",
        "description": "Análise de redes sem fio.",
        "tools": 4
    },
    {
        "name": "Web",
        "description": "Ferramentas de segurança web.",
        "tools": 8
    },
    {
        "name": "OSINT",
        "description": "Coleta de informações públicas.",
        "tools": 5
    },
    {
        "name": "Payload",
        "description": "Gerenciamento de payloads.",
        "tools": 3
    },
    {
        "name": "Report",
        "description": "Geração de relatórios.",
        "tools": 2
    }
]


selected = 0


def create_interface():


    layout = Layout()


    layout.split_column(

        Layout(name="header", size=5),

        Layout(name="body"),

        Layout(name="footer", size=3)

    )


    layout["body"].split_row(

        Layout(name="modules", ratio=1),

        Layout(name="dashboard", ratio=3)

    )


    return layout



def header():


    text = Text()


    text.append(
        "██╗    ██╗███████╗   ",
        style="cyan"
    )

    text.append(
        "WS.System v0.1\n",
        style="bold white"
    )


    text.append(
        "██║    ██║██╔════╝   ",
        style="cyan"
    )

    text.append(
        "Enterprise Network & Cybersecurity Framework",
        style="white"
    )


    return Panel(
        Align.center(text),
        border_style="cyan"
    )




def module_panel():


    content = ""


    for index, module in enumerate(modules):

        if index == selected:

            content += (
                f"[bold cyan]► {module['name']}[/]\n"
            )

        else:

            content += (
                f"  {module['name']}\n"
            )


    return Panel(
        content,
        title="MODULES",
        border_style="cyan"
    )




def dashboard_panel():


    module = modules[selected]


    table = Table(
        show_header=False,
        box=None
    )


    table.add_row(
        "Nome:",
        module["name"]
    )

    table.add_row(
        "Status:",
        "[green]Ready[/]"
    )


    table.add_row(
        "",
        ""
    )


    table.add_row(
        "Descrição:",
        module["description"]
    )


    table.add_row(
        "",
        ""
    )


    table.add_row(
        "Sistema Operacional:",
        "Windows / Linux"
    )


    table.add_row(
        "Python:",
        "3.13"
    )


    table.add_row(
        "Módulos Carregados:",
        str(module["tools"])
    )


    return Panel(
        table,
        title="Dashboard",
        border_style="cyan"
    )




def footer():


    return Panel(
        "[cyan]↑↓[/] Navegar | "
        "[cyan]ENTER[/] Abrir | "
        "[cyan]ESC[/] Voltar | "
        "[cyan]F1[/] Ajuda | "
        "[cyan]Q[/] Sair",
        border_style="cyan"
    )





def render():


    interface = create_interface()


    interface["header"].update(
        header()
    )


    interface["modules"].update(
        module_panel()
    )


    interface["dashboard"].update(
        dashboard_panel()
    )


    interface["footer"].update(
        footer()
    )


    console.clear()

    console.print(interface)





kb = KeyBindings()



@kb.add("down")
def down(event):

    global selected

    selected += 1


    if selected >= len(modules):

        selected = 0


    render()




@kb.add("up")
def up(event):

    global selected

    selected -= 1


    if selected < 0:

        selected = len(modules)-1


    render()




@kb.add("q")
def quit(event):

    event.app.exit()




@kb.add("enter")
def enter(event):

    module = modules[selected]["name"]

    console.print(
        f"\nAbrindo módulo: {module}"
    )




def run_dashboard():


    render()


    app = Application(

        layout=PTLayout(
            Window(
                FormattedTextControl(
                    ""
                )
            )
        ),

        key_bindings=kb,

        full_screen=True

    )


    app.run()