from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_uploads import configure_uploads, UploadSet
from config import cursor, db_connector
from config import user_table, exam_paper_table, teacher_student_table, exam_paper_columns, student_exam_log_table
from config import choice_question_table, judge_question_table, subjective_question_table
from os import path

import common_helper
import os
import sql_helper
import json

# global path
upload_path = 'FilesUpload'
paper_path = 'ExamPapers'
base_path = path.dirname(path.abspath(__file__))
paper_set = UploadSet(paper_path)
file_dest = path.join(base_path, upload_path)

app = Flask(__name__)

# 配置项
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOADS_DEFAULT_URL'] = 'http://localhost:5000/uploadFile/'
app.config['UPLOADS_DEFAULT_DEST'] = file_dest

# 让上传文件的配置生效
configure_uploads(app, paper_set)


def print_log(name: str, info: str):
    print('[' + name + ']' + '    ' + info)
    return


@app.route('/')
def index():
    user_id = session.get('user_id')
    print_log('index', str(user_id))
    if user_id is not None:
        if user_id[0] == 'T':
            return redirect(url_for('teacherIndex'))
        elif user_id[0] == 'A':
            return redirect(url_for('adminIndex'))
        else:
            return redirect(url_for('studentIndex'))
    else:
        return render_template('index.html')


@app.route('/hello', methods=['GET'])
def hello_world():
    return 'Hello World!'


@app.route('/login/', methods=['GET', 'POST'])
def login():
    print_log('login', request.method)
    if request.method == 'GET':
        return 'login-GET'
    else:
        user_id = str(request.form['UserIDLogin'])
        password = str(request.form['PasswordLogin'])

        query = 'select * from ' + user_table + ' where user_id = %s'
        flag = cursor.execute(query, user_id)
        # flag = 1, 账号正确
        if flag:
            result = cursor.fetchone()
            data = {'success': 1, 'user_id': result.get('user_id'), 'user_name': result.get(
                'user_name'), 'user_type': result.get('user_type')}
            session['user_id'] = data.get('user_id')
            print_log('login', str(data))

            if str(result['user_password']) == password:
                return jsonify(data)
            else:
                data['success'] = 0
                return jsonify(data)
        # flag = 0, 账号错误
        else:
            return jsonify({'success': -1})


@app.route('/check_id/', methods=['GET', 'POST'])
def check_id() -> object:
    if request.method == 'GET':
        return 'checkRegisterStudentID-GET'
    else:
        user_id = request.form['user_id']
        query = 'select * from ' + user_table + ' where user_id = %s'
        flag = cursor.execute(query, user_id)
        return jsonify({'has': flag})


@app.context_processor
def my_context():
    user_id = session.get('user_id') if session.get('user_id') is not None else ''
    if user_id != '':
        sql = 'select user_name, user_type from ' + user_table + ' where `user_id` = %s'
        cursor.execute(sql, user_id)
        result = cursor.fetchone()
        user_name = result.get('user_name')
        user_type = result.get('user_type')
        print_log('my context', str(user_name) + str(user_type) + str(user_id))
        return {'user_id': user_id, 'user_name': user_name, 'user_type': user_type}
    else:
        return {}


@app.route('/register/', methods=['GET', 'POST'])
def register():
    print_log('register', request.method)
    if request.method == 'GET':
        return 'register-GET'
    else:
        user_id = request.form['user_id']
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        password = request.form['password']
        user_type = common_helper.check_type(user_id)
        print_log('register', user_id + ' ' + user_name + ' ' +
                  user_email + ' ' + password + ' ' + user_type)
        sql = 'INSERT INTO ' + user_table + \
              ' VALUES (%s, %s, %s, %s, now(), now(), %s)'
        try:
            flag = cursor.execute(
                sql, (user_id, user_name, user_email, password, user_type))
            db_connector.commit()
        except Exception as e:
            db_connector.rollback()
        return jsonify({'success': flag})


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    session.clear()
    if request.method == 'GET':
        return redirect(url_for('index'))
    return jsonify({'success': 1})


