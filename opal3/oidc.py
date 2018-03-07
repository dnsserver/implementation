# -*- coding: utf-8 -*-
import requests
from flask import flash, session, redirect, url_for, request, abort, g
import flask_oidc
from .database import User, db

flask_oidc.logger.setLevel(10)


class OpenIDConnect(flask_oidc.OpenIDConnect):
    # def refresh_token(self):
    #     pass

    def get_token_info(self, token):
        return self._get_token_info(token)

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

    def delete_client(self, id):
        pass

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


oidc = OpenIDConnect()


def register_oidc(app):
    oidc.init_app(app)

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
