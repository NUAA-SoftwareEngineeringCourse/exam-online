## 配置说明文档
+ 安装 python 环境 (我用的是 python 3.7)
+ IDE 建议使用 **PyCharm 专业版** 导入。
  > [下载 Pycharm 专业版](https://www.jetbrains.com/pycharm/download/#section=windows)
+ 数据库使用 mysql, 在 `config.py` 中配置数据库的名字与账号密码。

+ 现在去除了 PyCharm 自动配置的虚拟 Python 环境 `venv`, 需要手动配置 python 解释器：
  > File -> Project:xxx -> Project Interpreter   
  > 选择 python.exe 所在的路径即可。


+ 也可以使用 VSCode 进行开发，运行则使用 **PowerShell** 切换到项目所在路径下：
  ```bash
  PS E:\Program Files\PyCharm\workspace\exam-online> python .\app.py
  * Serving Flask app "app" (lazy loading)
  * Environment: production
    WARNING: Do not use the development server in a  production environment.
    Use a production WSGI server instead.
  * Debug mode: on
  * Restarting with stat
  * Debugger is active!
  * Debugger PIN: 263-797-513
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
  ```

+ 如果出现某个库无法 `import`, 例如提示：`can not find/import moudle xxx`，则运行：
  ```bash
  pip install xxx
  ```


## TODO List
- 主线 1
  > 学生查看考试列表 -> 学生参加考试 -> 提交 -> 自动给分 -> 学生查看成绩

  待完成列表：
  - 后台返回学生选择的考试的试卷
  - 提交并自动判分 
  - 后台读写数据库并返回成绩
  - 支持查看自己的答卷情况 (错了那些题目)

- 主线 2 
  > 教师发布考试 -> 学生完成考试 (即完成主线1) -> 教师后台可看见考试数据 (学生答案，成绩分布等)
  
  待完成列表：
  - 后台读写数据库并显示数据
  - 设计数据库存放学生的答案
  - 设计数据库存放学生的成绩

+ 需要特别考虑的地方
  - 教师 - 学生是多对多的关系：学生端并不是返回所有教师发布的考试（因为学生并不一定是某个教师的学生）
  - 各个数据库的关联情况，需要考虑设置外码的问题：
    - user
    - exam_paper
    - teacher_student(记录多对多的联系的表)
    - paper_answer(记录每个学生所完成的每份试卷的答案，未完成)
    - paper_grade(记录每个学生所完成的每份试卷的成绩，未完成)