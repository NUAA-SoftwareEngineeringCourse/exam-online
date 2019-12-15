from config import db_connector, cursor

s = '1616302;1616303;1616404;'

for x in s.split(';'):
    if x != '':
       sql = 'SELECT * FROM USER WHERE user_id LIKE %s'
       cursor.execute(sql, x+'%')
       data = cursor.fetchall()
       for d in data:
           print(d)
       print('------------')