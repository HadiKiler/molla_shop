from flask import Blueprint, jsonify, request,render_template,flash,redirect,url_for
from admin.user.models import User
from initialize import db
from flask_login import login_user,current_user,login_required,logout_user

blueprint = Blueprint('auth', __name__)


@blueprint.route('/login', methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('site.main'))
    if request.method=='POST':
        username = request.form.get('username',"").strip()
        password = request.form.get('password',"").strip()
        remember = bool(request.form.get('remember',""))
        user = User.query.filter_by(username=username).first()
        if user and user.password == password and user.is_admin == False:
            login_user(user,remember=remember)
            flash("logined successfuly !", 'info')
            return redirect(url_for('site.main'))
        else:
             flash("Username or Password Error !", 'info')
    return render_template('auth/login.html')


@blueprint.route('/register', methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('site.main'))
    if request.method=='POST':
        username = request.form.get('username',"").strip()
        password = request.form.get('password',"").strip()
        email = request.form.get('email',"").strip()

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Usernmae alredy exists !','danger')
            return render_template('auth/login.html')
        
        user = User(username=username,password=password,email=email)
        db.session.add(user)
        db.session.commit()
        flash('account successfuly created , now login !','info')
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html')


@blueprint.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.main'))
