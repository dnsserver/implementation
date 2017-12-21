# -*- coding: utf-8 -*-
import requests
from flask import flash, session, redirect, url_for, request, abort, g
import flask_oidc
from .database import User, db


class OpenIDConnect(flask_oidc.OpenIDConnect):
    # def refresh_token(self):
    #     pass

    # def get_access_token(self):
    #     token = super().get_access_token()
    #     if token:
    #         return token
    #     elif not token and 'oidc-token' in session:
    #         return session['oidc-token']
    #     else:
    #         return None

    def delete_client(self, id):
        pass

    def register_client(self, data):
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
        return r.text



oidc = OpenIDConnect()


def register_oidc(app):
    oidc.init_app(app)

    @app.before_request
    def before_request():
        if oidc.user_loggedin and 'oidc' not in session:
            session['oidc-token'] = oidc.get_access_token()

        if oidc.user_loggedin:
            print("sub:", oidc.user_getfield("sub"))
            print("email:", oidc.user_getfield("email"))

        public_endpoints = ['index', 'login', 'logout', '_oidc_callback']
        if not oidc.user_loggedin and request.endpoint not in public_endpoints:
            flash("Please login!", category="error")
            return redirect(url_for('index'))

    @app.route('/login')
    @oidc.require_login
    def login():
        user = User(id=oidc.user_getfield('sub'),
                    email=oidc.user_getfield('email'),
                    full_name=oidc.user_getfield('name'),
                    nick=oidc.user_getfield('preferred_username'),
                    other=oidc.user_getfield('other'))
        if not User.query.filter_by(id=user.id).first():
            db.session.add(user)
            db.session.commit()

        flash("Welcome {} !".format(user.nick))
        session['oidc-token'] = oidc.get_access_token()
        return redirect(url_for('index'))

    @app.route('/logout')
    def logout():
        oidc.logout()
        session.clear()
        flash(u'You were signed out')
        return redirect(url_for('index'))