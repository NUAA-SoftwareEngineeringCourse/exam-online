from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_uploads import configure_uploads, UploadSet
from config import cursor, db_connector
from config import user_table, exam_paper_table, exam_paper_columns
from os import path
import helper
import os
import time


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
        user_type = helper.check_type(user_id)
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
    std_dict = dict({'title': 'Exam-Title',
                     'description': 'Exam-Desc', 'day': 'Day', 'month': 'Month'})
    print_log('teacherIndex', str(std_dict))
    exam_list = []
    sql = 'select paper_title, paper_desc, paper_date, paper_time from ' + \
        exam_paper_table + ' where paper_userid=%s'

    cursor.execute(sql, teacher_id)
    results = cursor.fetchall()
    for x in results:
        std_dict['title'] = x.get('paper_title')
        std_dict['description'] = x.get('paper_desc')
        paper_date = x.get('paper_date')
        std_dict['day'] = paper_date.day
        std_dict['month'] = helper.month_int2str(paper_date.month)
        std_dict['duration'] = x.get('paper_time')
        std_dict['time'] = paper_date.time()
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
    std_dict = dict({'title': '', 'description': '', 'day': '',
                     'month': '', 'duration': '', 'time': '', 'teacher': ''})
    print_log('studentIndex', str(std_dict))
    exam_list = []
    sql = 'select paper_title, paper_desc, paper_date, user_name, paper_time from ' + user_table + ' inner join ' \
          + exam_paper_table + ' on ' + exam_paper_table + \
        '.paper_userid=' + user_table + '.user_id'
    cursor.execute(sql)
    results = cursor.fetchall()
    for x in results:
        std_dict['title'] = x.get('paper_title')
        std_dict['description'] = x.get('paper_desc')
        date = x.get('paper_date')
        std_dict['day'] = date.day
        std_dict['month'] = helper.month_int2str(date.month)
        std_dict['duration'] = x.get('paper_time')
        std_dict['time'] = date.time()
        std_dict['teacher'] = x.get('user_name')
        exam_list.append(dict(std_dict))
    return render_template('studentIndex.html', exam_list=exam_list)


@app.route('/studentExam/', methods=['GET', 'POST'])
def studentExam():
    print_log('studentExam', request.method)
    return render_template('studentExam.html')


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
    paper_set.save(paper_file, name=paper_title + '.xlsx')

    # 插入 exam_paper 表
    # (paper_title, paper_desc, paper_time, paper_date, paper_open, paper_path, paper_userid)
    file_path = path.join(base_path, upload_path,
                          paper_path, paper_title + '.xlsx')
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
    print_log('start-exam', request.method)
    return render_template('exam.html', question=helper.parse_paper('Test.xlsx'))


@app.route('/submit_paper/', methods=['POST', 'GET'])
def submit_paper():
    print_log('submit-paper', request.method)
    answers = request.form['answers']
    print(answers)
    return jsonify({'success': 1})


@app.route('/student_history/', methods=['POST', 'GET'])
def student_history():
    return render_template('studentHistory.html')


@app.route('/student_help/', methods=['GET', 'POST'])
def student_help():
    return render_template('studentHelp.html')


@app.route('/teacher_modify/', methods=['POST', 'GET'])
def teacher_modify():
    return render_template('teacherModify.html')


@app.route('/teacher_result/', methods=['POST', 'GET'])
def teacher_result():
    return render_template('teacherResult.html')


@app.route('/zhuguanti/', methods=['POST', 'GET'])
def zhuguanti():
    return render_template('zhuguanti.html')


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000)
