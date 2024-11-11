import warnings

import ipywidgets as widgets

import iqde.layouts as layout

warnings.filterwarnings("ignore")


text = widgets.Label("replics:")
text2 = widgets.Label("tables:")
text3 = widgets.Label(value="attributes:", layout=layout.text)
text4 = widgets.Label(value="subscription")
text5 = widgets.Label(value="select FROM:")
text6 = widgets.Label(value="SQL name:")
text7 = widgets.Label(value="load archived:")

replics = widgets.Dropdown(layout=layout.select_replic)
tables = widgets.SelectMultiple(layout=layout.select_tables)
attrs = widgets.SelectMultiple(layout=layout.select_attrs)

get_joins_btn = widgets.Button(layout=layout.btn, description="joins")
joins_info = widgets.Output(layout=layout.joins_info, description="joins_info")
joins_type = widgets.ToggleButtons(
    layout=layout.joins_type, options=["left", "inner", "right"]
)
select_from = widgets.Dropdown(layout=layout.select_from)

subscribe = widgets.Text(layout=layout.subscribe_name)
add_subscribe_btn = widgets.Button(layout=layout.btn, description="save substription")

construct_sql_btn = widgets.Button(layout=layout.btn, description="GET SQL")
sql_redactor = widgets.Textarea(layout=layout.sql_redactor)

input_script_name = widgets.Text(
    layout=layout.input_script_name, placeholder="input_script_name"
)
save_script_btn = widgets.Button(layout=layout.btn, description="save_script_btn")

logo = widgets.Label("Integrated query design environment (IQDE)")
file = open("iqde/data/logo.png", "rb")
image = file.read()
logo_img = widgets.Image(
    value=image,
    format="png",
    width=70,
    height=70,
)
