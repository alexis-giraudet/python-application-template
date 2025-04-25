import asyncio
import pyvisa
from rich.panel import Panel
from rich.table import Table
from textual import work
from textual.app import App, ComposeResult
from textual.suggester import SuggestFromList
from textual.widgets import (
    Header,
    Footer,
    Button,
    Label,
    Input,
    RichLog,
)


class PyVisaApp(App):

    CSS = """
    Screen {
        layout: grid;
        grid-size: 5 3;
        grid-columns: auto 1fr auto auto auto;
        grid-rows: auto 1fr auto;
    }

    Label {
        width: 100%;
        padding: 1;
        text-align: center;
    }

    #pyvisa_log {
        column-span: 5;
    }

    #query_message_input {
        column-span: 3;
    }
    """

    pyvisa_resource_manager = pyvisa.ResourceManager("@py")
    pyvisa_resource = None

    def compose(self) -> ComposeResult:
        self.list_resources_info_button = Button(
            "List", id="list_resources_info_button"
        )
        self.resource_name_label = Label("Resource", id="resource_name_label")
        self.resource_name_input = Input(
            placeholder="E.g. TCPIP0::1.2.3.4::999::SOCKET",
            suggester=None,
            id="resource_name_input",
        )
        self.resource_open_button = Button.success("Open", id="resource_open_button")
        self.resource_close_button = Button.error("Close", id="resource_close_button")
        self.pyvisa_log = RichLog(id="pyvisa_log")
        self.query_message_label = Label("Query", id="query_message_label")
        self.query_message_input = Input(
            placeholder="E.g. *IDN?", id="query_message_input"
        )
        self.query_send_button = Button(
            "Send", variant="primary", id="query_send_button"
        )

        self.update_resource_widgets()

        yield Header()
        yield self.resource_name_label
        yield self.resource_name_input
        yield self.resource_open_button
        yield self.resource_close_button
        yield self.list_resources_info_button
        yield self.pyvisa_log
        yield self.query_message_label
        yield self.query_message_input
        yield self.query_send_button
        yield Footer()

    def on_mount(self) -> None:
        self.title = "PyVISA App"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "list_resources_info_button":
            self.action_list_resources_info()
        elif button_id == "resource_open_button":
            self.action_resource_open()
        elif button_id == "query_send_button":
            self.action_query_send()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        input_id = event.input.id
        if input_id == "resource_name_input":
            self.action_resource_open()
        elif input_id == "query_message_input":
            self.action_query_send()

    def update_resource_widgets(self, disable_all: bool = False) -> None:
        self.resource_name_input.disabled = (
            disable_all or self.pyvisa_resource is not None
        )
        self.resource_open_button.disabled = (
            disable_all or self.pyvisa_resource is not None
        )
        self.resource_close_button.disabled = (
            disable_all or self.pyvisa_resource is None
        )
        self.query_message_input.disabled = disable_all or self.pyvisa_resource is None
        self.query_send_button.disabled = disable_all or self.pyvisa_resource is None
        self.list_resources_info_button.disabled = disable_all

    def action_list_resources_info(self) -> None:
        self.update_resource_widgets(True)
        self.list_resources_info_button.loading = True
        self.work_list_resources_info()

    @work
    async def work_list_resources_info(self) -> None:
        panel_kwargs = {
            "title": "List Resources Info",
            "title_align": "left",
        }
        try:
            resource_table = Table(title=str(self.pyvisa_resource_manager))
            resource_table.add_column("Name")
            resource_table.add_column("Alias")
            resource_table.add_column("Type")
            resource_table.add_column("Class")
            resource_table.add_column("Board Number")

            list_resources_info = await asyncio.to_thread(
                self.pyvisa_resource_manager.list_resources_info
            )
            self.resource_name_input.suggester = SuggestFromList(
                list(list_resources_info), case_sensitive=False
            )
            for resource_info in list_resources_info.values():
                resource_table.add_row(
                    str(resource_info.resource_name),
                    str(resource_info.alias),
                    str(resource_info.interface_type),
                    str(resource_info.resource_class),
                    str(resource_info.interface_board_number),
                )

            self.pyvisa_log.write(
                Panel(
                    resource_table,
                    **panel_kwargs,
                    border_style="green",
                )
            )
        except Exception as e:
            self.pyvisa_log.write(
                Panel(
                    str(e),
                    **panel_kwargs,
                    border_style="red",
                )
            )
        self.list_resources_info_button.loading = False
        self.update_resource_widgets()

    def action_resource_open(self) -> None:
        self.update_resource_widgets(True)
        self.resource_open_button.loading = True
        self.work_resource_open()

    @work
    async def work_resource_open(self) -> None:
        resource_name = self.resource_name_input.value
        panel_kwargs = {
            "title": f'Open Resource "{resource_name}"',
            "title_align": "left",
        }
        try:
            self.pyvisa_resource = await asyncio.to_thread(
                self.pyvisa_resource_manager.open_resource, resource_name
            )
            Panel(
                str(resource_name),
                **panel_kwargs,
                border_style="green",
            )
        except Exception as e:
            self.pyvisa_log.write(
                Panel(
                    str(e),
                    **panel_kwargs,
                    border_style="red",
                )
            )
        self.resource_open_button.loading = False
        self.update_resource_widgets()

    def action_resource_close(self) -> None:
        self.update_resource_widgets(True)
        self.resource_close_button.loading = True
        self.work_resource_close()

    @work
    async def work_resource_close(self) -> None:
        panel_kwargs = {
            "title": f'Close Resource "{self.pyvisa_resource.resource_name}"',
            "title_align": "left",
        }
        try:
            await asyncio.to_thread(self.pyvisa_resource.close)
            Panel(
                "",
                **panel_kwargs,
                border_style="green",
            )
        except Exception as e:
            self.pyvisa_log.write(
                Panel(
                    str(e),
                    **panel_kwargs,
                    border_style="red",
                )
            )
        self.resource_close_button.loading = False
        self.update_resource_widgets()

    def action_query_send(self) -> None:
        self.update_resource_widgets(True)
        self.query_send_button.loading = True
        self.work_resource_close()

    @work
    async def work_query_send(self) -> None:
        query_message = self.query_message_input.value
        panel_kwargs = {
            "title": f'Send Query "{query_message}"',
            "title_align": "left",
        }
        try:
            Panel(
                await asyncio.to_thread(self.pyvisa_resource.query, query_message),
                **panel_kwargs,
                border_style="green",
            )
        except Exception as e:
            self.pyvisa_log.write(
                Panel(
                    str(e),
                    **panel_kwargs,
                    border_style="red",
                )
            )
        self.query_send_button.loading = False
        self.update_resource_widgets()


def main():
    PyVisaApp().run()
