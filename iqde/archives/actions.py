import codecs
import pandas as pd

from IPython.display import clear_output
from sql_metadata import Parser

from iqde.models import (
    Replics,
    Tables,
    Attributes,
    Scripts,
    ScriptsTables,
    ScriptsAttrs
)

from iqde.archives.joins import get_joins


import warnings

warnings.filterwarnings("ignore")


def set_saved_scripts(wgt):

    saved_scripts = Scripts.objects.all().to_list()
    saved_scripts = [script.script_name for script in saved_scripts]
    wgt.options = saved_scripts


# def refresh_tables(tables_wgt, sql_redactor):
#     """Обновить список таблиц при выборе реплики."""
#     replic = Replics.objects.get(system_name=replic_wgt.value)
#     tables_data = Tables.objects.filter(replic_id=replic.id).to_list()
#     tables_data = [(table.system_name, table) for table in tables_data]
#     tables_wgt.options = tables_data
#     subscribe_wgt.value = replic.subscribe_name


def create_attr_string(table, attr):
    """Создание читаемого формата строки для выбора атрибутов."""
    pass


def refresh_attrs(tables_wgt, attrs_wgt, sql_redactor):
    """Обновить список полей при выборе таблиц."""
    sql_text = sql_redactor.value
    parser = Parser(sql_text)
    columns = parser.columns
    df = create_table_attr_df(columns)
    choosed_tables = tables_wgt.value
    attrs = []

    for table in choosed_tables:
        attr_objects = df[df["table"] == table]
        for _, row in attr_objects.iterrows():
            attr = row["attr"]
            align_string = f"{table}  .  {attr.upper()}"
            attrs.append((align_string, (table, attr)))
    attrs_wgt.options = attrs


def construct_sql(
    select_attrs,
    subscribe_name,
    select_from,
    sql_redactor,
    select_replic,
    joins_info,
    joins_type,
):
    """Сформировать текст SQL-запроса."""
    query = "SELECT DISTINCT\n"
    for i, attr in enumerate(select_attrs.value):
        table = attr[0]
        string = f",{table.lower()}.{attr[1].lower()}\n"
        if i == 0:
            string = string[1:]
        query += string

    query += "\n"
    joins_data = get_joins(
        select_replic, select_attrs, joins_info, select_from, joins_type
    )
    for join in joins_data:
        query += f"{join}\n"

    query += f"\nWHERE 1=1\n;"
    sql_redactor.value = query


def save_sql(input_script_name, sql_allert, sql_redactor, archive):
    """Сохранить SQL-запрос в базу."""
    if not input_script_name.value:
        with sql_allert:
            clear_output()
            print("Поле не может быть пустым!")
            return

    sql = Scripts.objects.get(script_name=input_script_name.value)
    if not sql:
        Scripts.objects.add(
            Scripts(script_name=input_script_name.value, sql=sql_redactor.value)
        )
        sql = Scripts.objects.get(script_name=input_script_name.value)

    set_saved_scripts(archive)

    with sql_allert:
        clear_output()
        print("Сохранено!")


def change_sql(btn):
    """Изменить SQL-запрос в базе."""
    sql = Scripts.objects.get(script_name=input_script_name.value)

    # TODO: Надо обязательно проверить надежность получения sql, чтобы не удалить лишнее
    replic = Replics.objects.get(system_name=select_replic.value)
    Scripts.objects.update(
        Scripts(
            sql=sql_redactor.value, replic_id=replic.id, from_table=select_from.value
        ),
        id=sql.id,
    )
    ScriptsTables.objects.delete(script_id=sql.id)
    ScriptsAttrs.objects.delete(script_id=sql.id)

    for table in select_tables.value:
        table = Tables.objects.get(system_name=table[0], replic_id=replic.id)
        ScriptsTables.objects.add(ScriptsTables(script_id=sql.id, table_id=table.id))

    for attr in select_attrs.value:
        table = Tables.objects.get(system_name=attr[0], replic_id=replic.id)
        attr = Attributes.objects.get(system_name=attr[1], table_id=table.id)

        if not attr:
            continue

        sql_attr = ScriptsAttrs.objects.get(script_id=sql.id, attr_id=attr.id)
        ScriptsAttrs.objects.add(ScriptsAttrs(script_id=sql.id, attr_id=attr.id))

    with sql_allert:
        clear_output()
        print("Изменено!")


