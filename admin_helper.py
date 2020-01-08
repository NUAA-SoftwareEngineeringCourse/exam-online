import xlrd
from config import user_table
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
