import os
from os import path

upload_path = 'FilesUpload'
paper_path = 'ExamPapers'
base_path = path.dirname(path.abspath(__file__))
file_dest = path.join(base_path, upload_path)

print(base_path)
print(file_dest)

print('(paper_title, paper_desc, paper_time, paper_date, paper_open, paper_path, paper_userid, paper_class)')
