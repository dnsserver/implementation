# -*- coding: utf-8 -*-
import requests
import json
from flask import flash, session, redirect, url_for, request, abort, g, jsonify
import flask_oidc
from functools import wraps
from sqlalchemy.event import listen

from .database import User, db, Orn

flask_oidc.logger.setLevel(10)


class OpenIDConnect(flask_oidc.OpenIDConnect):
    # def refresh_token(self):
    #     pass

    def get_token_info(self, token):
        return self._get_token_info(token)

    def require_access_token(self, func):
        """Checks if there is access token or not."""
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if self.get_access_token():
                return func(*args, **kwargs)
            else:
                return jsonify({"message": "no token"})
        return decorated_function


    def get_access_token(self):
        token = None
        try:
            token = super().get_access_token()
        except:
            if 'Authorization' in request.headers and request.headers['Authorization'].startswith('Bearer '):
                token = request.headers['Authorization'].split(None, 1)[1].strip()
            if 'access_token' in request.form:
                token = request.form['access_token']
            elif 'access_token' in request.args:
                token = request.args['access_token']
        # print(token)
        return token

    def get_configuration(self):
        cfg = self.client_secrets.copy()
        cfg.pop('client_secret', None)
        return cfg

    def delete_client(self, id):
        pass

    def _update_client(self, cl):
        token = self.client_secrets['registration_access_token']
        url = "%s/%s"%(self.client_secrets['registration_uri'], cl['client_id'])
        if not token:
            raise Exception("No access token")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(token)
        }
        # grant_types = " ".join(cl["grant_types"])
        # cl["grant_types"] = grant_types

        r = requests.put(url, json=cl, headers=headers)
        r.raise_for_status()

    def _get_client(self):
        token = self.client_secrets['registration_access_token']
        url = "%s/%s"%(self.client_secrets['registration_uri'], self.client_secrets['client_id'])
        if not token:
            raise Exception("No access token")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(token)
        }
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.json()

    def register_client(self, data):
        """
        :param data: python object that can be serialized into json
        :return: python object serialized from json response
        """
        token = self.get_access_token()
        url = self.client_secrets['registration_uri']
        if not token:
            raise Exception("No access token")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(token)
        }
        r = requests.post(url, json=data, headers=headers)
        r.raise_for_status()
        return r.json()

    def update_scope(self, orn):
        print("update scope for %s"%orn['name'])
        cl = self._get_client()
        scopes = cl['scope'].split(' ')
        if orn['name'] not in scopes:
            scopes.append(orn['name'])

        cl['scope'] = ' '.join(scopes)
        self._update_client(cl)

    def insert_scope(self, orn):
        print("insert scope for %s"%orn['name'])
        cl = self._get_client()
        scopes = cl['scope'].split(' ')
        if orn['name'] not in scopes:
            scopes.append(orn['name'])

        cl['scope'] = ' '.join(scopes)
        self._update_client(cl)

    def delete_scope(self, orn):
        print("delete scope for %s"%orn['name'])
        cl = self._get_client()
        scopes = cl['scope'].split(' ')
        if orn['name'] in scopes:
            scopes.remove(orn['name'])

        cl['scope'] = ' '.join(scopes)
        self._update_client(cl)


oidc = OpenIDConnect()

def orn_after_insert(mapper, connection, instance):
    oidc.insert_scope(instance.json_obj())

def orn_after_update(mapper, connection, instance):
    oidc.update_scope(instance.json_obj())

def orn_after_delete(mapper, connection, instance):
    oidc.delete_scope(instance.json_obj())


def register_oidc(app):
    oidc.init_app(app)

    listen(Orn, 'after_update', orn_after_update)
    listen(Orn, 'after_insert', orn_after_insert)
    listen(Orn, 'after_delete', orn_after_delete)

    @app.before_request
    def before_request_oidc():
        token = oidc.get_access_token()
        if oidc.user_loggedin and not hasattr(g, 'sub'):
            g.sub = oidc.user_getfield("sub")
            g.access_token = oidc.get_access_token()
            g.access_type = "web"
            user = User.query.get(g.sub)
            if user and oidc.get_access_token():
                g.user = User.query.get(g.sub)
        elif token is not None:
            info = oidc.get_token_info(token)
            if info['active']:
                g.sub = info['sub']
                g.access_token = token
                g.access_type = "api"

    @app.teardown_appcontext
    def teardown_oidc(_):
        """Closes the database and other resources."""
        sub = getattr(g, 'sub', None)
        if sub is not None:
            g.pop('sub', None)
            g.pop('access_token', None)
            g.pop('user', None)
            g.pop('access_type', None)

    @app.route('/login')
    @oidc.require_login
    def login():
        user = User.query.get(oidc.user_getfield('sub'))
        if not user:
            user = User(id=oidc.user_getfield('sub'),
                        email=oidc.user_getfield('email'),
                        full_name=oidc.user_getfield('name'),
                        nick=oidc.user_getfield('preferred_username'),
                        other=oidc.user_getfield('other'))
            db.session.add(user)
            db.session.commit()

        flash("Welcome {} !".format(user.nick))
        return redirect(url_for('index'))

    @app.route('/logout')
    def logout():
        oidc.logout()
        session.clear()
        flash(u'You were signed out')
        return redirect(url_for('index'))
