from flask import Blueprint, jsonify, request
from .models import FeedBack
from initialize import db
from ast import literal_eval

blueprint = Blueprint('feedback', __name__)


@blueprint.route('/feedback', methods=["GET"])
def feedbacks():
    filter = literal_eval(request.args.get('filter')) # change strig to dict
    qs = []
    try:
        q = filter['q']
        for feedback in FeedBack.query.all():
            if str(feedback.order_id) == q or feedback.user.username == q:
                qs.append(feedback)
    except:
        qs = FeedBack.query.all()
    data = []
    for feedback in qs:
        data.append({
            "id": feedback.id,
            'order_id': feedback.order_id,
            'user_id': feedback.user_id,
            'rating': feedback.rating,
            'comment': feedback.comment,
            'feedback_date': feedback.feedback_date,
        })
    response = jsonify(data)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(data)
    return response


@blueprint.route('/feedback/<int:id>', methods=["GET"])
def read_feedback(id):
    f = FeedBack.query.get(id)
    return jsonify({
            "id": f.id,
            'order_id': f.order_id,
            'user_id': f.user_id,
            'rating': f.rating,
            'comment': f.comment,
            'feedback_date': f.feedback_date,
        })
