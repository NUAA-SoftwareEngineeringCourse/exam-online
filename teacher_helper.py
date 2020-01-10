from config import db_connector, cursor


def get_question_list_by_ids(ids_list: list, table: str):
    sql = 'SELECT * FROM ' + table + 'WHERE q_id=%s'
    result = []
    for x in ids_list:
        cursor.execute(sql, x)
        result.append(cursor.fetchone())
    return result
