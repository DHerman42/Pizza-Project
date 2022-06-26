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
        self.toppings_count = data['toppings_count']
        self.quantity = data['quantity']
        self.favorite = data['favorite']
        self.user_id = data['user_id']
        self.created_at = data['created_at']

    @classmethod
    def save(cls,data):
        query ="INSERT INTO topping (method,size,crust,toppings,toppings_count,quantity,favorite,user_id, created_at) values (%(method)s,%(size)s,%(crust)s,%(toppings)s,%(toppings_count)s,%(quantity)s,'False',%(user_id)s, NOW());"
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
    def destroy(cls,data):
        query = "DELETE FROM topping where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)