@app.route('/teacherIndex/', methods=['POST', 'GET'])
def teacherIndex():
    print_log('teacherIndex', request.method)
    teacher_id = session.get('user_id')
    if teacher_id is None:
        return '请先登录!'
    elif session.get('user_type') == 'STUDENT':
        return '无权访问教师页面！'

    std_dict = dict({'title': '', 'description': '', 'is_open': 0, 'exam_id': 0,
                     'day': '', 'month': '', 'year': ''})
    print_log('teacherIndex', str(std_dict))
    exam_list = []
    sql = 'select paper_id, paper_title, paper_desc, paper_date, paper_time, paper_open from ' + \
          exam_paper_table + ' where paper_userid=%s'

    cursor.execute(sql, teacher_id)
    results = cursor.fetchall()
    for x in results:
        std_dict['title'] = x.get('paper_title')
        std_dict['description'] = x.get('paper_desc')
        paper_date = x.get('paper_date')
        std_dict['day'] = paper_date.day
        std_dict['month'] = common_helper.month_int2str(paper_date.month)
        std_dict['year'] = paper_date.year
        std_dict['duration'] = x.get('paper_time')
        std_dict['time'] = paper_date.time()
        std_dict['is_open'] = '是' if int(x.get('paper_open')) == 1 else '否'
        std_dict['exam_id'] = x.get('paper_id')
        exam_list.append(dict(std_dict))
    return render_template('teacherIndex.html', exam_list=exam_list)


@app.route('/teacherExam/', methods=['GET', 'POST'])
def teacherExam():
    print_log('teacherExam', request.method)
    return render_template('teacherExam.html')


@app.route('/studentIndex/', methods=['GET', 'POST'])
def studentIndex():
    print_log('studentIndex', request.method)
    student_id = session.get('user_id')
    if student_id is None:
        return '请先登录!'

    std_dict = dict({'title': '', 'description': '', 'day': '', 'year': '',
                     'month': '', 'duration': '', 'time': '', 'teacher': ''})
    print_log('studentIndex', str(std_dict))
    exam_list = []
    sql = 'SELECT * FROM ' + \
          exam_paper_table + ' INNER JOIN ' + teacher_student_table + ' ON exam_paper.paper_id=teacher_student.paper_id ' + \
          'INNER JOIN ' + user_table + ' ON user.user_id=teacher_student.teacher_id ' + \
          'WHERE student_id=%s'
    print_log('student index', sql)
    cursor.execute(sql, session.get('user_id'))
    results = cursor.fetchall()
    for x in results:
        std_dict['title'] = x.get('paper_title')
        std_dict['description'] = x.get('paper_desc')
        date = x.get('paper_date')
        std_dict['day'] = date.day
        std_dict['month'] = common_helper.month_int2str(date.month)
        std_dict['year'] = date.year
        std_dict['duration'] = x.get('paper_time')
        std_dict['time'] = date.time()
        std_dict['teacher'] = x.get('user_name')
        exam_list.append(dict(std_dict))
    return render_template('studentIndex.html', exam_list=exam_list)


