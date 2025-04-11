import asyncio
import pyvisa
from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Tree, Header, Footer


class PyVisaScanApp(App):
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit"),
        Binding(key="r", action="refresh", description="Refresh"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        self.instruments_tree: Tree[str] = Tree("Instruments")
        yield self.instruments_tree
        yield Footer()

    def on_mount(self) -> None:
        self.title = "PyVISA instruments scanner"
        self.action_refresh()

    def action_refresh(self) -> None:
        self.instruments_tree.loading = True
        self.work_refresh(self.instruments_tree)

    @work
    async def work_refresh(self, instruments_tree: Tree) -> None:
        instruments_tree.clear()
        instruments_tree.root.expand()
        resource_manager = pyvisa.ResourceManager("@py")
        instruments_tree.root.label = str(resource_manager)
        for resource in await asyncio.to_thread(resource_manager.list_resources):
            node = instruments_tree.root.add(str(resource))
            try:
                node.add_leaf("IDN: " + await asyncio.to_thread(self.get_instrument_idn, resource_manager, resource))
                node.expand()
            except Exception as e:
                node.add_leaf("Error: " + str(e))
        instruments_tree.loading = False

    def get_instrument_idn(self, resource_manager, resource):
        instrument = resource_manager.open_resource(resource)
        return instrument.query("*IDN?")


def main():
    app = PyVisaScanApp()
    app.run()