def create_table_attr_df(columns):
    splited_columns = []
    length = 3
    for column in columns:
        column = column.split(".")
        if len(column) == length:
            splited_columns.append(column)
    headers = ["replic", "table", "attr"]
    df = pd.DataFrame(splited_columns, columns=headers)
    return df


def get_start_end_indexes(tdf):
    start = None
    end = None
    for i, row in tdf.iterrows():
        if row["value"].lower() == "from":
            start = i + 1
        if row["value"].lower() == "where":
            end = i
    return start, end


def get_join_names(tdf):
    names = {}
    for i, row in tdf.iterrows():
        if (
            i == 0
            and not ("join" in row["next_token"].value.lower())
            and (not row["next_token"].value.lower() == "as")
        ):
            prev_name = tdf.iloc[(i)]["value"]
            next_name = tdf.iloc[(i + 1)]["value"]
            names[next_name] = prev_name
            continue

        if "join" in row["previous_token"].value.lower():
            prev_name = tdf.iloc[(i)]["value"]
            if row["next_token"].value.lower() == "as":
                next_name = tdf.iloc[(i + 2)]["value"]
                names[next_name] = prev_name
            if not row["next_token"].value.lower() == "on":
                next_name = tdf.iloc[(i + 1)]["value"]
                names[next_name] = prev_name
            continue

        if row["next_token"].value.lower() == "as":
            prev_name = tdf.iloc[(i)]["value"]
            next_name = tdf.iloc[(i + 2)]["value"]
            names[next_name] = prev_name
            continue
    return names


def create_join_message(tdf, select_tables):
    replic = tdf["left_replic"][0]
    from_table_name = "select_from.value"
    strings = [f"FROM {replic}.{from_table_name} AS {from_table_name}"]
    unlinked = select_tables.value
    linked = []
    while unlinked:
        current = unlinked.pop(0)
        for _, row in tdf.iterrows():

            left_replic = replic
            left_table = row["table_left"]
            left_attr = row["attr_left"]

            right_replic = replic
            right_table = row["table_right"]
            right_attr = row["attr_right"]

            objects = {
                "left_replic": left_replic,
                "left_table": left_table,
                "left_attr": left_attr,
                "right_replic": right_replic,
                "right_table": right_table,
                "right_attr": right_attr,
            }
            if row["table_left"] == current and row["table_right"] not in linked:
                string = (
                    f"JOIN {objects['right_replic']}.{objects['right_table']} AS "
                    + f"{objects['right_table']}\nON {objects['right_table']}.{objects['right_attr']}"
                    + f" = {objects['left_table']}.{objects['left_attr']}"
                )
                strings.append(string)
                linked.append(row["table_left"])
                linked.append(row["table_right"])
            if row["table_right"] == current and row["table_left"] not in linked:
                string = (
                    f"JOIN {objects['left_replic']}.{objects['left_table']} AS "
                    + f"{objects['left_table']}\nON {objects['left_table']}.{objects['left_attr']}"
                    + f" = {objects['right_table']}.{objects['right_attr']}"
                )
                strings.append(string)
                linked.append(row["table_right"])
                linked.append(row["table_left"])

    for s in strings:
        print(s)
    return strings


