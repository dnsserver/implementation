# -*- coding: utf-8 -*-

from flask import g, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from wtforms import validators

import flask_admin as admin
from flask_admin.base import expose, MenuLink

from flask_admin.contrib import sqla

import datetime


db = SQLAlchemy()


def register_database(app):
    db.init_app(app)

    @app.before_request
    def before_request_db():
        dba = getattr(g, '_database', None)
        if dba is None:
            g._database = True

    @app.teardown_appcontext
    def teardown_app(_):
        """Closes the database and other resources."""
        database = getattr(g, '_database', None)
        if database is not None:
            db.session.close()


# Create models
class User(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    email = db.Column(db.String(120), unique=True)
    nick = db.Column(db.String(100))
    full_name = db.Column(db.String(80), unique=True)
    other = db.Column(db.String(200))

    def __str__(self):
        return self.email

    def json_obj(self):
        return {
            "id": self.id,
            "email": self.email,
            "nick": self.nick,
            "full_name": self.full_name,
            "other": self.other
        }


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))

    def __str__(self):
        return self.name

    def json_obj(self):
        return {
            "id": self.id,
            "name": self.name
        }


class SourceType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __str__(self):
        return self.name

    def json_obj(self):
        return {
            "id": self.id,
            "name": self.name
        }


# Create M2M table
source_tags_table = db.Table('source_tags', db.Model.metadata,
                          db.Column('source_id', db.Integer, db.ForeignKey('source.id')),
                          db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                          )


class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    uri = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    tags = db.relationship('Tag', secondary=source_tags_table)
    source_type_id = db.Column(db.Integer, db.ForeignKey(SourceType.id), nullable=False)
    source_type = db.relationship(SourceType, backref='source')

    def __str__(self):
        return self.name

    def json_obj(self):
        return {
            "id": self.id,
            "name": self.name,
            "uri": self.uri,
            "description": self.description,
            "date": self.date,
            "tags": [tag.name for tag in self.tags],
            "source_type": self.source_type_id,
        }


class Algorithm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __str__(self):
        return self.name

    def json_obj(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date": self.date
        }


orn_source_table = db.Table('orn_source', db.Model.metadata,
                          db.Column('source_id', db.Integer, db.ForeignKey('source.id')),
                          db.Column('orn_id', db.Integer, db.ForeignKey('orn.id'))
                          )
orn_algorithm_table = db.Table('orn_algorithm', db.Model.metadata,
                          db.Column('algorithm_id', db.Integer, db.ForeignKey('algorithm.id')),
                          db.Column('orn_id', db.Integer, db.ForeignKey('orn.id'))
                          )


class Orn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    sources = db.relationship('Source', secondary=orn_source_table)
    algorithms = db.relationship('Algorithm', secondary=orn_algorithm_table)

    def json_obj(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "sources": [source.id for source in self.sources],
            "algorithms": [algorithm.id for algorithm in self.algorithms]
        }


class PersonaProvider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    oidc_request = db.Column(db.Text, nullable=False)
    oidc_response = db.Column(db.Text, nullable=False)

    def __str__(self):
        return self.name

    def json_obj(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "oidc_request": self.oidc_request,
            "oidc_response": self.oidc_response
        }




# Customized User model admin
class UserAdmin(sqla.ModelView):
    # inline_models = (PersonaProvider,)

    def is_accessible(self):
        return hasattr(g, 'user')


class MyModelView(sqla.ModelView):
    def is_accessible(self):
        return hasattr(g, 'user')


class AuthenticatedMenuLink(MenuLink):
    def is_accessible(self):
        return hasattr(g, 'user')


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not hasattr(g, 'user'):
            return redirect(url_for('login'))
        return super(MyAdminIndexView, self).index()


# Create admin
admin = admin.Admin(name='Admin', template_mode='bootstrap3', index_view=MyAdminIndexView())
# Add views
admin.add_view(UserAdmin(User, db.session))
admin.add_view(MyModelView(Tag, db.session))
admin.add_view(MyModelView(SourceType, db.session))
admin.add_view(MyModelView(Source, db.session))
admin.add_view(MyModelView(Algorithm, db.session))

admin.add_view(MyModelView(Orn, db.session))
admin.add_view(MyModelView(PersonaProvider, db.session))

admin.add_link(AuthenticatedMenuLink(name="Logout", endpoint="logout"))
