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
