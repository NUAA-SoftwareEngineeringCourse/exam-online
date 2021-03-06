import xlrd
import xlwt
from config import choice_question_table, judge_question_table, subjective_question_table
from config import cursor, db_connector

student_type = 'STUDENT'
teacher_type = 'TEACHER'
admin_type = 'ADMIN'


def print_log(name: str, info):
    print('[' + name + ']' + '    ' + str(info))
    return


def check_type(user_id: str) -> str:
    if user_id != '' and user_id[0] == 'T':
        return teacher_type
    return student_type


def month_int2str(month: int) -> str:
    month_table = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                   'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    return month_table[month - 1]


def parse_paper(path: str):
    id_inc = int(0)
    questions_list = list()
    std_single = dict(q_type='radio', q_text='', id=0,
                      A='', B='', C='', D='', value=0)
    std_multiple = dict(q_type='checkbox', q_text='',
                        id=0, A='', B='', C='', D='', value=0)
    std_judge = dict(q_type='decide', q_text='', id=0, value=0)

    std_subjective = dict(q_type='textarea', q_text='', id=0, value=0)

    xlsx_file = xlrd.open_workbook(path)
    single_sheet = xlsx_file.sheet_by_index(0)
    print_log('parse paper', single_sheet.row_values(0))
    for i in range(1, single_sheet.nrows):
        question = single_sheet.row_values(i)
        std_single['q_text'] = question[0]
        std_single['A'] = question[1]
        std_single['B'] = question[2]
        std_single['C'] = question[3]
        std_single['D'] = question[4]
        std_single['answer'] = question[5]
        std_single['value'] = int(question[6])
        std_single['id'], id_inc = id_inc, id_inc + 1
        questions_list.append(dict(std_single))

    multiple_sheet = xlsx_file.sheet_by_index(1)
    print_log('parse paper', multiple_sheet.row_values(0))
    for i in range(1, multiple_sheet.nrows):
        question = multiple_sheet.row_values(i)
        std_multiple['q_text'] = question[0]
        std_multiple['A'] = question[1]
        std_multiple['B'] = question[2]
        std_multiple['C'] = question[3]
        std_multiple['D'] = question[4]
        std_multiple['answer'] = question[5]
        std_multiple['value'] = question[6]
        std_multiple['id'], id_inc = id_inc, id_inc + 1
        questions_list.append(dict(std_multiple))

    judge_sheet = xlsx_file.sheet_by_index(2)
    print_log('parse paper', judge_sheet.row_values(0))
    for i in range(1, judge_sheet.nrows):
        question = judge_sheet.row_values(i)
        std_judge['q_text'] = question[0]
        std_judge['answer'] = question[1]
        std_judge['value'] = question[2]
        std_judge['id'], id_inc = id_inc, id_inc + 1
        questions_list.append(dict(std_judge))

    subjective_sheet = xlsx_file.sheet_by_index(3)
    print_log('parse paper', subjective_sheet.row_values(0))
    for i in range(1, subjective_sheet.nrows):
        question = subjective_sheet.row_values(i)
        std_subjective['q_text'] = question[0]
        std_subjective['answer'] = question[1]
        std_subjective['value'] = question[2]
        std_subjective['id'], id_inc = id_inc, id_inc + 1
        questions_list.append(dict(std_subjective))
    return questions_list


def get_grade_segment(student_list: list) -> dict:
    seg = dict({'levelA': 0, 'levelB': 0, 'levelC': 0, 'levelD': 0, 'levelE': 0})
    for x in student_list:
        if x['grade'] >= 91:
            seg['levelA'] += 1
        elif x['grade'] >= 81:
            seg['levelB'] += 1
        elif x['grade'] >= 71:
            seg['levelC'] += 1
        elif x['grade'] >= 60:
            seg['levelD'] += 1
        else:
            seg['levelE'] += 1
    return seg


def compare_answer(answers: dict, paper_path: str) -> int:
    print_log('cmp ans', answers)
    print_log('cmp ans', paper_path)

    grade = 0

    excel_file = xlrd.open_workbook(paper_path)
    single_sheet = excel_file.sheet_by_index(0)
    multiple_sheet = excel_file.sheet_by_index(1)
    judge_sheet = excel_file.sheet_by_index(2)
    subjective_sheet = excel_file.sheet_by_index(3)

    single_answers = single_sheet.col_values(5)[1:]
    single_values = [int(x) for x in single_sheet.col_values(6)[1:]]

    multiple_answers = multiple_sheet.col_values(5)[1:]
    multiple_values = [int(x) for x in multiple_sheet.col_values(6)[1:]]

    judge_answers = judge_sheet.col_values(1)[1:]
    judge_values = [int(x) for x in judge_sheet.col_values(2)[1:]]

    subjective_values = [int(x) for x in subjective_sheet.col_values(2)[1:]]

    for i in range(0, len(judge_answers)):
        s = str(judge_answers[i]).lower()
        if s[0] == 't' or s[0] == '1' or s == '对':
            judge_answers[i] = '1'
        elif s == 'f' or s[0] == '0' or s == '错':
            judge_answers[i] = '0'

    for i in range(0, len(single_answers)):
        if answers.get(str(i)) == single_answers[i]:
            grade += int(single_values[i])

    inc = len(single_answers)
    for i in range(0, len(multiple_answers)):
        if set(answers.get(str(inc + i))) == set(multiple_answers[i]):
            grade += int(multiple_values[i])

    inc += len(multiple_answers)
    for i in range(0, len(judge_answers)):
        if answers.get(str(inc + i)) == judge_answers[i]:
            grade += int(judge_values[i])

    full_grade = sum(single_values) + sum(multiple_values) + sum(judge_values) + sum(subjective_values)
    return grade, full_grade


