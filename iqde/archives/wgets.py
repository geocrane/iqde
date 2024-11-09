import ipywidgets as widgets


import iqde.archives.layouts as layout
from iqde.models import Replics

import iqde.archives.actions as func
from iqde.plugins.custom_wigets import ConfirmationButton


import warnings

warnings.filterwarnings("ignore")


# import os
# files = os.listdir('scripts_files')


file = open("iqde/data/sber.png", "rb")
image = file.read()
logo_img = widgets.Image(
    value=image,
    format="png",
    width=70,
    height=70,
)


# исследование таблиц
logo = widgets.Label("Integrated query design environment (IQDE)")

# исследование таблиц
text = widgets.Label("subscription:")
select_replic = widgets.Text(layout=layout.select_replic)
text2 = widgets.Label("tables:")
select_tables = widgets.SelectMultiple(layout=layout.select_tables)
text3 = widgets.Label(value="attributes:", layout=layout.text)
select_attrs = widgets.SelectMultiple(layout=layout.select_attrs)
# get_joins_btn = widgets.Button(layout=lo.btn, description="get_joins_btn")

joins_info = widgets.Output(layout=layout.joins_info, description="joins_info")

text5 = widgets.Label(value="select FROM:")
select_from = widgets.Dropdown(layout=layout.select_from)
joins_type = widgets.ToggleButtons(
    layout=layout.joins_type, options=["left", "inner", "right"]
)

# construct_sql_btn = widgets.Button(layout=lo.btn, description="reCONSTRUCT")

sql_redactor = widgets.Textarea(layout=layout.sql_redactor)

text6 = widgets.Label(value="SQL name:")
input_script_name = widgets.Text(
    layout=layout.input_script_name, placeholder="input_script_name"
)
save_script_btn = widgets.Button(layout=layout.btn, description="save_script_btn")

# Архивы
text7 = widgets.Label(value="load archived:")
select_archive = widgets.Select(layout=layout.select_fixed)
load_archive_btn = widgets.Button(layout=layout.btn, description="GET")

read_file = widgets.FileUpload(description="LOAD FILE", accept=".sql", multiple=False)
read_file_label = widgets.Label(value="")

# files = [f"scripts_files/{file}" for file in files]
# read_file = widgets.Select(options=files, layout={"height": "200px"})


def get_data_from_file(*args):
    func.get_data_from_file(
        read_file,
        read_file_label,
        sql_redactor,
        select_replic,
        select_tables,
        select_attrs,
        joins_info,
        input_script_name,
    )
    pass


read_file.observe(get_data_from_file, "value")


# Устанавливаем список доступных к выбору реплик
replics = Replics.objects.all().to_list()
select_replic.options = [replic.system_name for replic in replics]

# Устанавливаем список архивных скриптов, доступных к загрузке
func.set_saved_scripts(select_archive)


# Обсерверы для обновления таблиц, полей
def refresh_tables(*args):

    func.refresh_tables(select_tables, sql_redactor)


# select_replic.observe(refresh_tables, "value")


def refresh_atts(*args):
    func.refresh_attrs(select_tables, select_attrs, sql_redactor)


select_tables.observe(refresh_atts, "value")


# Создать SQL запрос
def construct_sql(btn):
    func.construct_sql(
        select_attrs,
        select_replic,
        select_from,
        sql_redactor,
        select_replic,
        joins_info,
        joins_type,
    )


# construct_sql_btn.on_click(construct_sql)


def load_sql(btn):
    func.load_sql(
        select_archive,
        sql_redactor,
        input_script_name,
        save_script_btn,
        select_replic,
        select_tables,
        select_attrs,
        joins_info,
    )


load_archive_btn.on_click(load_sql)


def check_unique_sql_name(*args):
    func.check_unique_sql_name(input_script_name, save_script_btn)


input_script_name.observe(check_unique_sql_name, "value")


def save_sql(btn):
    func.save_sql(input_script_name, joins_info, sql_redactor, select_archive)


save_script_btn.on_click(save_sql)
save_script_btn.disabled = True

# change_script_btn.on_click(change_sql)
