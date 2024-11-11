from iqde.constructor import wgets as wg
from iqde.archives.wgets import archive
from iqde.constructor import scripts as scr


scr.set_replics_options(wg)


def replic_observer_updates(*args):
    scr.replic_observer_updates(wg)


wg.replics.observe(replic_observer_updates, "value")


def tables_observer_updates(*args):
    scr.tables_observer_updates(wg)


wg.tables.observe(tables_observer_updates, "value")


def check_unique_sql_name(*args):
    scr.check_unique_sql_name(wg)


wg.input_script_name.observe(check_unique_sql_name, "value")


def get_joins(btn):
    wg.get_joins_btn.description = "...search data..."
    # TODO: При ошибке мы ее не увидим
    try:
        scr.get_joins(wg)
    except Exception:
        wg.get_joins_btn.description = "joins (ошибка)"
    wg.get_joins_btn.description = "joins"


wg.get_joins_btn.on_click(get_joins)


def construct_sql(btn):
    scr.construct_sql(wg)


wg.construct_sql_btn.on_click(construct_sql)


def save_sql(btn):
    scr.save_sql(wg, archive)


wg.save_script_btn.on_click(save_sql)
wg.save_script_btn.disabled = True


wg.add_subscribe_btn.on_click(scr.save_subscribe)