def get_std_answers(path: str):
    excel_file = xlrd.open_workbook(path)
    single_sheet = excel_file.sheet_by_index(0)
    multiple_sheet = excel_file.sheet_by_index(1)
    judge_sheet = excel_file.sheet_by_index(2)
    subjective_sheet = excel_file.sheet_by_index(3)

    std_ans = {}
    single_ans = single_sheet.col_values(5)[1:]
    multiple_ans = multiple_sheet.col_values(5)[1:]
    judge_ans = judge_sheet.col_values(1)[1:]
    subjective_ans = subjective_sheet.col_values(1)[1:]

    for i in range(0, len(judge_ans)):
        s = str(judge_ans[i]).lower()
        if s[0] == 't' or s[0] == '1' or s == '对':
            judge_ans[i] = '1'
        elif s[0] == 'f' or s[0] == '0' or s == '错':
            judge_ans[i] = '0'

    order = 0
    for x in single_ans:
        std_ans[str(order)], order = x, order + 1

    for y in multiple_ans:
        std_ans[str(order)], order = y, order + 1

    for z in judge_ans:
        std_ans[str(order)], order = z, order + 1

    for s in subjective_ans:
        std_ans[str(order)], order = s, order + 1
    return std_ans


def add_sheet_header(header: list, sheet: xlwt.Worksheet):
    col = 0
    for h in header:
        sheet.write(0, col, h)
        col += 1
    return


def add_choice_row(sheet: xlwt.Worksheet, data: dict, row: int):
    sheet.write(row, 0, data.get('q_description'))
    sheet.write(row, 1, data.get('q_A'))
    sheet.write(row, 2, data.get('q_B'))
    sheet.write(row, 3, data.get('q_C'))
    sheet.write(row, 4, data.get('q_D'))
    sheet.write(row, 5, data.get('q_answer'))
    sheet.write(row, 6, data.get('q_value'))
    return


def add_judge_row(sheet: xlwt.Worksheet, data: dict, row: int):
    sheet.write(row, 0, data.get('q_description'))
    sheet.write(row, 1, data.get('q_answer'))
    sheet.write(row, 2, data.get('q_value'))
    return


def add_subjective_row(sheet: xlwt.Worksheet, data: dict, row: int):
    add_judge_row(sheet, data, row)
    return


def write_paper_file(question_ids: dict, output_file:str):
    print_log('write paper file', question_ids)

    choice_sql = 'SELECT * FROM ' + choice_question_table + 'WHERE q_id=%s'
    judge_sql = 'SELECT * FROM ' + judge_question_table + 'WHERE q_id=%s'
    subjective_sql = 'SELECT * FROM ' + subjective_question_table + 'WHERE q_id=%s'

    choice_header = ['Description', 'A', 'B', 'C', 'D', 'Answer', 'Value']
    judge_header = ['Description', 'Answer', 'Value']
    subjective_header = list(judge_header)

    workbook = xlwt.Workbook()
    single_sheet = workbook.add_sheet('单项选择题')
    multi_sheet = workbook.add_sheet('多项选择题')
    judge_sheet = workbook.add_sheet('判断题')
    subjective_sheet = workbook.add_sheet('主观题')

    add_sheet_header(choice_header, single_sheet)
    add_sheet_header(choice_header, multi_sheet)
    add_sheet_header(judge_header, judge_sheet)
    add_sheet_header(subjective_header, subjective_sheet)

    single_row, multi_row, judge_row, subjective_row = 1, 1, 1, 1

    for choice_id in question_ids.get('choice'):
        cursor.execute(choice_sql, choice_id)
        data = cursor.fetchone()
        if len(data.get('q_answer')) == 1:
            add_choice_row(sheet=single_sheet, data=data, row=single_row)
            single_row += 1
        else:
            add_choice_row(sheet=multi_sheet, data=data, row=multi_row)
            multi_row += 1

    for judge_id in question_ids.get('judge'):
        cursor.execute(judge_sql, judge_id)
        data = cursor.fetchone()
        add_judge_row(sheet=judge_sheet, data=data, row=judge_row)
        judge_row += 1

    for subjective_id in question_ids.get('subjective'):
        cursor.execute(subjective_sql, subjective_id)
        data = cursor.fetchone()
        add_subjective_row(sheet=subjective_sheet, data=data, row=subjective_row)
        subjective_row += 1
    workbook.save(output_file)
    return

