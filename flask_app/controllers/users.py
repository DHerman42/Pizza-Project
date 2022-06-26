from flask import render_template,redirect,session,request
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register',methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']),
        "address": request.form['address'],
        "city": request.form['city'],
        "state": request.form['state']
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/dashboard')


@app.route("/login", methods=['POST'])
def login():
    data = {
        'email': request.form['email'],
        'password': request.form['password']
    }

    user_in_db = User.validate_login(data)

    if not user_in_db:
        return redirect('/')
    else:
        session['user_id'] = user_in_db['id']
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')