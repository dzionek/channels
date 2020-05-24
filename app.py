from flask import Flask, render_template, session, request, jsonify
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

Session()

def is_logged():
    if not session.get('username'):
        return False
    elif not isinstance(session['username'], str):
        raise TypeError('Username is not a string')
    else:
        return True

@app.route('/')
def default():
    if is_logged():
        return render_template('app.html', username=session['username'])
    else:
        return render_template('login.html')

@app.route('/log_in', methods=['POST'])
def log_in():
    username = request.form.get('username')
    session['username'] = username
    return render_template('app.html', username=username)


if __name__ == '__main__':
    app.debug = True
    app.run()
