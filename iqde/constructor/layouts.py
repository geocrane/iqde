from ipywidgets import Layout

btn = Layout(width="150px", height="30px")
btn_wait = Layout(button_style="warning", width="150px", height="30px")

# Исследование
text = Layout(margin="0px 0px 0px 25px")
select_replic = Layout(width="540px")
select_tables = Layout(width="540px", height="200px")
select_attrs = Layout(width="740px", height="270px", margin="0px 0px 0px 25px")
joins_info = Layout(
    width="1300px", border="solid 1px white", margin="20px 0px 30px 0px"
)

# Конструктор
subscribe_name = Layout(width="580px")
select_from = Layout(width="750px")
joins_type = Layout()
sql_redactor = Layout(width="1300px", height="400px", margin="15px 0 0 0")
input_script_name = Layout(width="500px")

# Архивы
select_fixed = Layout(width="800px", height="200px")
select_customs = Layout(width="100%", height="200px")

# Виджеты размещения
explore_hbox = Layout()
explore_hbox2 = Layout(justify_content="flex-end")
construct_hbox_sub = Layout(width="1300px")
construct_hbox_join = Layout(justify_content="space-between", margin="0 0 20px 0")
construct_hbox_save = Layout(justify_content="flex-end", margin="10px 0 0 0")

# Виджеты основных блоков
explore = Layout(width="100%")
construct = Layout(width="100%")
select_is_custom = Layout(width="100%")
archives = Layout(width="100%")

# Общий виджет, аккумулирует внутри себя все остальные
accordion = Layout(width="1470px")
