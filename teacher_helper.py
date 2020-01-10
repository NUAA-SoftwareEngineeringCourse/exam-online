from config import db_connector, cursor
from datetime import datetime
from common_helper import choice_question_table, judge_question_table, subjective_question_table


def get_question_list_by_ids(ids_list: list, table: str):
    sql = 'SELECT * FROM ' + table + 'WHERE q_id=%s'
    result = []
    for x in ids_list:
        cursor.execute(sql, x)
        result.append(cursor.fetchone())
    return result


# 出卷更新 q_counter, q_year,
def update_questions_info(questions_ids: dict):
    now_year = datetime.now().year
    sql = 'UPDATE {} SET q_year=%s, q_counter=q_counter+1 WHERE q_id=%s'
    for x in questions_ids.get('choice'):
        try:
            cursor.execute(sql.format(choice_question_table), (now_year, x))
            db_connector.commit()
        except:
            db_connector.rollback()

    for x in questions_ids.get('judge'):
        try:
            cursor.execute(sql.format(judge_question_table), (now_year, x))
            db_connector.commit()
        except:
            db_connector.rollback()

    for x in questions_ids.get('subjective'):
        try:
            cursor.execute(sql.format(subjective_question_table), (now_year, x))
            db_connector.commit()
        except:
            db_connector.rollback()
