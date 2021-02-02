# @Author  : Shusheng Wang
# @Time    : 2021/2/2 6:04 下午
# @Email   : lastshusheng@163.com


import os
import logging
import click
from flask_cors import *
from flask_migrate import MigrateCommand
from logging.handlers import RotatingFileHandler
from flask import Flask, request
from echarts_data.settings import config, BASE_DIR
from echarts_data.blueprints.echarts_bp import echarts_bp
from echarts_data.extensions import db, migrate, manager


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask('data_analyse')
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    app.config.from_object(config[config_name])
    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_shell_context(app)
    register_commands(app)
    register_global_handel(app)
    return app


def register_logging(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(BASE_DIR, 'logs/data_analyse.log'), maxBytes=10 * 1024 * 1024,
                                       backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(file_handler)


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)


def register_blueprints(app):
    app.register_blueprint(echarts_bp, url_prefix='/api/echarts')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    manager.app = app
    manager.add_command('db', MigrateCommand)


def register_global_handel(app):
    @app.errorhandler(Exception)
    def error_handler(e):
        """
        全局异常捕获
        """
        db.session.rollback()
        raise e
