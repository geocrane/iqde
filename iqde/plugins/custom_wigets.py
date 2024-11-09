import ipywidgets as widgets
from IPython.display import clear_output
from traitlets import link, Unicode, Bool, Any


class ConfirmationButton(widgets.HBox):
    button_style = Any(default_value="")
    description = Unicode()
    disabled = Bool()
    icon = Unicode()
    layout = Any()
    style = Any()
    tooltip = Unicode()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._button = widgets.Button(**kwargs)
        self._confirm_btn = widgets.Button(
            description="confirm",
            icon="check",
            button_style="success",
            layout=dict(width="auto"),
        )
        self._cancel_btn = widgets.Button(
            description="cancel",
            icon="times",
            button_style="warning",
            layout=dict(width="auto"),
        )
        self._button.on_click(self._on_btn_click)
        self._cancel_btn.on_click(self._on_btn_click)
        self._confirm_btn.on_click(self._on_btn_click)
        self.children = [self._button]

        self.output = None
        self.allert_msg = None

        for key in self._button.keys:
            if key[0] != "_":
                link((self._button, key), (self, key))

    def set_allert_msg(self, msg):
        self.allert_msg = msg

    def set_output(self, output):
        self.output = output

    def on_click(self, *args, **kwargs):
        self._confirm_btn.on_click(*args, **kwargs)

    def _on_btn_click(self, b):
        if self.allert_msg:
            if b == self._button:
                with self.output:
                    clear_output()
                    print(self.allert_msg)
                self.children = [self._confirm_btn, self._cancel_btn]
            else:
                self.children = [self._button]
        else:
            self.children = [self._button]
