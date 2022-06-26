import os
from flask import render_template,redirect,session,request,json
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
                            toppings_meat=json_data['toppings_meat'])