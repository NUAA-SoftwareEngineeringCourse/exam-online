from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_uploads import configure_uploads, UploadSet
from config import cursor, db_connector
from config import user_table, exam_paper_table, teacher_student_table, exam_paper_columns, student_exam_log_table
from os import path

import common_helper
import os
import time
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
    if session.get('user_type') is not None:
        if session.get('user_type') == 'STUDENT':
            return redirect(url_for('studentIndex'))
        if session.get('user_type') == 'TEACHER':
            return redirect(url_for('teacherIndex'))
    else:
        return render_template('index-bak.html')


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
    print_log('my_context', '')
    user_id = session.get('user_id') if session.get(
        'user_id') is not None else ''
    if user_id != '':
        sql = 'select user_name, user_type from ' + user_table + ' where `user_id` = %s'
        cursor.execute(sql, user_id)
        result = cursor.fetchone()
        user_name = result.get('user_name')
        user_type = result.get('user_type')
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


@app.route('/exam_result/', methods=['GET', 'POST'])
def exam_result():
    time_str = str(time.asctime(time.localtime(time.time())))
    user_grade = [dict(paper_name='Math-Paper', exam_grade=100, create_time=time_str),
                  dict(paper_name='Chinese-Paper', exam_grade=100, create_time=time_str),
                  dict(paper_name='English-Paper', exam_grade=100, create_time=time_str)]
    return render_template('results.html', user_grade=user_grade)


@app.route('/teacherIndex/', methods=['POST', 'GET'])
def teacherIndex():
    print_log('teacherIndex', request.method)
    teacher_id = session.get('user_id')
    if teacher_id is None:
        return '请先登录!'

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
    sql = 'SELECT paper_title, paper_desc, paper_date, user_name, paper_time FROM ' + \
          exam_paper_table + ' INNER JOIN ' + user_table + ' ON user.user_id=exam_paper.paper_userid ' + \
          'WHERE paper_userid IN ' + \
          '(SELECT teacher_id FROM ' + teacher_student_table + ' WHERE student_id=%s)'
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
    # 该学生关联的老师发布的所有考试
    sql = 'SELECT paper_title, user_name, paper_date, paper_time, paper_open, paper_id FROM ' + \
          exam_paper_table + ' INNER JOIN ' + user_table + ' ON user.user_id=exam_paper.paper_userid ' + \
          'WHERE paper_userid IN ' + \
          '(SELECT teacher_id FROM ' + teacher_student_table + ' WHERE student_id=%s)'
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
    time_str = str(time.asctime(time.localtime(time.time())))
    data = [dict(user_name='sin', paper_name='math', exam_grade=100, create_time=time_str),
            dict(user_name='kin', paper_name='chinese',
                 exam_grade=100, create_time=time_str),
            dict(user_name='ben', paper_name='english', exam_grade=100, create_time=time_str)]
    return render_template('admin.html', user_grade_data=data)


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
    print('paper-title', paper_title, type(paper_title))
    print('paper-desc', paper_desc, type(paper_desc))
    print('paper-time', paper_time, type(paper_time))
    print('paper-date', paper_date, type(paper_date))
    print('paper-open', paper_open, type(paper_open))
    print('paper-file', paper_file, type(paper_file))

    # 上传文件到项目路径下的 upload_path / paper_path
    paper_set.save(paper_file, name=session.get('user_id') + '-' + paper_title + '.xlsx')

    # 插入 exam_paper 表
    # (paper_title, paper_desc, paper_time, paper_date, paper_open, paper_path, paper_userid)
    file_path = path.join(base_path,
                          upload_path,
                          paper_path,
                          session.get('user_id') + '-' + paper_title + '.xlsx')
    sql = 'insert into ' + exam_paper_table + exam_paper_columns + \
          'values' + '(%s, %s, %s, %s, %s, %s, %s)'
    try:
        cursor.execute(sql, (paper_title, paper_desc, paper_time,
                             paper_date, paper_open, file_path, user_id))
        db_connector.commit()
    except Exception as e:
        db_connector.rollback()

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
    sql = 'INSERT INTO ' + student_exam_log_table + ' VALUES (%s, %s, %s, %s, %s)'
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
                     'duration': '', 'grade': 0, 'full_grade': 100,
                     'exam_id': -1})
    # 三个表进行 INNER JOIN, 👴就是一个 sql 工具人
    sql = 'SELECT student_exam_log.paper_id, grade, full_grade, paper_title, paper_time, paper_date, user_name FROM ' + \
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
        history_list.append(d)
    return render_template('studentHistory.html', exam_history=history_list)


@app.route('/student_help/', methods=['GET', 'POST'])
def student_help():
    return render_template('studentHelp.html')


@app.route('/teacher_modify/', methods=['POST', 'GET'])
def teacher_modify():
    paper = dict({'pid': '1234',
                  'pname': '高等数学',
                  'teaname': '王力',
                  'prolist': '123',
                  'stulist': '456',
                  'submitted': '789'})
    ans = dict({'paperid': 12, 'stuid': '161630230', 'submit_time': '2019/12/01-19:00',
                'keguan_grade': 80, 'zhuguan_grade': 90,
                'confirmed': True})
    return render_template('teacherModify.html', paper=paper, ans=ans)


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
    return render_template('preview-paper.html', question=common_helper.parse_paper(data.get('paper_path')),
                           exam=exam_dict)


@app.route('/zhuguanti/', methods=['POST', 'GET'])
def zhuguanti():
    return render_template('zhuguanti.html')


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
    sql = 'SELECT paper_title,paper_id,paper_date,user_name FROM exam_paper inner join user on user_id=paper_userid'
    cursor.execute(sql)
    data = cursor.fetchall()
    for x in data:
        e = dict(exam_dict)
        e['exam_id'] = x.get('paper_id')
        e['exam_title'] = x.get('paper_title')
        e['teacher'] = x.get('user_name')
        e['exam_date'] = x.get('paper_date')
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


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000)
