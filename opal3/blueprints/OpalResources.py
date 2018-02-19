import requests
import json

from flask import jsonify, Blueprint, render_template, flash, redirect, url_for, g, session, abort, request
from ..database import db, Orn, Algorithm, Source
from ..oidc import oidc
from werkzeug import exceptions

bp = Blueprint('OpalResources', __name__)

@bp.route('/orn/', methods=['GET'])
# @oidc.accept_token(True, ['openid'])
def orn_index():
    orns = Orn.query.all()
    cls = [o.json_obj() for o in orns]
    return jsonify(cls)


@bp.route('/orn/<cid>', methods=['GET'])
# @oidc.accept_token(True, ['openid'])
def orn_id(cid):
    pt = Orn.query.filter_by(id=cid).first()
    return jsonify(pt.json_obj())


@bp.route('/algorithm/', methods=['GET'])
# @oidc.accept_token(True, ['openid'])
def algoritm_index():
    algs = Algorithm.query.all()
    cls = [o.json_obj() for o in algs]
    return jsonify(cls)


@bp.route('/algorithm/<aid>', methods=['GET'])
# @oidc.accept_token(True, ['openid'])
def algorithm_id(aid):
    pt = Algorithm.query.filter_by(id=aid).first()
    return jsonify(pt.json_obj())


@bp.route('/source/', methods=['GET'])
# @oidc.accept_token(True, ['openid'])
def source_index():
    srcs = Source.query.all()
    cls = [o.json_obj() for o in srcs]
    return jsonify(cls)


@bp.route('/source/<sid>', methods=['GET'])
# @oidc.accept_token(True, ['openid'])
def source_id(sid):
    pt = Source.query.filter_by(id=sid).first()
    return jsonify(pt.json_obj())


@bp.errorhandler(500)
def server_error(e):
    return jsonify(error=500, text=str(e)), 500


@bp.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404
