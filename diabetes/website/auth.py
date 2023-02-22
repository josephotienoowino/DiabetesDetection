from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
import pandas as pd
import pickle


auth = Blueprint('auth', __name__)

# model = pickle.load(open("Diabetes.pkl", "rb"))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

# @auth.route('/predict',methods=['POST','GET'])
# def predict():
#     text1 = request.form['1']
#     text2 = request.form['2']
#     text3 = request.form['3']
#     text4 = request.form['4']
#     text5 = request.form['5']
#     text6 = request.form['6']
#     text7 = request.form['7']
#     text8 = request.form['8']
 
#     row_df = pd.DataFrame([pd.Series([text1,text2,text3,text4,text5,text6,text7,text8])])
#     print(row_df)
#     prediction=model.predict_proba(row_df)
#     output='{0:.{1}f}'.format(prediction[0][1], 2)
#     output = str(float(output)*100)+'%'
#     if output>str(0.5):
#         return render_template('result.html',pred=f'You have chance of having diabetes.\nProbability of having Diabetes is {output}')
#     else:
#         return render_template('result.html',pred=f'You are safe.\n Probability of having diabetes is {output}')