from flask import Flask, session
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_mail import Mail

from datetime import timedelta
from models import db

from models.user import User
from models.node import Node
from models.topic import Topic
from models.board import Board

from routes.chat import main as routes_chat
from routes.user import main as routes_user
from routes.node import main as routes_node
from routes.mail import main as routes_mail
from routes.profile import main as routes_profile
from routes.board import main as routes_board


app = Flask(__name__)
db_path = 'TreeNewBee.sqlite'
manager = Manager(app)


def register_routes(app):
    app.register_blueprint(routes_user)
    app.register_blueprint(routes_node, url_prefix='/node')
    app.register_blueprint(routes_mail, url_prefix='/mail')
    app.register_blueprint(routes_profile, url_prefix='/profile')
    app.register_blueprint(routes_board, url_prefix='/board')
    app.register_blueprint(routes_chat, url_prefix='/chat')


def configure_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = 'secret key'
    # 设置session过期时间
    app.permanent_session_lifetime = timedelta(days=30)
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
