import ipywidgets as widgets

import iqde.constructor.layouts as layout
import iqde.constructor.wgets as wg

wg.logo.add_class("logo")
wg.logo_img.add_class("logo-img")
wg.get_joins_btn.add_class("btn")
wg.get_joins_btn.add_class("get_joins_btn")
wg.add_subscribe_name_btn.add_class("btn")
wg.add_subscribe_name_btn.add_class("add_subscribe_name_btn")
wg.construct_sql_btn.add_class("btn2")
wg.save_script_btn.add_class("btn")
wg.load_archive_btn.add_class("btn2")
wg.joins_info.add_class("joins_overflow")

wg.text.add_class("text")
wg.text2.add_class("text")
wg.text3.add_class("text")
wg.text4.add_class("text")
wg.text5.add_class("text")
wg.text6.add_class("text")
wg.text7.add_class("text")

wg.select_replic.add_class("select_replic")
wg.select_tables.add_class("select_tables")

wg.select_attrs.add_class("select_attrs")

wg.joins_info.add_class("joins_info_p")
wg.subscribe_name.add_class("subscribe_name")

wg.select_from.add_class("select_from")
wg.joins_type.add_class("joins_type")
wg.sql_redactor.add_class("sql_redactor")
wg.input_script_name.add_class("input_script_name")


# Виджеты группировки
explore_vbox = widgets.VBox(
    children=[wg.text, wg.select_replic, wg.text2, wg.select_tables]
)
explore_vbox2 = widgets.VBox(children=[wg.text3, wg.select_attrs])
explore_hbox = widgets.HBox(
    layout=layout.explore_hbox, children=[explore_vbox, explore_vbox2]
)
explore_hbox2 = widgets.HBox(
    layout=layout.explore_hbox2, children=[wg.get_joins_btn]
)

construct_hbox_sub = widgets.HBox(
    layout=layout.construct_hbox_sub,
    children=[wg.subscribe_name, wg.add_subscribe_name_btn],
)
construct_hbox_join = widgets.HBox(
    layout=layout.construct_hbox_join, children=[wg.select_from, wg.joins_type]
)

construct_hbox_save = widgets.HBox(
    layout=layout.construct_hbox_save,
    children=[wg.text6, wg.input_script_name, wg.save_script_btn],
)

# Виджеты основных блоков
explore = widgets.VBox(
    layout=layout.explore,
    description="explore",
    children=[explore_hbox, wg.get_joins_btn, wg.joins_info],
)
constructor = widgets.VBox(
    layout=layout.construct,
    description="constructor",
    children=[
        wg.text4,
        construct_hbox_sub,
        wg.text5,
        construct_hbox_join,
        wg.construct_sql_btn,
        wg.sql_redactor,
        construct_hbox_save,
    ],
)
select_is_custom = widgets.Tab(
    layout=layout.select_is_custom,
    children=[wg.select_fixed_tab, wg.select_customs_tab],
)
select_is_custom.set_title(0, "defended scripts")
select_is_custom.set_title(1, "custom scripts")
archives = widgets.VBox(
    layout=layout.archives,
    children=[wg.text7, select_is_custom, wg.load_archive_btn],
)


logo_box = widgets.HBox(children=[wg.logo_img, wg.logo])
logo_box.add_class("logo-box")


# Общий виджет, аккумулирует внутри себя все остальные
accordion = widgets.VBox(
    layout=layout.accordion,
    children=[logo_box, explore, constructor],
    selected_index=1,
)
# accordion = widgets.Accordion(layout=lo.accordion_layout, children=[explore, constructor, archives], selected_index=1)
accordion.titles = ("Explore", "Construct", "Archive")
accordion.add_class("provide_accordion")
accordion.add_class("accordion")
