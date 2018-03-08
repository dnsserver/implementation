import requests
import json

from flask import jsonify, Blueprint, render_template, flash, redirect, url_for, g, session, abort, request
from ..database import db, Orn, User, PersonaProvider
from ..oidc import oidc
from werkzeug import exceptions

bp = Blueprint('client', __name__)


def get_persona_provider(id):
    pp = PersonaProvider.query.filter_by(name=id).first()
    if not pp:
        raise exceptions.NotFound("PersonalProvider not found.")
    return pp


@bp.route('/configuration/', methods=['GET'])
@oidc.require_access_token
def configuration():
    conf = oidc.get_configuration()
    return jsonify(conf)


@bp.route('/user_info/', methods=['GET'])
def user_info():
    token = oidc.get_access_token()
    if token:
        info = oidc.get_token_info(token)
        return jsonify(info)
    return jsonify({"message": "no token"})


@bp.route('/token_info/', methods=['GET'])
def token_info():
    token = oidc.get_access_token()
    if token:
        info = oidc.get_token_info(token)
        return jsonify(info)
    return jsonify({"message": "no token"})


@bp.route('/client/', methods=['GET'])
# @oidc.accept_token(False, ['openid'])
@oidc.require_access_token
def index():
    ds_clients = PersonaProvider.query.all()
    cls = [cl.json_obj() for cl in ds_clients]
    return jsonify(cls)


@bp.route('/client/<pid>', methods=['DELETE'])
@oidc.require_access_token
def delete(pid):
    pp = get_persona_provider(pid)
    db.session.delete(pp)
    db.session.commit()
    return jsonify(text="deleted"), 200


@bp.route('/client/<pid>', methods=['GET'])
@oidc.require_access_token
def details(pid):
    pp = get_persona_provider(pid)
    return jsonify(pp.json_obj())


@bp.route('/client/', methods=['POST'])
@oidc.require_access_token
def register():
    client_obj = request.get_json()

    # TODO: validate client_obj required properties

    email = g.sub

    # TODO: verify scope list
    scopes = client_obj.pop('scopes', None)
    # scopes are on the DP - therefore not able to query in the database.
    # commenting it out
    #selected_orns = Orn.query.filter(Orn.name.in_(scopes)).all()
    #client_obj['scope'] = " ".join(["{}:{}".format(s.id,s.name) for s in selected_orns])
    client_obj['scope'] = " ".join(scopes)

    client_obj['contacts'] = [email]

    pt = PersonaProvider()
    pt.name = client_obj['client_name']


    # remove description from OIDC request
    pt.description = client_obj.pop('description', None)
    pt.recurring = client_obj.pop('recurring', False)
    pt.result_url = client_obj.pop('result_url', None)
    # pt.user_id = g.sub
    pt.oidc_request = json.dumps(client_obj)

    try:
        r = oidc.register_client(client_obj)
        pt.oidc_response = json.dumps(r)
        db.session.add(pt)
        db.session.commit()

        return jsonify(pt.json_obj())
    except Exception as err:
        print(err)
        raise exceptions.InternalServerError()


@bp.errorhandler(500)
def server_error(e):
    return jsonify(error=500, text=str(e)), 500


@bp.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404
