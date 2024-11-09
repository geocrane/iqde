import ipywidgets as widgets

from iqde.constructor.visual import accordion as constructor_accordion
from iqde.archives.visual import accordion as archives_accordion

from IPython.display import HTML, display
from iqde.styles import css

# from iqde.data.provided.wgets import sql_redactor as provided_sql
# from iqde.data.custom.wgets import sql_redactor as custom_sql


# custom_switcher
custom_switcher = widgets.Tab(
    children=[constructor_accordion, archives_accordion],
    layout={"width": "1500px"},
)
custom_switcher.set_title(0, "constructor")
custom_switcher.set_title(1, "archives")
custom_switcher.add_class("switcher")


def run(wgt=custom_switcher):
    display(wgt, HTML(css))


# def iquery():
#     if custom_switcher.selected_index == 0:
#         return provided_sql.value
#     if custom_switcher.selected_index == 1:
#         return custom_sql.value
#     else:
#         return None


# def copypast():
#     if custom_switcher.selected_index == 0:
#         print(f'query = f"""{provided_sql.value}"""')
#     if custom_switcher.selected_index == 1:
#         print(f'query = f"""{custom_sql.value}"""')
#     else:
#         return None
