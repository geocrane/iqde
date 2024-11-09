from IPython.display import clear_output

from iqde.models import (
    Replics,
    Tables,
    Attributes,
    Scripts,
    ScriptsTables,
    ScriptsAttrs,
)

from iqde.constructor.joins import get_joins


import warnings

warnings.filterwarnings("ignore")


def set_saved_scripts(wgt):

    saved_scripts = Scripts.objects.all().to_list()
    saved_scripts = [script.script_name for script in saved_scripts]
    wgt.options = saved_scripts


def refresh_tables(replic_wgt, tables_wgt, subscribe_wgt):
    """Обновить список таблиц при выборе реплики."""
    replic = replic_wgt.value
    tables_data = Tables.objects.filter(replic_id=replic.id).to_list()
    tables_data = [
        (f"{table.system_name} ({table.business_name.upper()})", table)
        for table in tables_data
    ]
    tables_wgt.options = tables_data
    subscribe_wgt.value = replic.subscribe_name


def create_attr_string(table, attr):
    """Создание читаемого формата строки для выбора атрибутов."""
    pass


def refresh_attrs(replic_wgt, tables_wgt, attrs_wgt, select_from_wgt):
    """Обновить список полей при выборе таблиц."""
    choosed_tables = tables_wgt.value

    attrs = []

    for table in choosed_tables:
        attr_objects = Attributes.objects.filter(table_id=table.id).to_list()
        for attr in attr_objects:
            align_string = f"""
{table.system_name}  .
            {attr.system_name.upper()}   .  ({attr.business_name.capitalize()})  .  (type: {attr.type})
            """
            attrs.append((align_string, attr))
    attrs_wgt.options = attrs
    options = [(i.system_name, i) for i in choosed_tables]
    select_from_wgt.options = options
    if options:
        select_from_wgt.value = options[0][1]


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
        table = Tables.objects.get(id=attr.table_id)
        string = f",{table.system_name.lower()}.{attr.system_name.lower()} as `{attr.business_name.capitalize()}`\n"
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


def load_sql(btn):
    """Загрузить SQL-запрос из базы."""
    name = select_fixed_tab.value
    sql = Scripts.objects.get(script_name=name)
    replic = Replics.objects.get(id=sql.replic_id)
    tables = ScriptsTables.objects.filter(script_id=sql.id).to_list()
    attrs = ScriptsAttrs.objects.filter(script_id=sql.id).to_list()

    tables_ids = [table.table_id for table in tables]
    attrs_ids = [attr.attr_id for attr in attrs]

    sql_redactor.value = sql.sql
    input_script_name.value = sql.script_name


def save_subscribe(btn):
    """Сохранить имя подписки."""
    # TODO: База блокируется при нарушении уникальности.
    replic = Replics.objects.get(system_name=select_replic.value)
    Replics.objects.update(Replics(subscribe_name=subscribe_name.value), id=replic.id)


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
