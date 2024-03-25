from flask import Blueprint, jsonify, request
from .models import Log
from initialize import db
from ast import literal_eval

blueprint = Blueprint('log', __name__)


@blueprint.route('/log', methods=["GET"])
def logs():
    filter = literal_eval(request.args.get('filter')) # change strig to dict
    sort = literal_eval(request.args.get('sort'))[1]

    qs = []
    try:
        q = filter['q']
        for log in Log.query.all():
            if str(log.user_id) == q or q in log.action:
                qs.append(log)
    except:
        qs = Log.query.all()


    if sort == "DESC":
        qs = list(qs)
        qs.reverse()
        
    data = []
    for log in qs:
        data.append({
            "id": log.id,
            'user_id': log.user_id,
            'action': log.action,
            'action_date': log.action_date,
        })
    response = jsonify(data)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(data)
    return response


@blueprint.route('/log/<int:id>', methods=["GET"])
def read_log(id):
    l = Log.query.get(id)
    return jsonify({
            "id": l.id,
            'user_id': l.user_id,
            'action': l.action,
            'action_date': l.action_date,
        })