@app.route('/studentExam/', methods=['GET', 'POST'])
def studentExam():
    print_log('student exam', request.method)
    exam_dict = {'title': '', 'teacher_name': '', 'date': '', 'duration': 0, 'is_open': 0, 'exam_id': -1}
    exam_list = list()
    # 该学生关联的老师发布的考试
    sql = 'SELECT * FROM ' + \
          exam_paper_table + ' INNER JOIN ' + teacher_student_table + ' ON exam_paper.paper_id=teacher_student.paper_id ' + \
          'INNER JOIN ' + user_table + ' ON user.user_id=teacher_student.teacher_id ' + \
          'WHERE student_id=%s'
    cursor.execute(sql, session.get('user_id'))
    data = cursor.fetchall()

    # 该学生已经完成的考试
    sql = 'SELECT paper_id FROM ' + student_exam_log_table + ' WHERE student_id = %s'
    cursor.execute(sql, session.get('user_id'))
    finished_exam_ids = [x.get('paper_id') for x in cursor.fetchall()]

    exam_order = 1
    for x in data:
        if x.get('paper_id') in finished_exam_ids:
            continue
        d = dict(exam_dict)
        d['title'] = x.get('paper_title')
        d['teacher_name'] = x.get('user_name')
        d['date'] = x.get('paper_date')
        d['duration'] = x.get('paper_time')
        d['is_open'] = x.get('paper_open')
        d['exam_id'] = x.get('paper_id')
        d['order'], exam_order = exam_order, exam_order + 1
        exam_list.append(d)
    return render_template('studentExam.html', exam_list=exam_list)


@app.route('/adminIndex/', methods=['GET', 'POST'])
def adminIndex():
    return render_template('admin.html')


@app.route('/uploadFile/', methods=['POST', 'GET'])
def uploadFile():
    user_id = session.get('user_id')
    if user_id is None:
        return '请先登录！'
    paper_title = request.form.get('exam-title-input')
    paper_desc = request.form.get('exam-desc-input')
    paper_time = request.form.get('exam-time-input')
    paper_date = request.form.get('exam-date-input')
    paper_open = (request.form.get('optionsRadios') == 'open-paper')
    paper_file = request.files['exam-file-input']
    paper_class = request.form.get('exam-class-input')
    print('paper-title', paper_title, type(paper_title))
    print('paper-desc', paper_desc, type(paper_desc))
    print('paper-time', paper_time, type(paper_time))
    print('paper-date', paper_date, type(paper_date))
    print('paper-open', paper_open, type(paper_open))
    print('paper-file', paper_file, type(paper_file))
    print('paper-class', paper_class)

    # 上传文件到项目路径下的 upload_path / paper_path
    paper_set.save(paper_file, name=session.get('user_id') + '-' + paper_title + '.xlsx')

    # 插入 exam_paper 表
    # (paper_title, paper_desc, paper_time, paper_date, paper_open, paper_path, paper_userid)
    file_path = path.join(base_path,
                          upload_path,
                          paper_path,
                          session.get('user_id') + '-' + paper_title + '.xlsx')
    sql = 'insert into ' + exam_paper_table + exam_paper_columns + \
          'values' + '(%s, %s, %s, %s, %s, %s, %s, %s)'
    try:
        cursor.execute(sql, (paper_title, paper_desc, paper_time,
                             paper_date, paper_open, file_path,
                             user_id, paper_class))
        db_connector.commit()
    except Exception as e:
        db_connector.rollback()

    # 获取上面新增试卷的ID
    sql = 'SELECT max(paper_id) FROM ' + exam_paper_table
    cursor.execute(sql)
    paper_id = cursor.fetchone().get('max(paper_id)')

    print_log('upload files', str(paper_id))

    # 在 teacher_student 中建立关联
    for c in paper_class.split(';'):
        if c != '':
            sql = 'SELECT * FROM `user` WHERE user_id LIKE %s'
            cursor.execute(sql, c + '%')
            students = cursor.fetchall()
            for s in students:
                print_log('upload files', s.get('user_id'))
                sql = 'INSERT INTO ' + teacher_student_table + ' VALUES (%s,%s,%s)'
                try:
                    cursor.execute(sql, (user_id, s.get('user_id'), paper_id))
                    db_connector.commit()
                except:
                    db_connector.rollback()

    # 插入试题数据库
    sql_helper.insert_questions(paper_id=paper_id, paper_path=file_path)
    return redirect(url_for('teacherIndex'))


