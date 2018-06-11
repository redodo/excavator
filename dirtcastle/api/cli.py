import click
import os

from . import settings
from .app import app
from .database import init_db, db


@click.group()
def cli():
    init_db(db)


@cli.command()
@click.option('-h', '--host', default=settings.API_HOST)
@click.option('-p', '--port', default=5000)
@click.option('-d', '--debug', is_flag=True)
def runserver(host, port, debug):
    app.serve(host, port, debug=debug, use_reloader=debug)
