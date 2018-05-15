# coding=utf-8
from flask.ext.migrate import Migrate, MigrateCommand
from flask_script import Manager
from ihome import create_app, db, models


# 需求：不修改业务逻辑的代码，只通过修改manage.py文件中的一句代码获取不同配置环境中的app
app = create_app("development")
# 创建Manager管理对象
manager = Manager(app)
Migrate(app, db)
# 添加迁移命令
manager.add_command("db", MigrateCommand)


if __name__ == "__main__":
    manager.run()
    # app.run()
