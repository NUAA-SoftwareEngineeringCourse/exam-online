import pymysql
db_connector = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    db='SinWeb',
    user='root',
    password='',
    charset='utf8'
)

cursor = db_connector.cursor(cursor=pymysql.cursors.DictCursor)

# Sample for insert and select
'''
query = 'select * from user where user_id =\'161630231\' '
flag = cursor.execute(query)
if flag:
    data = cursor.fetchall()
    for x in data:
        print(x)
    print(flag)
else:
    print(flag)

sql = 'insert into user values (%s, %s, %s, %s, now(), now())'
try:
    flag = cursor.execute(sql, ('161630229', '王珊月', 'wang@qq.com', '161630229'))
    db_connector.commit()
except Exception as e:
    db_connector.rollback()
print(flag)
'''

