from config import db_connector, cursor

sql = 'select * from exam_paper'

cursor.execute(sql)
data = cursor.fetchone()
print(data['paper_date'])