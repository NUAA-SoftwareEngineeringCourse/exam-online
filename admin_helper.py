import xlrd
from datetime import datetime
from config import user_table, choice_question_table, judge_question_table, subjective_question_table
from config import db_connector, cursor
from common_helper import student_type, teacher_type


def insert_users_by_file(path: str):
    sql = 'INSERT INTO ' + user_table + \
          '(user_id, user_name, user_password, user_create_time, user_update_time, user_type)' + \
          'VALUES (%s, %s, %s, now(), now(), %s)'
    user_excel = xlrd.open_workbook(path)
    sheet = user_excel.sheet_by_index(0)
    for i in range(1, sheet.nrows):
        row_val = sheet.row_values(i)
        print(row_val)
        id, name, role = row_val[0], row_val[1], row_val[2]
        if role == '学生':
            id = str(int(id))
            role = student_type
        elif role == '教师':
            id = str(id)
            role = teacher_type
        if cursor.execute(sql, (id, name, id, role)) == 0:
            print('[insert users by file]', row_val, 'failed!')
            db_connector.rollback()
            return False
    db_connector.commit()
    return True


def admin_get_user_list():
    user_list = list()
    user_dict = {'user_id:': '', 'password': '', 'user_type': ''}
    sql = 'SELECT * FROM ' + user_table
    cursor.execute(sql)
    userdata = cursor.fetchall()
    for x in userdata:
        u = dict(user_dict)
        u['user_id'] = x.get('user_id')
        u['password'] = x.get('user_password')
        u['user_type'] = x.get('user_type')
        u['user_name'] = x.get('user_name')
        u['user_email'] = x.get('user_email')
        user_list.append(u)
    return user_list


def admin_get_questions_type():
    sql = 'SELECT DISTINCT q_type FROM {}'
    cursor.execute(sql.format(choice_question_table))
    l1 = [x.get('q_type') for x in cursor.fetchall()]
    cursor.execute(sql.format(judge_question_table))
    l2 = [x.get('q_type') for x in cursor.fetchall()]
    cursor.execute(sql.format(subjective_question_table))
    l3 = [x.get('q_type') for x in cursor.fetchall()]
    return set(l1 + l2 + l3)


# 挑选题目的策略函数
# difficulity >=3 为 hard
def select_questions_strategy(ques_list, total_num, hard_num):
    # 先按频率排序
    ques_list = sorted(ques_list, key=lambda x: x.get('q_counter'))

    hard_factor = 3
    difficulity_key = 'q_difficulty'
    now_year = datetime.now().year

    # 避免题库不足
    total_num = min(total_num, len(ques_list))
    hard_num = min(total_num, hard_num)
    easy_num = total_num - hard_num

    # 前若干年的list, 此处设定为前2年
    # easy_list 是最近若干年的, l[0]是easy, l[1]是hard
    # hard_list 是前若干年的题, l[0]是easy, l[1]是hard

    diff_year = 2
    easy_list = []
    hard_list = []
    for x in ques_list:
        if x.get(difficulity_key) >= hard_factor:
            hard_list.append(dict(x))
        else:
            easy_list.append(dict(x))

    easy_list = sorted(easy_list, key=lambda x: x.get('q_year'))
    hard_list = sorted(hard_list, key=lambda x: x.get('q_year'))

    result_list = []
    for x in easy_list[0:easy_num]:
        result_list.append(x)
    for x in hard_list[0:hard_num]:
        result_list.append(x)

    return sorted(result_list, key=lambda x: x.get(difficulity_key))

# sql = 'SELECT * FROM {} WHERE q_type like %s'
# cursor.execute(sql.format(choice_question_table), '软件测试')
# all_choices = sorted(cursor.fetchall(), key=lambda x: x.get('q_counter'))
# all_choices = select_questions_strategy(all_choices, 10, 3)
# print(len(all_choices))
# for x in all_choices:
#     print(x)
