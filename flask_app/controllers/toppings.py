from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.topping import Topping
from flask_app.models.user import User


@app.route('/new/order')
def new_order():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template(new_order.html, user=User.get_id(data))

@app.route('/create/order',methods=['POST'])
def create_order():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Topping.validate_job(request.form):
        return redirect('/new/order')
    data = {
        "method": request.form["method"],
        "size": request.form["size"],
        "crust": request.form["crust"],
        "toppings": request.form["toppings"],
        "user_id": session["user_id"]
    }
    Topping.save(data)
    return redirect('/dashboard')


@app.route('user/account/<int:id>')
def user_account(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" :id
    }
    return render_template("user_account.html", topping=Topping.get_topping_user(data),user=User.get_id(data))