@app.route('/start_exam/', methods=['POST', 'GET'])
def start_exam():
    print_log('start-exam', request.method + request.args.get('exam_id'))

    exam_id = request.args.get('exam_id')
    sql = 'SELECT * FROM ' + exam_paper_table + ' WHERE paper_id=%s'
    cursor.execute(sql, str(exam_id))
    data = cursor.fetchone()

    sql2 = 'SELECT user_name FROM ' + user_table + ' WHERE user_id=%s'
    cursor.execute(sql2, data.get('paper_userid'))
    data2 = cursor.fetchone()

    question = common_helper.parse_paper(data.get('paper_path'))
    exam = {'exam_id': exam_id, 'title': data.get('paper_title'),
            'duration': data.get('paper_time'), 'teacher': data2.get('user_name')}
    return render_template('exam.html', question=question, exam=exam)


@app.route('/submit_paper/', methods=['POST', 'GET'])
def submit_paper():
    print_log('submit-paper', request.method)
    answers = request.form['answers']
    exam_id = request.form['exam_id']

    print_log('submit paper', answers + ' ' + str(type(answers)))
    print_log('submit paper', exam_id)

    sql = 'SELECT * FROM ' + exam_paper_table + ' WHERE paper_id = %s'
    cursor.execute(sql, exam_id)
    data = cursor.fetchone()
    # 单选题、多选题、判断题判分
    grade, full_grade = common_helper.compare_answer(json.loads(answers), data.get('paper_path'))
    print_log('submit paper', 'grade = ' + str(grade))
    print_log('submit paper', 'full grade = ' + str(full_grade))
    # 写入数据库
    sql = 'INSERT INTO ' + student_exam_log_table + ' VALUES (%s, %s, %s, %s, %s, -1, now())'
    print_log('submit paper', 'sql = ' + sql)
    try:
        cursor.execute(sql, (exam_id, session.get('user_id'), str(answers), grade, full_grade))
        db_connector.commit()
    except:
        db_connector.rollback()
    return jsonify({'success': 1})


@app.route('/student_history/', methods=['POST', 'GET'])
def student_history():
    print_log('student history', request.method)
    student_id = session.get('user_id')
    history_list = list()
    std_dict = dict({'order': 0, 'title': '', 'teacher': '', 'date': '',
                     'duration': '', 'grade': 0, 'full_grade': 100, 'subjective_grade': 0,
                     'exam_id': -1})
    # 三个表进行 INNER JOIN, 👴就是一个 sql 工具人
    sql = 'SELECT student_exam_log.paper_id, grade, full_grade, subjective_grade, paper_title, paper_time, paper_date, user_name FROM ' + \
          '(student_exam_log INNER JOIN exam_paper ON student_exam_log.`paper_id`=exam_paper.`paper_id`) ' + \
          ' INNER JOIN `user` ON user.`user_id`=exam_paper.`paper_userid` ' + \
          ' WHERE student_exam_log.student_id = %s'
    cursor.execute(sql, student_id)
    data = cursor.fetchall()

    order = 1
    for x in data:
        d = dict(std_dict)
        d['order'], order = order, order + 1
        d['title'] = x.get('paper_title')
        d['teacher'] = x.get('user_name')
        d['date'] = x.get('paper_date').date()
        d['duration'] = x.get('paper_time')
        d['grade'] = x.get('grade')
        d['full_grade'] = x.get('full_grade')
        d['exam_id'] = x.get('paper_id')
        d['subjective_grade'] = x.get('subjective_grade') if x.get('subjective_grade') != -1 else '未发布'
        history_list.append(d)
    return render_template('studentHistory.html', exam_history=history_list)


@app.route('/student_help/', methods=['GET', 'POST'])
def student_help():
    return render_template('studentHelp.html')


