# coding=utf-8
from flask.ext.migrate import Migrate, MigrateCommand
from flask_script import Manager
from ihome import app, db

# 需求：不修改业务逻辑的代码，只通过修改manage.py文件中的一句代码获取不同配置环境中的app

# 创建Manager管理对象
manager = Manager(app)
Migrate(app, db)
# 添加迁移命令
manager.add_command("db", MigrateCommand)


@app.route("/", methods=["GET", "POST"])
def index():
    # 测试redis
    # redis_store.set("name", "itcast")

    # 测试session存储
    # session["name"] = "itheima"
    return "index"


if __name__ == "__main__":
    manager.run()

