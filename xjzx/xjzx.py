from flask_migrate import Migrate,  MigrateCommand
from app import create_app
from flask_script import Manager
from config import DevelopConfig
from models import db

app = create_app(DevelopConfig)

# 扩展命令　想用右键run直接运行需要在script_parameters中加runserver
manager = Manager(app)

# 初始化数据库
db.init_app(app)

# 数据库迁移　
Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
