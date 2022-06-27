import os
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import json

class Topping:
    db_name ="pizzatime"
    def __init__(self,data):
        self.id = data['id']
        self.method = data['method']
        self.size = data['size']
        self.crust = data['crust']
        self.toppings = data['toppings']
        self.toppings_count = data['toppings_count']
        self.quantity = data['quantity']
        self.user_id = data['user_id']
        self.created_at = data['created_at']

    @classmethod
    def save(cls,data):
        query ="INSERT INTO topping (method,size,crust,toppings,toppings_count,quantity,user_id, created_at) values (%(method)s,%(size)s,%(crust)s,%(toppings)s,%(toppings_count)s,%(quantity)s,%(user_id)s, NOW());"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM topping LEFT JOIN user on user.id = topping.user_id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_toppings = []
        for topping in results:
            print(topping['id'])
            all_toppings.append( cls(topping) )
        return all_toppings

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM topping WHERE id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]

    @classmethod
    def get_topping_user(cls,data):
        query = "SELECT * from topping LEFT JOIN user on user.id = topping.user_id where user.id = %(id)s ORDER BY created_at DESC;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        all_toppings = []
        for topping in results:
            print(topping['id'])
            all_toppings.append( cls(topping) )
        return all_toppings

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM topping where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def calculate_total(data):

        total = 0.0

        filename = os.path.join(app.static_folder, 'json', 'settings.json')
        f = open(filename)
        json_data = json.load(f)
        f.close()

        if(data['size'] == "Large"):
            total += json_data['price_large']
        elif(data['size'] == "Medium"):
            total += json_data['price_med']
        elif(data['size'] == "Small"):
            total += json_data['price_small']

        total += data['toppings_count'] * json_data['price_toppings']

        total *= int(data['quantity'])

        if(data['method'] == "Delivery"):
            total += json_data['price_delivery']

        total = round(total, 2)

        return total
