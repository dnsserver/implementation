import requests
from flask import jsonify, Blueprint, render_template, flash, redirect, url_for, g, session, abort, request
from ..database import db, Orn, DSClient, User
from ..oidc import oidc


bp = Blueprint('client', __name__)


@bp.route('/client')
def index():
    dsclients = DSClient.query.filter_by(user_id=oidc.user_getfield("sub")).all()
    cls = [cl.json_obj() for cl in dsclients]
    return jsonify(cls)


@bp.route('/client/delete', methods=['POST'])
def delete(id):
    flash("Not implemented.")
    return redirect(url_for('client.index'))


@bp.route('/client/register', methods=['GET', 'POST'])
def register():
    error = None
    orns = Orn.query.all()
    selected_orns = None
    if request.method == 'POST':
        token = oidc.get_access_token()
        email = oidc.user_getfield("email") or "not provided"
        if not token:
            oidc.logout()
            flash("Please login.")
            return redirect(url_for('index'))

        scope = "openid email"
        if 'orn' in request.values:
            list_orn = request.values.getlist('orn')
            selected_orns = Orn.query.filter(Orn.id.in_(list_orn)).all()
            for sel in selected_orns:
                scope = "{} {}".format(scope, sel.name)

        data = {
                "client_id": None,
                "client_secret": None,
                "redirect_uris": [
                    request.form['redirect_url']
                ],
                "client_name": request.form['name'],
                "client_uri": None,
                "logo_uri": None,
                "contacts": [
                    email
                ],
                "tos_uri": None,
                "token_endpoint_auth_method": "client_secret_post",
                "scope": scope,
                "grant_types": [
                    "authorization_code"
                ],
                "response_types": [
                    "code"
                ],
                "policy_uri": None,
                "jwks_uri": None,
                "jwks": None,
                "jwksType": "URI",
                "sector_identifier_uri": None,
                "request_object_signing_alg": None,
                "userinfo_signed_response_alg": None,
                "userinfo_encrypted_response_alg": None,
                "userinfo_encrypted_response_enc": None,
                "id_token_signed_response_alg": None,
                "id_token_encrypted_response_alg": None,
                "id_token_encrypted_response_enc": None,
                "default_max_age": 60000,
                "require_auth_time": True,
                "default_acr_values": [],
                "initiate_login_uri": None,
                "post_logout_redirect_uris": [],
                "claims_redirect_uris": [],
                "request_uris": [],
                "software_statement": None,
                "software_id": None,
                "software_version": None,
                "code_challenge_method": None,
                "registration_access_token": None,
                "registration_client_uri": None,
                "softwareId": None,
                "softwareVersion": None,
                "token_endpoint_auth_signing_alg": None
        }
        try:
            r = oidc.register_client(data)
            dsclient = DSClient()
            dsclient.orns = selected_orns
            if 'name' in request.values:
                dsclient.name = request.values['name']
            if 'description' in request.values:
                dsclient.description = request.values['description']
            if 'recurring' in request.values:
                dsclient.recurring = request.values['recurring']
            if 'redirect_url' in request.values:
                dsclient.redirect_url = request.values['redirect_url']

            dsclient.request_json = jsonify(data)
            dsclient.response_json = r
            dsclient.user_id = oidc.user_getfield("sub")

            db.session.add(dsclient)
            db.session.commit()
            flash('Client registered.')
            return redirect(url_for('client.details', id=dsclient.id))
        except requests.exceptions.HTTPError as err:
            error = err

    return render_template('client/register.html', error=error, orns=orns)


@bp.route('/client/details/<id>')
def details(id):
    dsclient = DSClient.query.filter_by(id=id).first()
    error = None
    if not dsclient:
        error = "Client not found."
    return render_template('client/details.html', error=error, client=dsclient)
