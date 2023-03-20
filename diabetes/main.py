from website import create_app
from flask import Blueprint, render_template, request, flash, redirect, url_for
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from flask_login import login_required, current_user
from datetime import datetime



clf = LogisticRegression()
app = create_app()

model = pickle.load(open("model.pkl", "rb"))
    
@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    prediction = request.args.get('pred')
    return render_template("home.html", user=current_user, pred=prediction)

@app.route('/results')
@login_required
def results():
    prediction = request.args.get('pred')
    return render_template("results.html", user=current_user, pred=prediction)

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    text1 = request.form['1']
    text2 = request.form['2']
    text3 = request.form['3']
    text4 = request.form['4']
    text5 = request.form['5']
    text6 = request.form['6']
    text7 = request.form['7']
    text8 = request.form['8']

    row_df = pd.DataFrame([pd.Series([text1,text2,text3, text4, text5, text6,text7,text8])])

    prediction = model.predict_proba(row_df)
    output = '{0:.{1}f}'.format(prediction[0][1], 2)
    output = float(output) * 100

    if output > 40.0:
        return redirect(url_for('results', pred=f'You have chance of having diabetes.\n {output}%'))
    else:
        return redirect(url_for('results', pred=f'You are safe.\n  {output}%'))

    if output > 40.0:
        return redirect(url_for('results', pred=f'You have a positive diabetes detection.\nProbability of having Diabetes is {output}%'))
    else:
        return redirect(url_for('results', pred=f'You are safe.\n Probability of having diabetes is {output}%'))


if __name__ == '__main__':
    app.run(debug=True)
