import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def getdatabase():
    if 'database' not in g:
        g.database=sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        g.database.row_factory=sqlite3.Row
    return g.database

def closedatabase(e=None):
    database=g.pop('database',None)
    if database is not None:
        database.close()

def initdatabase():
    database=getdatabase()
    with current_app.open_resource('schema.sql') as f:
        database.executescript(f.read().decode('utf8'))

@click.command('initdatabase')
@with_appcontext
def initdatabasecommand():
    initdatabase()
    click.echo('Initialized the database.')

def initapplication(app):
    app.teardown_appcontext(closedatabase)
    app.cli.add_command(initdatabasecommand)