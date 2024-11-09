import ipywidgets as widgets
import iqde.archives.layouts as layout
import iqde.archives.wgets as cwg

# Подключение стилей css

cwg.logo.add_class("logo")
cwg.logo_img.add_class("logo-img")
cwg.save_script_btn.add_class("btn-c")
cwg.load_archive_btn.add_class("btn2-c")
cwg.joins_info.add_class("joins_overflow")

cwg.read_file.add_class("read-file-btn")

cwg.text.add_class("text")
cwg.text2.add_class("text")
cwg.text3.add_class("text")
# cwg.text4.add_class("text")
cwg.text5.add_class("text")
cwg.text6.add_class("text")
cwg.text7.add_class("text")
cwg.read_file_label.add_class("text")
cwg.read_file_label.add_class("read_file_label")


cwg.select_replic.add_class("select_replic")
cwg.select_tables.add_class("select_tables")

cwg.select_attrs.add_class("select_attrs")

cwg.joins_info.add_class("joins_info_c")
# cwg.subscribe_name.add_class("subscribe_name")

cwg.select_archive.add_class("select_archive")
cwg.select_from.add_class("select_from")
cwg.joins_type.add_class("joins_type")
cwg.sql_redactor.add_class("sql_redactor")
cwg.input_script_name.add_class("input_script_name")


# Виджеты группировки
explore_vbox = widgets.VBox(
    children=[cwg.text, cwg.select_replic, cwg.text2, cwg.select_tables]
)
explore_vbox2 = widgets.VBox(children=[cwg.text3, cwg.select_attrs])
explore_hbox = widgets.HBox(
    layout=layout.explore_hbox, children=[explore_vbox, explore_vbox2]
)
explore_hbox2 = widgets.HBox(layout=layout.explore_hbox2, children=[])

construct_hbox_save = widgets.HBox(
    layout=layout.construct_hbox_save,
    children=[cwg.text6, cwg.input_script_name, cwg.save_script_btn],
)

# Виджеты основных блоков
explore = widgets.VBox(
    layout=layout.explore,
    description="explore",
    children=[explore_hbox, explore_hbox2, cwg.joins_info],
)
constructor = widgets.VBox(
    layout=layout.construct,
    description="constructor",
    children=[
        # cwg.construct_sql_btn,
        cwg.sql_redactor,
        construct_hbox_save,
    ],
)

read_file_and_label = widgets.VBox(children=[cwg.read_file, cwg.read_file_label])
read_file_and_label.add_class("read_file_and_label")

select_archive_and_file = widgets.HBox(
    children=[cwg.select_archive, read_file_and_label]
)

archives = widgets.VBox(
    layout=layout.archives,
    children=[cwg.text7, select_archive_and_file, cwg.load_archive_btn],
)

logo_box = widgets.HBox(children=[cwg.logo_img, cwg.logo])
logo_box.add_class("logo-box")

# Общий виджет, аккумулирует внутри себя все остальные
accordion = widgets.VBox(
    layout=layout.accordion,
    children=[logo_box, archives, explore, constructor],
    selected_index=1,
)
accordion.add_class("custom_accordion")
accordion.add_class("accordion")
