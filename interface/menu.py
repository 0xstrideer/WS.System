from rich.console import Console
from rich.panel import Panel
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl

console = Console()

options = [
    "Opção 1",
    "Opção 2",
    "Opção 3"
]

selected = 0


def draw_menu():

    body = []

    for i, option in enumerate(options):

        if i == selected:
            body.append(("class:selected", f"➜ {option}\n"))
        else:
            body.append(("class:normal", f"  {option}\n"))

    return body


kb = KeyBindings()


@kb.add("up")
def _(event):
    global selected
    selected = (selected - 1) % len(options)
    event.app.invalidate()


@kb.add("down")
def _(event):
    global selected
    selected = (selected + 1) % len(options)
    event.app.invalidate()


@kb.add("enter")
def _(event):
    event.app.exit(result=selected)


root = HSplit([
    Window(
        FormattedTextControl(draw_menu),
        always_hide_cursor=True
    )
])

application = Application(
    layout=Layout(root),
    key_bindings=kb,
    full_screen=False
)


def menu():

    console.print(
        Panel.fit(
            "[bold cyan]Main Menu[/]",
            border_style="cyan"
        )
    )

    result = application.run()

    return result