from flask import Flask, request, jsonify, session, make_response, render_template
import jwt
import datetime
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Bananada é mto bom'


def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Missing token'}), 403
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.exceptions.DecodeError:
            return jsonify({'message': 'Decode error'}), 403
        except:
            return jsonify({'message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return wrapped


@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Currently logged in'


@app.route('/public')
def public():
    return 'Anyone can view this'


@app.route('/auth')
@check_for_token
def auth():
    return 'Only authorized can view this'


@app.route('/login', methods=['POST'])
def login():
    # for purpose of learning jwt quicly the password is hardcoded
    if request.form['username'] and request.form['password'] == '123':
        session['logged_in'] = True
        token = jwt.encode({
            'username': request.form['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
        },
            app.config['SECRET_KEY'])
        return jsonify(token)  # showing the token just for testing pourposes
    else:
        return jsonify({'message': 'Unable to validate the user'}), 403, {'WWW-Authenticate': 'Basic realm: "Login"'}


@app.route('/logout')
def logout():
    if session.get('logged_in'):
        session.clear()
        return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