def set_fields_with_data(
    sql_text, select_replic, select_tables, select_attrs, joins_info
):
    parser = Parser(sql_text)
    columns = parser.columns

    df = create_table_attr_df(columns)
    select_replic.value = df["replic"][0]

    tables = list(df["table"].drop_duplicates())
    select_tables.options = tables

    l = [t.__dict__ for t in parser.tokens]
    tokens_df = pd.DataFrame(l)

    start, end = get_start_end_indexes(tokens_df)
    joins_df = tokens_df[start:end]
    joins_df = joins_df.reset_index()

    names = get_join_names(joins_df)
    names_splited = {}
    for key, value in names.items():
        names_splited[key] = value.split(".")
    names_splited

    links = []
    for i, row in joins_df.iterrows():
        if row["value"].lower() == "=":
            left = joins_df.iloc[(i - 1)]["value"]
            right = joins_df.iloc[(i + 1)]["value"]
            links.append((left, right))

    joins_final = []
    for link in links:
        object_ = {}
        left = link[0].split(".")
        right = link[1].split(".")
        if len(left) == 2:
            object_["left_replic"] = names_splited[left[0]][0]
            object_["left_table"] = names_splited[left[0]][1]
            object_["left_attr"] = left[1]
        if len(right) == 2:
            object_["right_replic"] = names_splited[right[0]][0]
            object_["right_table"] = names_splited[right[0]][1]
            object_["right_attr"] = right[1]
        if len(left) == 3:
            object_["left_replic"] = left[0]
            object_["left_table"] = left[1]
            object_["left_attr"] = left[2]
        if len(right) == 3:
            object_["right_replic"] = right[0]
            object_["right_table"] = right[1]
            object_["right_attr"] = right[2]
        if (
            not len(left) == 2
            and not len(right) == 2
            and not len(left) == 3
            and not len(right) == 3
        ):
            print(
                f"SQL не распарсился:\nНайдены связи: {link}\nНазвания: {names_splited}"
            )
        joins_final.append(object_)

    tdf = pd.DataFrame(joins_final)

    join_sql = create_join_message(tdf, select_tables)

    joins = []

    for _, row in tdf.iterrows():
        table_left = row["left_table"]
        attr_left = row["left_attr"]

        table_right = row["right_table"]
        attr_right = row["right_attr"]

        joins.append(
            {
                "table_left": table_left,
                "attr_left": attr_left,
                "table_right": table_right,
                "attr_right": attr_right,
            }
        )

    join_msg = f"""REPLIC: {df["replic"][0].upper()}\n"""

    max_len = 0
    for join in joins:
        length = len(f'{join["table_left"]}.{join["attr_left"]}')
        if length > max_len:
            max_len = length

    for join in joins:
        length = len(f'{join["table_left"]}.{join["attr_left"]}')
        spaces = max_len - length
        msg = f"""{join["table_left"]}.{join["attr_left"]} {" " * spaces}  <=>  {join["table_right"]}.{join["attr_right"]}\n"""

        join_msg += msg

    with joins_info:
        clear_output()
        print(join_msg)

    return join_sql


def load_sql(
    select_archive,
    sql_redactor,
    input_script_name,
    save_script_btn,
    select_replic,
    select_tables,
    select_attrs,
    joins_info,
):
    """Загрузить SQL-запрос из базы."""
    name = select_archive.value
    sql = Scripts.objects.get(script_name=name)

    sql_redactor.value = sql.sql
    input_script_name.value = sql.script_name
    save_script_btn.disabled = True
    sql_text = sql.sql
    set_fields_with_data(
        sql_text, select_replic, select_tables, select_attrs, joins_info
    )


def check_unique_sql_name(input_script_name, save_script_btn):
    """Управление активностью кнопки сохранения SQL при неуникальном наименовании."""
    sql_name = Scripts.objects.filter(script_name=input_script_name.value).to_list()
    if sql_name:
        # change_script_btn.set_allert_msg(f"Вы уверены, что хотите изменить скрипт {sql_name[0].script_name}")
        save_script_btn.disabled = True
    else:
        # change_script_btn.set_allert_msg(None)
        save_script_btn.disabled = False
    if not str(input_script_name.value).strip():
        save_script_btn.disabled = True


def get_data_from_file(
    read_file,
    read_file_label,
    sql_redactor,
    select_replic,
    select_tables,
    select_attrs,
    joins_info,
    input_script_name,
):
    file_name = read_file.value[0].name
    read_file_label.value = file_name

    sql = codecs.decode(read_file.value[0].content, encoding="utf-8")
    sql_redactor.value = sql

    set_fields_with_data(sql, select_replic, select_tables, select_attrs, joins_info)
    input_script_name.value = file_name.split(".")[0]



# def get_data_from_file(
#     read_file,
#     # read_file_label,
#     sql_redactor,
#     select_replic,
#     select_tables,
#     select_attrs,
#     joins_info,
#     input_script_name,
# ):
#     file_path = read_file.value
#     with open(file_path, 'r') as file:
#         content = file.read()

#     sql_redactor.value = content

#     set_fields_with_data(content, select_replic, select_tables, select_attrs, joins_info)
#     input_script_name.value = file_path.split("/")[1]