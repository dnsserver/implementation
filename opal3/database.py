# -*- coding: utf-8 -*-

import json
from flask_sqlalchemy import SQLAlchemy

from wtforms import validators

import flask_admin as admin
from flask_admin.contrib import sqla

import datetime

db = SQLAlchemy()


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
            "other": self.other,
            "user_info": [user_info.id for user_info in self.info]
        }


class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), nullable=False)
    value = db.Column(db.String(64))
    user_id = db.Column(db.String(200), db.ForeignKey(User.id))
    user = db.relationship(User, backref='info')

    def __str__(self):
        return '%s - %s' % (self.key, self.value)

    def json_obj(self):
        return {
            "id": self.id,
            "key": self.key,
            "value": self.value,
            "user": self.user_id
        }


class OrnType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __str__(self):
        return self.name

    def json_obj(self):
        return {
            "id": self.id,
            "name": self.name
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


# Create M2M table
orn_tags_table = db.Table('orn_tags', db.Model.metadata,
                          db.Column('orn_id', db.Integer, db.ForeignKey('orn.id')),
                          db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                          )

# Create M2M table
orn_dsclient_table = db.Table('orn_dsclient', db.Model.metadata,
                          db.Column('orn_id', db.Integer, db.ForeignKey('orn.id')),
                          db.Column('ds_client_id', db.Integer, db.ForeignKey('ds_client.id'))
                          )

class Orn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    uri = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    tags = db.relationship('Tag', secondary=orn_tags_table)
    orn_type_id = db.Column(db.Integer, db.ForeignKey(OrnType.id), nullable=False)
    orn_type = db.relationship(OrnType, backref='orn')
    dsclients = db.relationship('DSClient', secondary=orn_dsclient_table)

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
            "orn_type": self.orn_type_id,
        }


class DSClient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    orns = db.relationship('Orn', secondary=orn_dsclient_table)
    recurring = db.Column(db.Boolean, default=False)
    redirect_url = db.Column(db.String(200), nullable=False)
    registered_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    request_json = db.Column(db.Text)
    response_json = db.Column(db.Text)
    user_id = db.Column(db.String(200), db.ForeignKey(User.id))
    user = db.relationship(User, backref='dsclient')

    def json_obj(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "orns": [orn.id for orn in self.orns],
            "recurring": self.recurring,
            "redirect_url": self.redirect_url,
            "registered_date": str(self.registered_date),
            "request_json": self.request_json,
            "response_json": self.response_json,
            "user": self.user_id,
        }


# Customized User model admin
class UserAdmin(sqla.ModelView):
    inline_models = (UserInfo,)


class OrnAdmin(sqla.ModelView):
    # Visible columns in the list view
    column_exclude_list = ['uri', 'description']

    # List of columns that can be sorted. For 'user' column, use User.username as
    # a column.
    column_sortable_list = ('name', 'date', ('tag', 'name'))

    column_searchable_list = ('name', 'tags.name')

    column_filters = ('name',
                      'date',
                      'tags')

    # Pass arguments to WTForms. In this case, change label for text field to
    # be 'Big Text' and add required() validator.
    form_args = dict(
        uri=dict(label='URI', validators=[validators.required()])
    )

    form_ajax_refs = {
        'tags': {
            'fields': (Tag.name,)
        }
    }

    def __init__(self, session):
        # Just call parent class with predefined model.
        super(OrnAdmin, self).__init__(Orn, session)


# Create admin
admin = admin.Admin()
# Add views
admin.add_view(UserAdmin(User, db.session))
admin.add_view(OrnAdmin(db.session))
admin.add_view(sqla.ModelView(OrnType, db.session))
admin.add_view(sqla.ModelView(Tag, db.session))
admin.add_view(sqla.ModelView(DSClient, db.session))