@app.route('/teacher_modify/', methods=['POST', 'GET'])
def teacher_modify():
    print_log('teacher modify', request.method)
    std_exam_dict = dict(exam_id='', exam_title='', exam_date='', student_submit_exam_list=[])
    std_submit_exam_dict = dict(student_id=0, student_name='', submit_time='', grade=100, subjective_grade=-1)
    exam_list = []

    sql = 'SELECT * FROM ' + exam_paper_table + ' WHERE paper_userid=%s'
    cursor.execute(sql, session.get('user_id'))
    data = cursor.fetchall()
    for exam in data:
        exam_dict = dict(std_exam_dict)
        exam_dict['exam_id'] = exam.get('paper_id')
        exam_dict['exam_title'] = exam.get('paper_title')
        exam_dict['exam_date'] = exam.get('paper_date')

        submit_list = []
        sql = 'SELECT * FROM ' + student_exam_log_table + ' INNER JOIN ' + user_table + \
              'ON student_exam_log.student_id=user.user_id ' + \
              'WHERE paper_id=%s'
        cursor.execute(sql, exam.get('paper_id'))
        for submit_log in cursor.fetchall():
            submit_dict = dict(std_submit_exam_dict)
            submit_dict['student_name'] = submit_log.get('user_name')
            submit_dict['student_id'] = submit_log.get('user_id')
            submit_dict['submit_time'] = submit_log.get('submit_time')
            submit_dict['grade'] = submit_log.get('grade')
            submit_dict['subjective_grade'] = submit_log.get('subjective_grade')
            submit_list.append(submit_dict)

        exam_dict['student_submit_exam_list'] = submit_list
        exam_list.append(exam_dict)

    return render_template('teacherModify.html', exam_list=exam_list)


@app.route('/teacher_check_paper', methods=['GET', 'POST'])
def teacher_check_paper():
    # 这个函数跟学生的 show_answers() 逻辑是一样的
    print_log('teacher check paper', request.method)

    # 提取GET方法的参数
    paper_id = request.args.get('paper_id')
    student_id = request.args.get('student_id')
    student_name = request.args.get('student_name')

    # 找到试卷文件，并提取出试题和正确答案
    sql = 'SELECT paper_path FROM ' + exam_paper_table + 'WHERE paper_id=%s'
    cursor.execute(sql, paper_id)
    path = cursor.fetchone().get('paper_path')
    std_ans = common_helper.get_std_answers(path)
    question = common_helper.parse_paper(path)

    # 找到学生选择的试卷的答案
    sql = 'SELECT answer_json FROM ' + student_exam_log_table + \
          'WHERE student_id=%s and paper_id=%s'
    cursor.execute(sql, (student_id, paper_id))
    answers = json.loads(cursor.fetchone().get('answer_json'))

    for i in range(0, len(question)):
        question[i]['std_ans'] = std_ans[str(i)]
        if answers.get(str(i)) is None:
            continue
        if question[i].get('q_type') == 'checkbox':
            is_correct = set(answers[str(i)]) == set(std_ans[str(i)])
        else:
            is_correct = answers[str(i)] == std_ans[str(i)]
        question[i]['is_correct'] = is_correct
        question[i]['selected'] = answers[str(i)]

    # 找到试卷相关信息
    sql = 'SELECT * FROM ' + \
          exam_paper_table + 'INNER JOIN' + user_table + 'ON user.user_id=exam_paper.paper_userid ' + \
          'WHERE paper_id=%s'
    cursor.execute(sql, paper_id)
    data = cursor.fetchone()
    exam = {'title': data.get('paper_title'), 'exam_id': paper_id, 'teacher': data.get('user_name'),
            'duration': data.get('paper_time')}

    return render_template('teacher-check-paper.html', question=question, exam=exam,
                           student=dict(student_name=student_name, student_id=student_id))


@app.route('/teacher_submit_grade', methods=['POST', 'GET'])
def teacher_submit_grade():
    print_log('teacher submit grade', request.method)
    paper_id = request.form['paper_id']
    student_id = request.form['student_id']
    subjective_grade = request.form['subjective_grade']
    print_log('teacher submit grade', str(paper_id) + ' ' + str(student_id) + ' ' + str(subjective_grade))

    sql = 'UPDATE ' + student_exam_log_table + ' SET subjective_grade=%s ' + \
          'WHERE paper_id=%s AND student_id=%s'
    try:
        cursor.execute(sql, (subjective_grade, paper_id, student_id))
        db_connector.commit()
    except:
        db_connector.rollback()

    return redirect(url_for('teacher_modify'))


