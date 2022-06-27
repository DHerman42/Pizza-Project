from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)

class User:
    db_name ="pizzatime" # named the database after our group project assignement
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO user (first_name,last_name,email,password,address,city,state) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,%(address)s,%(city)s,%(state)s);"
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
        return results[0]
    
    @classmethod
    def edit_user(cls, data):
        query = "UPDATE user SET first_name = %(first_name)s, last_name = %(last_name)s, address = %(address)s, city = %(city)s, state = %(state)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)


    @classmethod
    def delete_user(cls,data):
        query = "DELETE FROM user where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_registration(user):
        is_valid = True
        query = "SELECT * FROM user WHERE email = %(email)s;"
        email = connectToMySQL(User.db_name).query_db(query,user)
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters", "register_first_name")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters", "register_last_name")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email! Enter valid email","register_email")
            is_valid=False
        elif not len(email) == 0:
            flash("Email is already entered", "register_email")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register_password")
            is_valid=False
        if (user['password']) != user["confirm_password"]:
            flash("Password does not match", "register_confirm")
            is_valid=False
        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query, data)
        if len(results) > 0:
            user = results[0]
            print(user)
        if len(results) == 0:
            flash("No matching email", "login_email")
            is_valid = False
        elif not bcrypt.check_password_hash(user['password'], data['password']):
            flash("Incorrect password entered", "login_password")
            is_valid = False
        if is_valid:
            return user
        else: 
            return is_valid
