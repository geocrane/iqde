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


def set_replics_options(wg):
    replics = Replics.objects.all().to_list()
    replics_options = []
    for replic in replics:
        if replic.business_name:
            option_title = replic.business_name.upper()
        else:
            option_title = "БЕЗ ИМЕНИ"
        replics_options.append((f"{option_title} ({replic.system_name})", replic))
    wg.replics.options = replics_options


def replic_observer_updates(wg):
    """Обновить виджеты при выборе реплики."""
    replic = wg.replics.value
    tables = Tables.objects.filter(replic_id=replic.id).to_list()
    options = [
        (f"{table.system_name} ({table.business_name.upper()})", table)
        for table in tables
    ]
    wg.tables.options = options
    wg.subscribe.value = replic.subscribe_name


def tables_observer_updates(wg):
    """Обновить виджеты при выборе таблиц."""
    tables = wg.tables.value
    attrs_options = []
    for table in tables:
        attrs = Attributes.objects.filter(table_id=table.id).to_list()
        for attr in attrs:
            option_title = f"{table.system_name}  .  {attr.system_name.upper()}   .  ({attr.business_name.capitalize()})  .  (type: {attr.type})"
            attrs_options.append((option_title, attr))
    wg.attrs.options = attrs_options
    from_options = [(i.system_name, i) for i in tables]
    wg.select_from.options = from_options
    if from_options:
        wg.select_from.value = from_options[0][1]


def construct_sql(wg):
    """Сформировать текст SQL-запроса."""
    query = "SELECT DISTINCT\n"
    for i, attr in enumerate(wg.attrs.value):
        table = Tables.objects.get(id=attr.table_id)
        line = f",{table.system_name.lower()}.{attr.system_name.lower()} as `{attr.business_name.capitalize()}`\n"
        if i == 0:
            line = line[1:]
        query += line
    query += "\n"
    joins_data = get_joins(wg)
    for join in joins_data:
        query += f"{join}\n"
    query += "\nWHERE 1=1\n;"
    wg.sql_redactor.value = query


def save_sql(wg, archive):
    """Сохранить SQL-запрос в базу."""
    sql = Scripts.objects.get(script_name=wg.input_script_name.value)
    if not sql:
        Scripts.objects.add(
            Scripts(script_name=wg.input_script_name.value, sql=wg.sql_redactor.value)
        )
        sql = Scripts.objects.get(script_name=wg.input_script_name.value)

    set_saved_scripts(archive)


def check_unique_sql_name(wg):
    """Управление активностью кнопки сохранения SQL при неуникальном наименовании."""
    sql_name = Scripts.objects.filter(script_name=wg.input_script_name.value).to_list()
    if sql_name:
        wg.save_script_btn.disabled = True
    else:
        wg.save_script_btn.disabled = False
    if not str(wg.input_script_name.value).strip():
        wg.save_script_btn.disabled = True


# def change_sql(btn):
#     """Изменить SQL-запрос в базе."""
#     sql = Scripts.objects.get(script_name=input_script_name.value)

#     # TODO: Надо обязательно проверить надежность получения sql, чтобы не удалить лишнее
#     replic = Replics.objects.get(system_name=select_replic.value)
#     Scripts.objects.update(
#         Scripts(
#             sql=sql_redactor.value, replic_id=replic.id, from_table=select_from.value
#         ),
#         id=sql.id,
#     )
#     ScriptsTables.objects.delete(script_id=sql.id)
#     ScriptsAttrs.objects.delete(script_id=sql.id)

#     for table in select_tables.value:
#         table = Tables.objects.get(system_name=table[0], replic_id=replic.id)
#         ScriptsTables.objects.add(ScriptsTables(script_id=sql.id, table_id=table.id))

#     for attr in select_attrs.value:
#         table = Tables.objects.get(system_name=attr[0], replic_id=replic.id)
#         attr = Attributes.objects.get(system_name=attr[1], table_id=table.id)

#         if not attr:
#             continue

#         sql_attr = ScriptsAttrs.objects.get(script_id=sql.id, attr_id=attr.id)
#         ScriptsAttrs.objects.add(ScriptsAttrs(script_id=sql.id, attr_id=attr.id))

#     with sql_allert:
#         clear_output()
#         print("Изменено!")


def save_subscribe(btn):
    """Сохранить имя подписки."""
    pass
    # # TODO: База блокируется при нарушении уникальности.
    # replic = Replics.objects.get(system_name=select_replic.value)
    # Replics.objects.update(Replics(subscribe_name=subscribe_name.value), id=replic.id)
