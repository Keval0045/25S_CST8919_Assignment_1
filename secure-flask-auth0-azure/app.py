from flask import Flask, redirect, session, url_for, render_template, request
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os
from functools import wraps
from datetime import datetime

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Auth0 Config
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=os.getenv("AUTH0_CLIENT_ID"),
    client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
    api_base_url=f"https://{os.getenv('AUTH0_DOMAIN')}",
    access_token_url=f"https://{os.getenv('AUTH0_DOMAIN')}/oauth/token",
    authorize_url=f"https://{os.getenv('AUTH0_DOMAIN')}/authorize",
    client_kwargs={'scope': 'openid profile email'},
)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            app.logger.warning(f"Unauthorized access attempt to {request.path} at {datetime.utcnow()}")
            return redirect('/')
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=os.getenv("AUTH0_CALLBACK_URL"))

@app.route('/callback')
def callback():
    auth0.authorize_access_token()
    userinfo = auth0.get('userinfo').json()
    session['profile'] = {
        'user_id': userinfo['sub'],
        'email': userinfo['email']
    }
    app.logger.info(f"Login successful: user_id={userinfo['sub']}, email={userinfo['email']}, time={datetime.utcnow()}")
    return redirect('/protected')

@app.route('/protected')
@requires_auth
def protected():
    user = session['profile']
    app.logger.info(f"/protected accessed by user_id={user['user_id']}, email={user['email']}, time={datetime.utcnow()}")
    return render_template('protected.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