@app.route('/teacher_result/', methods=['POST', 'GET'])
def teacher_result():
    # std_student_dict = {'user_name': '', 'student_id': '', 'grade': 0}
    std_paper_dict = {'name': '', 'paper_id': -1, 'student_num': '', 'avg_grade': 0, 'student_list': [],
                      'grade_segment': {}}
    paper_list = []

    # 查询该教师发布的考试
    sql = 'SELECT paper_id, paper_title FROM ' + exam_paper_table + ' WHERE paper_userid=%s'
    cursor.execute(sql, session.get('user_id'))
    published_exams = cursor.fetchall()

    for exam in published_exams:
        paper_dict = dict(std_paper_dict)
        # 已完成该考试的学生列表
        student_list = sql_helper.get_students_by_paperid(exam.get('paper_id'))

        # 如果 student_list 为空，没有学生参加考试，则不显示
        if student_list is None or len(student_list) == 0:
            continue

        paper_dict['name'] = exam.get('paper_title')
        paper_dict['paper_id'] = exam.get('paper_id')
        paper_dict['student_num'] = len(student_list)
        paper_dict['avg_grade'] = sum([int(x.get('grade')) for x in student_list]) / paper_dict['student_num']
        paper_dict['student_list'] = student_list
        paper_dict['grade_segment'] = common_helper.get_grade_segment(student_list)
        paper_list.append(paper_dict)

    return render_template('teacherResult.html', paper_list=paper_list)


@app.route('/show_answers/', methods=['POST', 'GET'])
def show_answers():
    # 获取 get 方法的参数
    exam_id = request.args.get('exam_id')
    student_id = request.args.get('student_id')

    # 找到试卷文件，并提取出试题和正确答案
    sql = 'SELECT paper_path FROM ' + exam_paper_table + \
          'WHERE paper_id=%s'
    cursor.execute(sql, exam_id)
    path = cursor.fetchone().get('paper_path')
    std_ans = common_helper.get_std_answers(path)
    question = common_helper.parse_paper(path)

    # 找到学生选择的试卷的答案
    sql = 'SELECT answer_json FROM ' + student_exam_log_table + \
          'WHERE student_id=%s and paper_id=%s'
    cursor.execute(sql, (student_id, exam_id))
    answers = json.loads(cursor.fetchone().get('answer_json'))

    print(answers, len(answers))
    print(std_ans, len(std_ans))
    print(len(question))

    for i in range(0, len(question)):
        question[i]['std_ans'] = std_ans[str(i)]
        if answers.get(str(i)) is None:
            continue
        if question[i].get('q_type') == 'checkbox':
            is_correct = set(answers[str(i)]) == set(std_ans[str(i)])
        else:
            is_correct = answers[str(i)] == std_ans[str(i)]
        question[i]['is_correct'] = is_correct
        question[i]['selected'] = answers[str(i)]

    # 找到试卷相关信息
    sql = 'SELECT * FROM ' + \
          exam_paper_table + 'INNER JOIN' + user_table + 'ON user.user_id=exam_paper.paper_userid ' + \
          'WHERE paper_id=%s'
    cursor.execute(sql, exam_id)
    data = cursor.fetchone()
    exam = {'title': data.get('paper_title'), 'exam_id': exam_id, 'teacher': data.get('user_name'),
            'duration': data.get('paper_time')}

    return render_template('show-answers.html', question=question, exam=exam)


