import sqlite3
import itertools

from collections import deque
import networkx as nx
import pandas as pd

from IPython.display import clear_output

from iqde import config
from iqde.models import (
    Replics,
    Tables,
    Attributes,
)


def bfs(graph, start):
    visited = set()
    # TODO: Set() уничтожает порядок следования. Хотелось бы сохранить
    vis = []
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node in graph:
            if node not in visited:
                visited.add(node)
                vis.append(node)
                queue.extend(set(graph[node]) - visited)
    return vis


def get_join_list(select_replic, select_attrs):
    replic = select_replic.value
    attrs = select_attrs.value
    tables_ids = []
    attrs_ids = []
    for attr in attrs:
        table = Tables.objects.get(id=attr.table_id)
        tables_ids.append(table.id)
        attrs_ids.append(attr.id)
    df_users_choise = pd.DataFrame(
        {
            "table_id": tables_ids,
            "id": attrs_ids,
        }
    )

    conn = sqlite3.connect(config.CONSTRUCTOR_DB)
    cursor = conn.cursor()

    cursor.execute(
        f"SELECT * FROM JOINS where replic_left = {replic.id} and replic_right = {replic.id}"
    )
    results = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    edges = pd.DataFrame(results, columns=column_names).astype(int)
    edges = edges[edges["table_left"] != edges["table_right"]]
    cursor.close()
    conn.close()

    table_join_list = df_users_choise[
        df_users_choise["table_id"].isin(
            pd.concat([edges["table_left"], edges["table_right"]])
        )
    ]
    return table_join_list, edges


def get_linked_tables(table_join_list, edges, select_from):
    combinations = list(
        itertools.combinations(
            table_join_list["table_id"].drop_duplicates().tolist(), 2
        )
    )

    G = nx.from_pandas_edgelist(edges, "table_left", "table_right")

    nodes_query = []
    errors = []
    for combination in combinations:
        # TODO: Если связи нет - будет ошибка NetworkXNoPath: No path between 79 and 1023.
        try:
            nodes_query = nodes_query + nx.shortest_path(
                G, combination[0], combination[1]
            )
        except Exception:
            errors.append((combination[0], combination[1]))
    nodes_query = list(set(nodes_query))

    # TODO: Где используется subgraph?
    subgraph = G.subgraph(nodes_query).copy()
    components = list(nx.connected_components(G))
    df_from = pd.DataFrame()
    claster = 0

    start_point = select_from.value.id
    visited_groups = []
    for component in components:
        # TODO: в подграфе может отсутствовать стартовая нода?
        # TODO: Что делает visited?
        visited = list(bfs(subgraph.subgraph(component).copy(), start_point))
        df_from = edges[
            (edges["table_left"].isin(nodes_query))
            & (edges["table_right"].isin(nodes_query))
        ]
        df_from["claster"] = claster
        claster += 1
        visited_groups.append(visited)

    return df_from, visited_groups


def get_objects_for_join(row):
    left_replic = Replics.objects.get(id=int(row["replic_left"]))
    left_table = Tables.objects.get(id=int(row["table_left"]))
    left_attr = Attributes.objects.get(id=int(row["attr_left"]))

    right_replic = Replics.objects.get(id=int(row["replic_right"]))
    right_table = Tables.objects.get(id=int(row["table_right"]))
    right_attr = Attributes.objects.get(id=int(row["attr_right"]))

    data = {
        "left_replic": left_replic.subscribe_name,
        "left_table": left_table.system_name,
        "left_attr": left_attr.system_name,
        "right_replic": right_replic.subscribe_name,
        "right_table": right_table.system_name,
        "right_attr": right_attr.system_name,
    }
    return data


def get_join_string(df_from, visited_groups, select_from, joins_type):
    for group in visited_groups:
        replic = Replics.objects.get(id=select_from.value.replic_id)
        from_table_name = select_from.value.system_name
        strings = [
            f"FROM {replic.subscribe_name}.{from_table_name} AS {from_table_name}"
        ]
        unlinked = group
        linked = []
        while unlinked:
            current = unlinked.pop(0)
            for _, row in df_from.iterrows():
                objects = get_objects_for_join(row)
                if (
                    int(row["table_left"]) == current
                    and row["table_right"] not in linked
                ):
                    string = (
                        f"{joins_type.value} JOIN {objects['right_replic']}.{objects['right_table']} AS "
                        + f"{objects['right_table']}\nON {objects['right_table']}.{objects['right_attr']}"
                        + f" = {objects['left_table']}.{objects['left_attr']}"
                    )
                    strings.append(string)
                    linked.append(row["table_left"])
                    linked.append(row["table_right"])
                if (
                    int(row["table_right"]) == current
                    and row["table_left"] not in linked
                ):
                    string = (
                        f"{joins_type.value} JOIN {objects['left_replic']}.{objects['left_table']} AS "
                        + f"{objects['left_table']}\nON {objects['left_table']}.{objects['left_attr']}"
                        + f" = {objects['right_table']}.{objects['right_attr']}"
                    )
                    strings.append(string)
                    linked.append(row["table_right"])
                    linked.append(row["table_left"])

        return strings


def get_joins(wg):
    table_join_list, edges = get_join_list(wg.replics, wg.attrs)
    df_from, visited_groups = get_linked_tables(table_join_list, edges, wg.select_from)
    join_string = get_join_string(
        df_from, visited_groups, wg.select_from, wg.joins_type
    )

    replic = wg.replics.value
    replic_name = replic.system_name
    joins = []

    for _, row in df_from.iterrows():
        table_left = Tables.objects.get(id=int(row["table_left"]))
        attr_left = Attributes.objects.get(id=int(row["attr_left"]))

        table_right = Tables.objects.get(id=int(row["table_right"]))
        attr_right = Attributes.objects.get(id=int(row["attr_right"]))

        joins.append(
            {
                "table_left": table_left,
                "attr_left": attr_left,
                "table_right": table_right,
                "attr_right": attr_right,
            }
        )

    join_msg = f"""REPLIC: {replic_name.upper()}\n"""

    max_len = 0
    for join in joins:
        length = len(
            f'{join["table_left"].system_name}.{join["attr_left"].system_name}'
        )
        if length > max_len:
            max_len = length

    for join in joins:
        length = len(
            f'{join["table_left"].system_name}.{join["attr_left"].system_name}'
        )
        spaces = max_len - length
        msg = f"""{join["table_left"].system_name}.{join["attr_left"].system_name} {" " * spaces}  <=>  {join["table_right"].system_name}.{join["attr_right"].system_name}\n"""

        join_msg += msg

    with wg.joins_info:
        clear_output()
        print(join_msg)

    return join_string
