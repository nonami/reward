import click
from flask.cli import AppGroup
from reward_app import authmanager

user_cli = AppGroup('user')


@user_cli.command('create')
@click.argument('username')
@click.argument('password')
def create_user(username, password):
    authmanager.create_user(username, password)
    click.echo('Done')
