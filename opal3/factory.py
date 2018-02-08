# -*- coding: utf-8 -*-

import click

from flask import Flask, render_template, _app_ctx_stack as stack, session, g, request, abort
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_bootstrap import Bootstrap
from flask_cors import CORS

from .database import register_database, db, admin, User, OrnType
from .utils import register_blueprints
from .oidc import register_oidc, oidc


def create_app(config=None):
    app = Flask('opal3')

    app.config.update(dict(
        DEBUG=True,
        TESTING=True,
        SECRET_KEY=b'_5#y2L"Fd3sd8z\n\xec]/',

        SQLALCHEMY_DATABASE_URI='sqlite:///opal3.db',
        SQLALCHEMY_ECHO=False,
        SQLALCHEMY_TRACK_MODIFICATIONS=True,

        OIDC_CLIENT_SECRETS='opal3/client_secrets.json',
        OIDC_ID_TOKEN_COOKIE_SECURE=False,
        OIDC_REQUIRE_VERIFIED_EMAIL=False,
        OIDC_USER_INFO_ENABLED=True,
        OIDC_INTROSPECTION_AUTH_METHOD='client_secret_post',
        OIDC_OPENID_REALM='http://localhost:5000/oidc_callback',
        OIDC_SCOPES=['openid', 'profile', 'email', 'address', 'phone', ],
    ))

    app.config.update(config or {})
    app.config.from_envvar('OPAL3_SETTINGS', silent=True)

    CORS(app)
    register_cli(app)
    register_database(app)
    register_oidc(app)

    admin.init_app(app)
    register_blueprints(app)
    Bootstrap(app)
    register_nav(app)
    return app


def register_nav(app):
    nav = Nav()

    @nav.navigation()
    def opalnavbar():
        items = list()
        items.append(View('Home', 'index'))
        if oidc.user_loggedin:
            items.append(View('Client', 'client.index'))
            if oidc.user_getfield("sub") == "90342.ASDFJWFA":
                items.append(View("Admin", "admin.index"))
            items.append(View('Logout', 'logout'))
        else:
            items.append(View('Login', 'login'))

        return Navbar('OPAL', *items)
    nav.init_app(app)


def register_cli(app):
    @app.cli.command('initdb')
    def initdb_command():
        """Creates the blueprints tables."""
        db.create_all()
        for tmp in ["csv", "json", "text", "praquet", "jdbc"]:
            dt = OrnType()
            dt.name = tmp
            db.session.add(dt)
        db.session.commit()
        click.echo('Initialized the database.')


app = create_app()


@app.route('/')
def index():
    return render_template('index.html')
