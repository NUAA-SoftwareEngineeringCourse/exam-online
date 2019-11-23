from config import cursor, exam_paper_table, user_table
from datetime import datetime

sql = 'SELECT paper_title, paper_desc, paper_date, user_name FROM ' + user_table + ' INNER JOIN ' \
      + exam_paper_table + ' ON ' + exam_paper_table + '.paper_userid='+user_table+'.user_id'

cursor.execute(sql)

data = cursor.fetchall()
for x in data:
    print(x)