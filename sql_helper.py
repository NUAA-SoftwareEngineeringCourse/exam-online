import config
from config import db_connector, cursor


def get_students(columns: str):
    sql = 'select ' + columns + ' from ' + config.user_table + ' where user_type like "STUDENT"'
    cursor.execute(sql)
    return cursor.fetchall()


def get_papers(columns: str):
    sql = 'select ' + columns + ' from ' + config.exam_paper_table
    cursor.execute(sql)
    return cursor.fetchall()

