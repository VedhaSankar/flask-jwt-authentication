from flask import Flask, jsonify, request, session, render_template, make_response
from functools import wraps
import datetime
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'


def check_for_token(func):

    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        print(data)
        # except:
        #     return jsonify({'message': "Invalid token"}), 403
        return func(*args, **kwargs)
    return wrapped


@app.route('/')
def index():

    # if not session.get('logged_in'):
    return render_template('index.html')

    # else:
    #     return "Currently logged in"

@app.route('/public')
def public():
    return "Anyone can see this"

@app.route('/auth', methods=['GET','POST'])
@check_for_token
def auth():

    return "You are authenticated"

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.form['username'] and request.form['password'] == 'admin':
        session['logged_in'] = True
        token = jwt.encode ({
            'user'  : request.form['username'],
            'exp'   : datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        },
        app.config['SECRET_KEY'],
        algorithm="HS256"
        )
        return jsonify({'token': token})
        
    else:
        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

if __name__ == '__main__':

    app.run(debug = True, port = 8500)