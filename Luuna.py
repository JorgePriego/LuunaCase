# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.


    Make a REST API to administer Users and Products. A User should have basic info such as email, name and password. 
    A Product should have basic info such as name, price and brand.
    This app should authenticate the Users and allow then to do CRUD operations on Products such as changing the name, brand and adjusting prices.
    You should manage auth through JWT.
    The app should as well send notifications to User when creating an account, updating his/her info, deleting his/her account.

"""

from flask import Flask
from flask_restful import Api, Resource, reqparse
import mysql.connector

mydb = mysql.connector.connect(
    host ="localhost",
    user="Jorge",
    passwd="pass")

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE database")

mycursor.execute("CREATE TABLE users (name VARCHAR(255), password VARCHAR(255), email VARCHAR (255))")

mycursor.execute("CREATE TABLE products (name VARCHAR(255), price FLOAT, brand VARCHAR (255))")


app = Flask (__name__)
api = Api(app)

class User(Resource):
    
    def get(self,name):
        "Checar en base de datos si existe y tomarlo"
        
        return "User not found", 404
        
    def post(self, name): 
        parser = reqparse.RequestParser()
        parser.add_argument("password")
        parser.add_argument("email")
        
        args= parser.parse_args()
        
        sql = "INSERT INTO users (name, password, email) VALUES (%s,%s,%s)"
        val = name, args["password"], args["email"]
        mycursor.execute(sql,val)
        
        mydb.commit()
        
        "Manda correo de aviso"
        return 201
        
    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("password")
        parser.add_argument("email")
        
        args= parser.parse_args()
        
        sql = "UPDATE users SET password = '"+args["password"]+"' WHERE name = '"+name+"'"
        mycursor.execute(sql)
        
        mydb.commit()
        "Manda correo de aviso"
        return 201
        
        
    def delete(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("email")
        
        args= parser.parse_args()
        
        sql = "DELETE FROM users WHERE email = '"+args["email"]+"'"
        mycursor.execute(sql)
        mydb.commit()

        "Manda correo de aviso"
        return 201


class Product(Resource):
    
    def get(self,name):
        "Checar en base de datos si existe y tomarlo"
        
        return "User not found", 404
        
    def post(self, name): 
        parser = reqparse.RequestParser()
        parser.add_argument("price")
        parser.add_argument("brand")
        
        args= parser.parse_args()
        
        sql = "INSERT INTO products (name, price, brand) VALUES (%s,%f,%s)"
        val = name, args["price"], args["brand"]
        mycursor.execute(sql,val)
        
        mydb.commit()
        return 201
        
    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("price")
        parser.add_argument("brand")
        
        args= parser.parse_args()
        
        sql = "UPDATE products SET price = '"+args["price"]+"' WHERE name = '"+name+"'"
        mycursor.execute(sql)
        
        mydb.commit()
        return 201
        
        
    def delete(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("brand")
        
        args= parser.parse_args()
        
        sql = "DELETE FROM products WHERE brand = '"+args["brand"]+"'"
        mycursor.execute(sql)
        mydb.commit()

        return 201        
    
api.add_resource(User, "/user/<string:name>")

app.run(debug=True)