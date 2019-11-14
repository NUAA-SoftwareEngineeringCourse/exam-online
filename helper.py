student_type = 'STUDENT'
teacher_type = 'TEACHER'


def check_type(user_id: str) -> str:
    if user_id != '' and user_id[0] == 'T':
        return teacher_type
    return student_type
