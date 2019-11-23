from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_uploads import configure_uploads, UploadSet, IMAGES
from config import cursor, db_connector
from os import path
import helper
import os
import time


paper_set = UploadSet('paper')
file_dest = path.join(path.dirname(path.abspath(__file__)), "upload-files")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOADS_DEFAULT_URL'] = 'http://localhost:5000/uploadFile/'
app.config['UPLOADS_DEFAULT_DEST'] = file_dest

# 让上传文件的配置生效
configure_uploads(app, paper_set)


# global table names
user_table = 'user'


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
            data = {'success': 1, 'user_id': result.get('user_id'), 'user_name': result.get('user_name'), 'user_type': result.get('user_type')}
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
    user_id = session.get('user_id') if session.get('user_id') is not None else ''
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
        print_log('register', user_id + ' ' + user_name + ' ' + user_email + ' ' + password + ' ' + user_type)
        sql = 'INSERT INTO ' + user_table + ' VALUES (%s, %s, %s, %s, now(), now(), %s)'
        try:
            flag = cursor.execute(sql, (user_id, user_name, user_email, password, user_type))
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


@app.route('/result/', methods=['GET', 'POST'])
def result():
    return 'result'


@app.route('/teacherIndex/', methods=['POST', 'GET'])
def teacherIndex():
    print_log('teacherIndex', request.method)
    # if session.get('user_id') is None:
    #     return '请先登录!'
    std_dict = dict({'title': 'Exam-Title', 'description': 'Exam-Desc', 'day': 'Day', 'month': 'Month'})
    print_log('teacherIndex', str(std_dict))
    exam_list = [
        dict({'title': '编译原理', 'description': '编译原理', 'day': 23, 'month': 'Nov'}),
        dict({'title': '概率论', 'description': '概率论', 'day': 24, 'month': 'Nov'}),
        dict({'title': '高等数学', 'description': '高等数学', 'day': 25, 'month': 'Dec'})
    ]
    return render_template('teacherIndex.html', exam_list=exam_list)


@app.route('/teacherExam/', methods=['GET', 'POST'])
def teacherExam():
    print_log('teacherExam', request.method)
    return render_template('teacherExam.html')


@app.route('/studentIndex/', methods=['GET', 'POST'])
def studentIndex():
    print_log('studentIndex', request.method)
    if session.get('user_id') is None:
        return '请先登录!'
    std_dict = dict({'title': 'Exam-Title', 'description': 'Exam-Desc', 'day': 'Day', 'month': 'Month'})
    print_log('teacherIndex', str(std_dict))
    exam_list = [
        dict({'title': '编译原理', 'description': '编译原理', 'day': 23, 'month': 'Nov'}),
        dict({'title': '概率论', 'description': '概率论', 'day': 24, 'month': 'Nov'}),
        dict({'title': '高等数学', 'description': '高等数学', 'day': 25, 'month': 'Dec'})
    ]
    return render_template('studentIndex.html', exam_list=exam_list)


@app.route('/studentExam/', methods=['GET', 'POST'])
def studentExam():
    print_log('studentExam', request.method)
    return render_template('studentExam.html')


@app.route('/adminIndex/', methods=['GET', 'POST'])
def adminIndex():
    time_str = str(time.asctime(time.localtime(time.time())))
    data = [dict(user_name='sin', paper_name='math', exam_grade=100, create_time=time_str),
            dict(user_name='kin', paper_name='chinese', exam_grade=100, create_time=time_str),
            dict(user_name='ben', paper_name='english', exam_grade=100, create_time=time_str)]
    return render_template('admin.html', user_grade_data=data)


@app.route('/uploadFile/', methods=['POST', 'GET'])
def uploadFile():
    if session.get('user_id') is None:
        return '请先登录！'
    paper_title = request.form.get('exam-title-input')
    paper_desc = request.form.get('exam-desc-input')
    paper_time = request.form.get('exam-time-input')
    paper_date = request.form.get('exam-date-input')
    paper_open = request.form.get('optionsRadios')
    paper_file = request.files['exam-file-input']
    print('paper-title', paper_title, type(paper_title))
    print('paper-desc', paper_desc, type(paper_desc))
    print('paper-time', paper_time, type(paper_time))
    print('paper-date', paper_date, type(paper_date))
    print('paper-open', paper_open, type(paper_open))
    print('paper-file', paper_file, type(paper_file))

    # 上传文件到项目路径下的 paper-files
    paper_set.save(paper_file, name=paper_title + '.docx')

    return redirect(url_for('teacherIndex'))


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000)