@app.route('/preview_paper/', methods=['POST', 'GET'])
def previwe_paper():
    print_log('preview paper', request.method)

    exam_id = request.args.get('exam_id')
    teacher_id = session.get('user_id')

    sql = 'SELECT paper_path, paper_title, paper_time, paper_date FROM ' + \
          exam_paper_table + ' INNER JOIN ' + user_table + ' ON exam_paper.paper_userid=user.user_id ' + \
          'WHERE paper_id=%s and paper_userid=%s'
    cursor.execute(sql, (exam_id, teacher_id))
    data = cursor.fetchone()
    exam_dict = {'title': data.get('paper_title'), 'exam_id': exam_id, 'duration': data.get('paper_time'),
                 'date': data.get('paper_date')}
    return render_template('preview-paper.html',
                           question=common_helper.parse_paper(data.get('paper_path')),
                           exam=exam_dict)


'''
leo's code begin
'''


@app.route('/admin_userlist/', methods=['GET', 'POST'])
def admin_userlist():
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
    return render_template('admin-userlist.html', user_list=user_list)


@app.route('/admin_examlist/', methods=['GET', 'POST'])
def admin_examlist():
    exam_list = list()
    exam_dict = {'exam_id:': '', 'exam_title': '', 'teacher': '', 'exam_date': ''}
    sql = 'SELECT paper_title,paper_id,paper_date,user_name,paper_time,paper_class FROM exam_paper inner join user on user_id=paper_userid'
    cursor.execute(sql)
    data = cursor.fetchall()
    for x in data:
        e = dict(exam_dict)
        e['exam_id'] = x.get('paper_id')
        e['exam_title'] = x.get('paper_title')
        e['teacher'] = x.get('user_name')
        e['exam_date'] = x.get('paper_date')
        e['exam_duration'] = x.get('paper_time')
        e['exam_class'] = x.get('paper_class')
        exam_list.append(e)
    return render_template('admin-examlist.html', exam_list=exam_list)


@app.route('/deleteUser', methods=['GET', 'POST'])
def deleteUser():
    if request.method == 'GET':
        return 'register-GET'
    else:
        user_id = request.form['user_id']
        sql = ' DELETE FROM ' + user_table + ' WHERE user_id = ' + user_id
        try:
            flag = cursor.execute(sql)
            db_connector.commit()
        except Exception as e:
            db_connector.rollback()
    return jsonify({'success': flag})


@app.route('/deleteExam', methods=['GET', 'POST'])
def deleteExam():
    if request.method == 'GET':
        return 'register-GET'
    else:
        exam_id = request.form['exam_id']
        print(exam_id)
        sql = ' DELETE FROM exam_paper WHERE paper_id = ' + exam_id
        try:
            flag = cursor.execute(sql)
            db_connector.commit()
        except Exception as e:
            db_connector.rollback()
    return jsonify({'success': flag})


@app.route('/admin_createUser/', methods=['POST', 'GET'])
def admin_createUser():
    return render_template('admin-create.html')


# leo's code: personal info
@app.route('/teacher_personal_info/', methods=['GET', 'POST'])
def teacher_personal_info():
    user_id = session.get('user_id')
    sql = 'SELECT * FROM user WHERE user_id = \'' + user_id + '\' '

    user_dict = {'user_id:': '', 'user_name': '', 'user_email': ''}

    cursor.execute(sql)
    userdata = cursor.fetchall()
    u = dict(user_dict)
    u['user_id'] = userdata[0].get('user_id')
    u['user_name'] = userdata[0].get('user_name')
    u['user_email'] = userdata[0].get('user_email')
    return render_template('teacher-personInfo.html', person=u)


@app.route('/student_personal_info/', methods=['POST', 'GET'])
def student_personal_info():
    user_id = session.get('user_id')
    sql = 'SELECT * FROM ' + user_table + ' WHERE user_id=%s'
    cursor.execute(sql, user_id)
    data = cursor.fetchone()
    u = dict()
    u['user_id'] = user_id
    u['user_name'] = data.get('user_name')
    u['user_email'] = data.get('user_email')
    return render_template('student-personInfo.html', person=u)


