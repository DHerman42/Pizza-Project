from flask_app.config import connectToMySQL
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db_name ="pizzatime" # named the database after our group project assignement
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.city = data['city']
        self.state = data['state']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO user (first_name,last_name.email,password,city,state) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,%(city)s,%(state)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_user_topping(cls,data):
        query = "SELECT * FROM user LEFT JOIN topping on user.id = topping.user_id;"
        results = connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM user;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_email(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_id(cls,data):
        query = "SELECT * FROM user where id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])


    @classmethod
    def delete_user(cls,data):
        query = "DELETE FROM user where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query,user)
        if len(user['email']) < 1:
            flash("Please enter an email", "register")
            is_valid=False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email! Enter valid email","register")
            is_valid=False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid=False
        if (user['password']) != user["confirm_password"]:
            flash("Password does not match")
            is_valid=False
        return is_valid


