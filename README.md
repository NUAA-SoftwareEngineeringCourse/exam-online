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
  **访问域名请使用：`http://localhost:5000`，请勿使用 `http://127.0.0.1:5000/`**。

+ 如果出现某个库无法 `import`, 例如提示：`can not find/import moudle xxx`，则运行：
  ```bash
  pip install xxx
  ```

+ 数据库建立  
  此处未经过测试，该 sql 脚本由 `mysqldump` 导出。
  > mysqldump.exe -u root -p sinweb > sinweb.sql  
  
  `exam_paper` 的 `paper_path` 字段存储上传文件的路径，使用的是绝对路径，请修改为 **你电脑上的相应绝对路径** 。
  然后把 `exam-online/Test-xxx.xlsx` 拷贝到数据库中的目录下，**注意根据数据库修改文件名**。
  ```bash
  cd exam-online/mysql/
  mysql -u xxx -p
  use xxx(your database name)
  source sinweb.sql 
  ```


## TODO List
- 其他需要完善的细节
  - ✔在学生考试页面添加**倒计时**功能。
  - ✔主观题页面。
  - ✔学生个人资料页面。
  - ✔在 `exam_paper` 中加入字段 `paper_id`。
  - ✔教师考试定时开放，未到规定时间，学生禁止进入该场考试的页面 (开放后 15 min 允许进入考试)。
  - ✔增加 “从题库中选取题目并组合为试卷” 的功能。
  - 教师功能：成绩单导出成为一个 Excel ，包含排名等信息。
 
- 需要修正的地方
  - ✔管理员：批量导入用户和试题
  - 管理员：提供题库的增删改查（新增一个专门的页面）
  - ✔管理员：导入单个题目（点击”添加XX题“，通过浮窗的形式填写信息）
  - ✔教师：从题库中生成试卷，前端需要优化，增加"修改某个试题"的功能。

   