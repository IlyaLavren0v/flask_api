from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Auto(Resource):
    __tablename__ = 'stock'

    parser = reqparse.RequestParser()
    parser.add_argument('max_speed', type=float, required=True, help="This field cannot be blank")
    parser.add_argument('distance', type=float, required=True, help="This field cannot be blank")
    parser.add_argument('handler', type=str, required=True, help="This field cannot be blank")
    parser.add_argument('stock', type=str, required=True, help="This field cannot be blank")

    @classmethod
    def search_name(cls, name):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()

        select_query = 'SELECT * FROM {} WHERE name=?'.format(cls.__tablename__)
        row = cur.execute(select_query, (name,)).fetchone()

        conn.close()
        if row:
            return  {'name' : row[0], 'max_speed' : row[1], 'distance' : row [2], 'handler' : row[3], 'stock' : row[4]}

    @jwt_required()
    def get(self, name):
        auto = Auto.search_name(name)
        if auto:
            return {'auto' : auto}, 200
        return {'Error' : "Auto with that mark not found"}, 404

    @jwt_required()
    def post(self, name):
        if Auto.search_name(name):
            return {'Error' : "Auto with that mark {} exists".format(name)}, 400
        
        request_body = Auto.parser.parse_args()
        auto = {'name' : name, 'max_speed' : request_body['max_speed'], 'distance' : request_body['distance'], 'handler' : request_body['handler'], 'stock' : request_body['stock']}
       
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()

        insert_query = "INSERT INTO {} VALUES(?, ?, ?, ?, ?)".format(self.__tablename__)
        cur.execute(insert_query, (auto["name"], auto["max_speed"], auto["distance"], auto["handler"], auto["stock"] ))

        conn.commit()
        conn.close()

        return {'Message' : "Auto created"}, 201

    @jwt_required()
    def put(self, name):
        auto = Auto.search_name(name)
        if auto:      
            data = Auto.parser.parse_args()

            conn = sqlite3.connect('data.db')
            cur = conn.cursor()

            update_query = "UPDATE {} SET max_speed=?, distance=?, handler=?, stock=? WHERE name=?".format(self.__tablename__)
            cur.execute(update_query, (data['max_speed'], data['distance'], data['handler'], data['stock'], name,))

            conn.commit()
            conn.close()

            return {'Message' : "Auto updated"}, 202 
        return {'Error' : "Auto with that mark {} not found".format(name)}, 404

    @jwt_required()
    def delete(self, name):
        if Auto.search_name(name):
            conn = sqlite3.connect('data.db')
            cur = conn.cursor()

            delete_query = "DELETE FROM {} WHERE name=?".format(self.__tablename__)
            cur.execute(delete_query, (name,))

            conn.commit()
            conn.close()

            return {"Message" : "Auto deleted"}, 202
        return {"Error" : "Auto with that mark {} not found".format(name)}, 404



class AutoCollection(Resource):
    __tablename__ = 'stock'
    @jwt_required()
    def get(self):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()

        select_query = "SELECT * FROM {}".format(self.__tablename__)
        stock = []
        for line in cur.execute(select_query):
            stock.append({'name' : line[0], 'max_speed' : line[1], 'distance' : line[2], 'handler' : line[3], 'stock' : line[4]})
        
        conn.close()

        if stock:
            return {'stock' : stock }, 200
        return {'Error' : "No one autos found in DataBase"}, 400