@app.route('/modifyPwd/', methods=['POST', 'GET'])
def modifyPwd():
    user_id = session.get('user_id')
    if user_id is None:
        return '请先登录！'

    sql = 'SELECT * FROM user WHERE user_id = \'' + user_id + '\' '
    cursor.execute(sql)
    userdata = cursor.fetchall()
    password = userdata[0].get('user_password')

    oldpwd = request.form.get('old_pwd')
    newpwd = request.form.get('new_pwd')
    conpwd = request.form.get('con_pwd')

    if password != oldpwd:
        return '原密码不正确！'
    if newpwd != conpwd:
        return '确认密码不一致！'
    if len(newpwd) < 8:
        return '密码长度不足8位！'
    sql = 'update user set user_password = \'' + newpwd + '\'  where user_id = \'' + user_id + '\' '
    cursor.execute(sql)
    if user_id[0] == 'T':
        return redirect(url_for('teacher_personal_info'))
    else:
        return redirect(url_for('student_personal_info'))


@app.route('/admin_add_user/', methods=['GET', 'POST'])
def admin_add_user():
    name = request.args.get('uname')
    id = request.args.get('id')
    pwd = request.args.get('pwd')
    role = request.args.get('role')
    print_log('admin add user', str(name) + str(id) + str(role))
    return redirect(url_for('adminIndex'))


# 增加从题库生成试卷的功能
@app.route('/generate_paper/', methods=['GET', 'POST'])
def generate_paper():
    questions = request.form.get('selected_questions')
    exam_title = request.form.get('exam_title')
    exam_tips = request.form.get('exam_tips')
    exam_duration = request.form.get('exam_duration')
    exam_datetime = request.form.get('exam_datetime')
    exam_class = request.form.get('exam_class')
    print_log('generate paper', str(questions))
    print(exam_title, exam_tips, exam_duration, exam_datetime, exam_class)

    output = os.path.join(file_dest, session.get('user_id') + '-' + exam_title + '.xls')
    common_helper.write_paper_file(question_ids=questions, output_file=output)

    sql = 'INSERT INTO ' + exam_paper_table + exam_paper_columns + \
          'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    try:
        cursor.execute(sql, (
            exam_title, exam_tips, exam_duration, exam_datetime, 0, output, session.get('user_id'), exam_class))
        db_connector.commit()
    except:
        db_connector.rollback()

    # 在 teacher_student 中建立关联
    for c in exam_class.split(';'):
        # TODO
        print('<><><待完成><><>')
        print(c)
        print('<><><><><>')
    return jsonify({'success': 1})


@app.route('/get_questions/', methods=['GET', 'POST'])
def get_questions():
    keyword = request.args.get('keyword')
    print_log('get questions', str(keyword))
    if keyword is None or keyword == '':
        return render_template('teacherQuestion.html')

    sql = 'SELECT paper_id FROM ' + exam_paper_table + ' WHERE paper_title LIKE "%' + keyword + '%"'
    choice_sql = 'SELECT * FROM ' + choice_question_table + 'WHERE q_paperid=%s'
    judge_sql = 'SELECT * FROM ' + judge_question_table + 'WHERE q_paperid=%s'
    subjective_sql = 'SELECT * FROM ' + subjective_question_table + 'WHERE q_paperid=%s'
    cursor.execute(sql)
    paper_ids = [x.get('paper_id') for x in cursor.fetchall()]
    print(paper_ids)

    choice_list, judge_list, subjective_list = [], [], []

    for pid in paper_ids:
        cursor.execute(choice_sql, pid)
        for q in cursor.fetchall():
            choice_list.append(q)
        cursor.execute(judge_sql, pid)
        for q in cursor.fetchall():
            judge_list.append(q)
        cursor.execute(subjective_sql, pid)
        for q in cursor.fetchall():
            subjective_list.append(q)
    return render_template('teacherQuestion.html', choice_list=choice_list, judge_list=judge_list,
                           subjective_list=subjective_list)


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000)
