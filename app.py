from flask import Flask, render_template, request, jsonify, session
from config import cursor, db_connector
import helper
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径


# global table names
user_table = 'user'


def print_log(name: str, info: str):
    print('[' + name + ']' + '    ' + info)
    return


@app.route('/')
def index():
    return render_template('index.html')


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
        return {'id': user_id, 'name': user_name, 'type': user_type}
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


@app.route('/logout/', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': 1})


@app.route('/result/', methods=['GET', 'POST'])
def result():
    return 'result'


@app.route('/teacher/', methods=['POST', 'GET'])
def teacher():
    print_log('teacher', request.method)
    return render_template('teacher.html')


@app.route('/student/', methods=['GET', 'POST'])
def student():
    print_log('student', request.method)
    return render_template('student.html')


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000)
