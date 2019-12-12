import config
from config import db_connector, cursor, student_exam_log_table, user_table


def get_students(columns: str):
    sql = 'select ' + columns + ' from ' + config.user_table + ' where user_type like "STUDENT"'
    cursor.execute(sql)
    return cursor.fetchall()


def get_papers(columns: str):
    sql = 'select ' + columns + ' from ' + config.exam_paper_table
    cursor.execute(sql)
    return cursor.fetchall()


# return [{'student_id':'', 'user_name':'', 'grade':0}, ..., {}]
# 此处的grade是指总分，即grade（客观题）+subjective_grade（主观题）
def get_students_by_paperid(paper_id):
    sql = 'SELECT student_id, user_name, grade+subjective_grade AS grade FROM ' + \
          student_exam_log_table + ' INNER JOIN ' + user_table + ' ON user.user_id=student_exam_log.student_id ' + \
          'WHERE paper_id=%s'
    cursor.execute(sql, paper_id)
    return cursor.fetchall()
