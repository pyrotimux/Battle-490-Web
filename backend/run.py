from flask import Flask, render_template, request
from flask import Flask, redirect, url_for, session, request
from flask_oauthlib.client import OAuth
from dbinit import DataInit
import sys

app = Flask(__name__)
app.config['GOOGLE_ID'] = 'IDHERE'
app.config['GOOGLE_SECRET'] = 'SECRET HERE'
app.debug = True
app.secret_key = 'MORE SECRET HERE'
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

def check_auth():
    if 'google_token' in session:
        authdict = google.get('userinfo').data
        if "email" in authdict:
            if  authdict["email"] == "teemo3737@gmail.com" and authdict["verified_email"] == True:
                return True
    return False



@app.route('/')
def index():
    if check_auth():
        return render_template('control.html')
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return redirect(url_for('logout'))

    session['google_token'] = (resp['access_token'], '')
    return redirect(url_for('index'))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


@app.route('/request', methods=['POST'])
def show_request():
    if not check_auth:
        return redirect(url_for('index'))

    if request.method == 'POST':
        pass

@app.route('/dbinit')
def dbinit():
    if check_auth():
        dbi = DataInit()
        dbi.create_dbs()
        return "Hello World!"
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=777, debug = True)