import requests
import json

from flask import jsonify, Blueprint, render_template, flash, redirect, url_for, g, session, abort, request
from ..database import db, Orn, PersonaTemplate, User
from ..oidc import oidc
from werkzeug import exceptions

bp = Blueprint('client', __name__)


def get_persona_template(ptid, ppid):
    pt = PersonaTemplate.query.filter_by(id=ptid, persona_provider_id=ppid).first()
    if not pt:
        raise exceptions.NotFound("Personal template not found.")
    return pt


@bp.route('/token_info/', methods=['GET'])
@oidc.accept_token(True, ['openid'])
def token_info():
    token = oidc.get_access_token()
    print(token)
    if token:
        info = oidc.get_token_info(token)
        print(info)

        return jsonify(info)
    return jsonify({"message": "no token"})


@bp.route('/client/', methods=['GET'])
@oidc.accept_token(True, ['openid'])
def index():
    ds_clients = PersonaTemplate.query.filter_by(persona_provider_id=g.sub).all()
    cls = [cl.json_obj() for cl in ds_clients]
    return jsonify(cls)


@bp.route('/client/<cid>', methods=['DELETE'])
@oidc.accept_token(True, ['openid'])
def delete(cid):
    pt = get_persona_template(cid, g.sub)
    db.session.delete(pt)
    db.session.commit()
    return redirect(url_for('client.index'))


@bp.route('/client/<cid>', methods=['GET'])
@oidc.accept_token(True, ['openid'])
def details(cid):
    pt = get_persona_template(cid, g.sub)
    return jsonify(pt.json_obj())


@bp.route('/client/', methods=['POST'])
@oidc.accept_token(True, ['openid'])
def register():
    client_obj = request.get_json()

    # TODO: validate client_obj required properties

    # check security
    token = g.access_token
    email = g.sub

    if not token:
        oidc.logout()
        raise exceptions.Unauthorized()

    # TODO: verify scope list
    scopes = client_obj['scope'].split(" ")
    # remove openid and email
    if 'openid' in scopes:
        scopes.remove('openid')
    if 'email' in scopes:
        scopes.remove('email')
    # select all orns that are listed in scopes
    selected_orns = Orn.query.filter(Orn.name.in_(scopes)).all()

    client_obj['contacts'] = [email]

    pt = PersonaTemplate()
    pt.orns = selected_orns
    pt.name = client_obj['client_name']

    # remove description from OIDC request
    pt.description = client_obj.pop('description', None)
    pt.recurring = client_obj.pop('recurring', False)
    pt.result_url = client_obj.pop('result_url', None)
    pt.user_id = g.sub
    pt.request_json = json.dumps(client_obj)

    try:
        r = oidc.register_client(client_obj)
        pt.response_json = json.dumps(r)
        db.session.add(pt)
        db.session.commit()

        return redirect(url_for('client.details', cid=pt.id))
    except Exception as err:
        print(err)
        raise exceptions.InternalServerError()


@bp.errorhandler(500)
def server_error(e):
    return jsonify(error=500, text=str(e)), 500


@bp.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404
