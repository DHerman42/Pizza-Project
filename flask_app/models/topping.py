from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Topping:
    db_name ="pizzatime"
    def __init__(self,data):
        self.id = data['id']
        self.method = data['method']
        self.size = data['size']
        self.crust = data['crust']
        self.toppings = data['toppings']
        self.user_id = data['user_id']

    @classmethod
    def save(cls,data):
        query ="INSERT INTO topping (method,size,crust,toppings,quantity,price,user_id) values (%(method)s,%(size)s,%(crust)s,%(toppings)s,%(quantity)s,%(price)s,%(user_id)s);"
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
    def get_topping_user(cls,data):
        query = "SELECT * from topping LEFT JOIN user on user.id = topping.user_id where user.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        all_toppings = []
        for topping in results:
            print(topping['id'])
            all_toppings.append( cls(topping) )
        return all_toppings

    @classmethod
    def update(cls,data):
        query = "UPDATE topping SET method=%(method)s, size=%(size)s, crust=%(crust)s, toppings=%(toppings)s, quantity=%(quantity)s, price=%(price)s;"

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM topping where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)


