import config
import common_helper
from config import db_connector, cursor, student_exam_log_table, user_table, teacher_student_table


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
    sql = 'SELECT student_id, user_name, grade, subjective_grade FROM ' + \
          student_exam_log_table + ' INNER JOIN ' + user_table + ' ON user.user_id=student_exam_log.student_id ' + \
          'WHERE paper_id=%s'
    cursor.execute(sql, paper_id)
    data = cursor.fetchall()
    for x in data:
        if x.get('subjective_grade') != -1:
            x['grade'] += x['subjective_grade']
            x.pop('subjective_grade')
    return sorted(data, key=lambda x: x.get('grade'), reverse=True)


# 上传试卷，同时把试题插入试题数据库，调用点在uploadFile
def insert_questions(paper_id, paper_path, paper_title):
    print('[insert questions]', paper_id, paper_path)

    # (q_description, q_value, q_answer, q_A, q_B, q_C, q_D, q_paperid)
    choice_sql = 'INSERT INTO ' + config.choice_question_table + \
                 '(q_description, q_value, q_answer, q_A, q_B, q_C, q_D, q_paperid, q_type)' + \
                 'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    # (q_description, q_value, q_answer, q_paperid)
    judge_sql = 'INSERT INTO ' + config.judge_question_table + \
                '(q_description, q_value, q_answer, q_paperid, q_type)' + \
                'VALUES (%s, %s, %s, %s, %s)'
    # (q_description, q_value, q_answer, q_paperid)
    subjective_sql = 'INSERT INTO ' + config.subjective_question_table + \
                     '(q_description, q_value, q_answer, q_paperid, q_type)' + \
                     'VALUES (%s, %s, %s, %s, %s)'

    questions = common_helper.parse_paper(paper_path)

    for x in questions:
        q_type = x.get('q_type')
        q_text = x.get('q_text')
        answer = x.get('answer')
        value = x.get('value')
        if q_type == 'radio' or q_type == 'checkbox':
            try:
                cursor.execute(choice_sql,
                               (q_text, value, answer, x.get('A'), x.get('B'), x.get('C'), x.get('D'), paper_id,
                                paper_title))
                db_connector.commit()
            except:
                db_connector.rollback()
        elif q_type == 'decide':
            answer = 1 if answer.upper()[0] == 'T' else 0
            try:
                cursor.execute(judge_sql, (q_text, value, answer, paper_id, paper_title))
                db_connector.commit()
            except:
                db_connector.rollback()
        elif q_type == 'textarea':
            try:
                cursor.execute(subjective_sql, (q_text, value, answer, paper_id, paper_title))
                db_connector.commit()
            except:
                db_connector.rollback()
    return


def insert_teacher_student(paper_class: str, teacher_id, paper_id):
    # 在 teacher_student 中建立关联
    for c in paper_class.split(';'):
        if c != '':
            sql = 'SELECT * FROM `user` WHERE user_id LIKE %s'
            cursor.execute(sql, c + '%')
            students = cursor.fetchall()
            for s in students:
                print('[upload files]', s.get('user_id'))
                sql = 'INSERT INTO ' + teacher_student_table + ' VALUES (%s,%s,%s)'
                try:
                    cursor.execute(sql, (teacher_id, s.get('user_id'), paper_id))
                    db_connector.commit()
                except:
                    db_connector.rollback()
                    return -1
