import xlrd

student_type = 'STUDENT'
teacher_type = 'TEACHER'


def check_type(user_id: str) -> str:
    if user_id != '' and user_id[0] == 'T':
        return teacher_type
    return student_type


def month_int2str(month: int) -> str:
    month_table = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                   'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    return month_table[month-1]


def parse_paper(path: str):
    id_inc = int(0)
    questions_list = list()
    std_single = dict(q_type='radio', q_text='', id=0,
                      A='', B='', C='', D='', value=0)
    std_multiple = dict(q_type='checkbox', q_text='',
                        id=0, A='', B='', C='', D='', value=0)
    std_judge = dict(q_type='decide', q_text='', id=0, value=0)

    xlsx_file = xlrd.open_workbook(path)
    single_sheet = xlsx_file.sheet_by_index(0)
    print(single_sheet.row_values(0))
    for i in range(1, single_sheet.nrows):
        question = single_sheet.row_values(i)
        std_single['q_text'] = question[0]
        std_single['A'] = question[1]
        std_single['B'] = question[2]
        std_single['C'] = question[3]
        std_single['D'] = question[4]
        std_single['value'] = int(question[6])
        std_single['id'], id_inc = id_inc, id_inc + 1
        questions_list.append(dict(std_single))

    multiple_sheet = xlsx_file.sheet_by_index(1)
    print(multiple_sheet.row_values(0))
    for i in range(1, multiple_sheet.nrows):
        question = multiple_sheet.row_values(i)
        std_multiple['q_text'] = question[0]
        std_multiple['A'] = question[1]
        std_multiple['B'] = question[2]
        std_multiple['C'] = question[3]
        std_multiple['D'] = question[4]
        std_multiple['value'] = question[6]
        std_multiple['id'], id_inc = id_inc, id_inc + 1
        questions_list.append(dict(std_multiple))

    judge_sheet = xlsx_file.sheet_by_index(2)
    print(judge_sheet.row_values(0))
    for i in range(1, judge_sheet.nrows):
        question = judge_sheet.row_values(i)
        std_judge['q_text'] = question[0]
        std_judge['value'] = question[2]
        std_judge['id'], id_inc = id_inc, id_inc + 1
        questions_list.append(dict(std_judge))
    return questions_list
