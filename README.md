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

  ```bash
  cd exam-online/mysql/
  mysql -u xxx -p
  use xxx(your database name)
  source xxx.sql(每个sql文件都执行一次，需要考虑外码依赖问题并决定执行顺序)
  ```


## TODO List
- 主线 1
  > 学生查看考试列表 -> 学生参加考试 -> 提交 -> 自动给分 -> 学生查看成绩

  待完成列表：
  - 在试卷中添加主观题，`exam.html` 添加主观题的答题区域
  - 提交后只看到客观题成绩，需要等待教师批改主观题完成后才能看到总成绩。

- 主线 2 
  > 教师发布考试 -> 学生完成考试 (即完成主线1) -> 教师后台可看见考试数据 (学生答案，成绩分布等)

  待完成列表：
  - 添加批改主观题的功能（这是工作比较多的地方，前端后台都要大量修改）
  - 成绩等信息写入数据库，并开放考卷给予学生查看

- 其他需要完善的细节
  - 在学生考试页面添加**倒计时**功能。
  - 教师考试定时开放。
  - 主观题页面。
  