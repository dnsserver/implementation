import requests
import json

from flask import jsonify, Blueprint, render_template, flash, redirect, url_for, g, session, abort, request
from ..database import db, Orn, User, PersonaProvider
from ..oidc import oidc
from werkzeug import exceptions
import datetime

bp = Blueprint('worker', __name__)

@bp.route('/submit_request/', methods=['POST'])
def submit_request():
    token = oidc.get_access_token()
    if not token:
        return jsonify({"message": "no token"}), 401

    # Get token info
    info = oidc.get_token_info(token)
    scopes = info["scope"].split(' ')
    client_id = info['client_id']
    user_id = info['user_id']

    # Get job info with structure
    """
    {
        id: job_id,
        orn: opal resource name,
        sync: true/false - should the result be returned or submited into url,
        url: url to post results,
        params: [] - array of parameter objects
    }
    """
    print(info)
    job = request.get_json()

    # Check if job.orn is in scopes list
    try:
        if job['orn'] not in info["scope"].split(" "):
            return jsonify(error=400, message="orn not in scope1"), 400
    except:
        return jsonify(error=400, message="orn not in scope2"), 400

    orn = Orn.query.filter_by(name=job["orn"]).first()
    if not orn:
        return jsonify(error=400, message="orn not found"), 400

    print(orn.json_obj())
    sources = orn.sources
    algs = orn.algorithms
    dt = datetime.datetime.utcnow()

    ret_val = {
        "sources": [s.json_obj() for s in sources],
        "algorithms": [a.json_obj() for a in algs],
        "datetime": dt,
        "client_id": client_id,
        "user_id": user_id
    }
    print(ret_val)
    return jsonify(ret_val), 200
