from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, text
from flask_restful import Resource, Api
from flask_cors import CORS  # Import CORS if needed

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app if you need it
api = Api(app)
db_connect = create_engine('sqlite:///crud.db')

# Route to serve the HTML file
@app.route('/')
def index():
    return render_template('index.html')

# Initialize the database
def init_db():
    conn = db_connect.connect()
    conn.execute(text('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    '''))
    conn.close()

init_db()

class Users(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM user")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        conn.close()
        return jsonify(result)

    def post(self):
        conn = db_connect.connect()
        name = request.json['name']
        email = request.json['email']

        conn.execute(text("INSERT INTO user (name, email) VALUES (:name, :email)"), {'name': name, 'email': email})

        query = conn.execute("SELECT * FROM user ORDER BY id DESC LIMIT 1")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        conn.close()
        return jsonify(result)

class UserById(Resource):
    def get(self, user_id):
        conn = db_connect.connect()
        query = conn.execute(text("SELECT * FROM user WHERE id = :id"), {'id': user_id})
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        conn.close()
        return jsonify(result)

    def delete(self, user_id):
        conn = db_connect.connect()
        conn.execute(text("DELETE FROM user WHERE id = :id"), {'id': user_id})
        conn.close()
        return {"status": "success"}

api.add_resource(Users, '/users') 
api.add_resource(UserById, '/users/<user_id>')

if __name__ == '__main__':
    app.run(debug=True)
