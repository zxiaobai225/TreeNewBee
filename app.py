from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


from models import db

from models.user import User
from models.node import Node
from models.topic import Topic

from routes.user import main as routes_user
from routes.node import main as routes_node


app = Flask(__name__)
db_path = 'TreeNewBee.sqlite'
manager = Manager(app)


def register_routes(app):
    app.register_blueprint(routes_user)
    app.register_blueprint(routes_node, url_prefix='/node')


def configure_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = 'secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    db.init_app(app)
    register_routes(app)
    return app


# 自定义的命令行命令用来运行服务器
@manager.command
def server():
    app = configure_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=8000,
    )
    app.run(**config)


def configure_manager():
    """
    这个函数用来配置命令行选项
    """
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    configure_manager()
    configure_app()
    manager.run()
