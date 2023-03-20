from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect
from flask_login import login_required, current_user




views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def welcome():
    if current_user.is_authenticated:
        if request.path == url_for('views.home'):
            # user is already on the home page, no need to redirect
            return render_template('home.html', user=current_user)
        else:
            # redirect to home page
            return redirect(url_for('views.home'))
    else:
        return render_template('welcome.html')

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
   
#returns home 
    return render_template("home.html", user=current_user)






