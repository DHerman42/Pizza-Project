import os
from flask import render_template,redirect,session,request,json, url_for
from flask_app import app
from flask_app.models.user import User
from flask_app.models.topping import Topping

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    
    data ={
        'id': session['user_id']
    }

    filename = os.path.join(app.static_folder, 'json', 'settings.json')
    f = open(filename)
    json_data = json.load(f)
    f.close()
    
    return render_template("dashboard.html",
                            user=User.get_id(data), 
                            topping=Topping.get_topping_user(data), 
                            toppings_veg=json_data['toppings_veg'],
                            toppings_meat=json_data['toppings_meat'],
                            order=Topping.get_all())

@app.route('/new_pizza', methods=['POST'])
def new_pizza():
    toppings = ", ".join(request.form.getlist('toppings'))
    data = {
        'method': request.form['method'],
        'size': request.form['size'],
        'crust': request.form['crust'],
        'toppings': toppings,
        'toppings_count': len(request.form.getlist('toppings')),
        'quantity': request.form['quantity'],
        'user_id': session['user_id']
    }

    session['order'] = data

    return redirect(url_for('confirm_order'))

@app.route('/confirm/')
def confirm_order():

    total = Topping.calculate_total(session['order'])

    return render_template('confirm_order.html', order=session['order'], total = total)

@app.route('/create_pizza', methods=['POST'])
def create_pizza():
    Topping.save(session['order'])
    session['order'] = ""
    return redirect('/dashboard')

@app.route('/cancel_order')
def cancel_order():
    session['order'] = ""
    return redirect('/dashboard')

# coming back to this

@app.route('/update_user/<int:id>', methods = ['POST'])
def update_user(id):
    # need to put something here
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "address": request.form['address'],
        "city": request.form['city'],
        "state": request.form['state'],
        "id":id
    }
    
    session['user_id'] = data
    User.edit_user(data)
    
    return redirect('/dashboard')

@app.route('/edit_user/<int:id>')
def edit_user(id):
    data = {
        "id" : id
    }
    
    return render_template('edit_user.html', this_user = User.get_id(data))