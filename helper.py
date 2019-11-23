student_type = 'STUDENT'
teacher_type = 'TEACHER'


def check_type(user_id: str) -> str:
    if user_id != '' and user_id[0] == 'T':
        return teacher_type
    return student_type


def month_int2str(month: int) -> str:
    month_table = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    return month_table[month-1]
