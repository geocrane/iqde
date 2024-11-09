import warnings

import ipywidgets as widgets

import iqde.constructor.layouts as layout
from iqde.models import Replics

import iqde.constructor.actions as func

# from iqde.data.custom.wgets import select_archive

# from iqde.data.custom_wigets import ConfirmationButton


warnings.filterwarnings("ignore")

file = open("iqde/data/logo.png", "rb")
image = file.read()
logo_img = widgets.Image(
    value=image,
    format="png",
    width=70,
    height=70,
)


# исследование таблиц
logo = widgets.Label("Integrated query design environment (IQDE)")
text = widgets.Label("replics:")
select_replic = widgets.Dropdown(layout=layout.select_replic)
text2 = widgets.Label("tables:")
select_tables = widgets.SelectMultiple(layout=layout.select_tables)
text3 = widgets.Label(value="attributes:", layout=layout.text)
select_attrs = widgets.SelectMultiple(layout=layout.select_attrs)
get_joins_btn = widgets.Button(layout=layout.btn, description="joins")

joins_info = widgets.Output(layout=layout.joins_info, description="joins_info")

# Конструктор SQL
text4 = widgets.Label(value="subscription")
subscribe_name = widgets.Text(layout=layout.subscribe_name)
add_subscribe_name_btn = widgets.Button(
    layout=layout.btn, description="save substription"
)

text5 = widgets.Label(value="select FROM:")
select_from = widgets.Dropdown(layout=layout.select_from)
joins_type = widgets.ToggleButtons(
    layout=layout.joins_type, options=["left", "inner", "right"]
)

construct_sql_btn = widgets.Button(layout=layout.btn, description="GET SQL")

sql_redactor = widgets.Textarea(layout=layout.sql_redactor)

text6 = widgets.Label(value="SQL name:")
input_script_name = widgets.Text(
    layout=layout.input_script_name, placeholder="input_script_name"
)
save_script_btn = widgets.Button(layout=layout.btn, description="save_script_btn")

# Архивы
text7 = widgets.Label(value="load archived:")
select_fixed_tab = widgets.Select(layout=layout.select_fixed)
select_customs_tab = widgets.Select(layout=layout.select_customs)
load_archive_btn = widgets.Button(layout=layout.btn, description="LOAD")

# Устанавливаем список доступных к выбору реплик
replics = Replics.objects.all().to_list()
select_replic.options = [
    (f"{replic.business_name} ({replic.system_name})", replic) for replic in replics
]

# Устанавливаем список архивных скриптов, доступных к загрузке
# func.set_saved_scripts(select_fixed_tab)


# Обсерверы для обновления таблиц, полей
def refresh_tables(*args):

    func.refresh_tables(select_replic, select_tables, subscribe_name)


select_replic.observe(refresh_tables, "value")


def refresh_atts(*args):
    func.refresh_attrs(select_replic, select_tables, select_attrs, select_from)


select_tables.observe(refresh_atts, "value")


# Получить джойны
def get_joins(btn):
    get_joins_btn.description = "...search data..."
    get_joins_btn.layout = layout.btn_wait
    try:
        func.get_joins(select_replic, select_attrs, joins_info, select_from, joins_type)
    except Exception:
        get_joins_btn.description = "joins"
    get_joins_btn.description = "joins"
    get_joins_btn.layout = layout.btn


get_joins_btn.on_click(get_joins)


# Создать SQL запрос
def construct_sql(btn):
    func.construct_sql(
        select_attrs,
        subscribe_name,
        select_from,
        sql_redactor,
        select_replic,
        joins_info,
        joins_type,
    )


construct_sql_btn.on_click(construct_sql)

load_archive_btn.on_click(func.load_sql)
add_subscribe_name_btn.on_click(func.save_subscribe)


def check_unique_sql_name(*args):
    func.check_unique_sql_name(input_script_name, save_script_btn)


input_script_name.observe(check_unique_sql_name, "value")


def save_sql(btn):
    func.save_sql(
        input_script_name,
        joins_info,
        sql_redactor,
        # select_archive
    )


save_script_btn.on_click(save_sql)

save_script_btn.disabled = True

# change_script_btn.on_click(change_sql)
