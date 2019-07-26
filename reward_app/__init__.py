import os
from flask import Flask
from flask_migrate import Migrate
import click


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object('reward_app.config')
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/status')
    def status():
        return 'Is Up!'

    from . import db

    db.db.init_app(app)
    migrate = Migrate(app, db.db)

    from . import vouchers
    app.register_blueprint(vouchers.bp)

    # CLI
    from . import commands
    app.cli.add_command(commands.create_user)

    return app
