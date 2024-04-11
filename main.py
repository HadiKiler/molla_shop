from flask import Flask ,send_from_directory,jsonify
from initialize import *
from admin.routes import *
from customer.routes import *
from flask_cors import CORS
from config import UPLOADS_DIR

app = Flask(__name__)
cors = CORS(app)

app.config.from_object('config.DevConfig') 
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = "Please Login first."
login_manager.login_message_category = "danger"

db.init_app(app) 


app.register_blueprint(user_blueprint)
app.register_blueprint(product_blueprint)
app.register_blueprint(category_blueprint)
app.register_blueprint(order_blueprint)
app.register_blueprint(payment_blueprint)
app.register_blueprint(address_blueprint)
app.register_blueprint(feedback_blueprint)
app.register_blueprint(admin_auth_blueprint)
app.register_blueprint(log_blueprint)

app.register_blueprint(site_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(ordering_blueprint)


@app.route('/uploads/<filename>')
def uploads(filename=''):
    return send_from_directory(UPLOADS_DIR, filename)


from admin.models import *

with app.app_context():
    db.create_all()
    user = User.query.first()
    if not user:
        user = User(username="admin",password="admin",is_admin=True)
        db.session.add(user)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
