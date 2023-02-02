import sqlite3
import bcrypt
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def get_db():
    db = sqlite3.connect('xprojector.db')
    return db

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.route('/')
def index():
    subscription = request.args.get('subscription', 'free')
    projections_per_hour = {
        'free': 3,
        'premium': 8,
        'enterprise': float('inf'),
    }[subscription]
    price = {
        'free': 0,
        'premium': 8,
        'enterprise': 15,
    }[subscription]
    return render_template('index.html', subscription=subscription, projections_per_hour=projections_per_hour, price=price)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = get_db()
        password = request.form['password'].encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        db.execute(
            'INSERT INTO users (username, email, password, subscription) VALUES (?, ?, ?, ?)',
            (request.form['username'], request.form['email'], hashed_password, request.form['subscription'])
        )
        db.commit()
        return redirect('/')
    return render_template('register.html')
@app.route('/check_for_update')
def check_for_update():
    current_version = request.args.get('version')
    latest_version = get_latest_version()
    if current_version != latest_version:
        return 'A new version is available: {}'.format(latest_version)
    return 'You are using the latest version: {}'.format(current_version)

def get_latest_version():
    # You can retrieve the latest version from your version control system or from a file on your server.
    return '1.0.1'


if __name__ == '__main__':
    app.run(debug=True)


