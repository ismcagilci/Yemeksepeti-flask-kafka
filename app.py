import json

from flask import request,Flask
import config
import database
from flask_sqlalchemy import SQLAlchemy
from producer import send_kafka
from consumer import get_consumer
import json


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


#Models(We can seperate models but for task i used one model)
class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    restaurant = db.Column(db.String(100))
    food = db.Column(db.String(100))
    category = db.Column(db.String(100))
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    status = db.Column(db.Integer)



@app.route('/', methods=['GET'])
def fetch():
    orders = database.get_all(Orders)
    all_orders = []
    for order in orders:
        new_order = {
            "id": order.id,
            "restaurant": order.restaurant,
            "food": order.food,
            "category": order.category,
            "username":order.username,
            "email":order.email,
            "status":order.status
        }

        all_orders.append(new_order)
    return json.dumps(all_orders), 200


@app.route('/add', methods=['POST'])
def add_order():
    data = request.get_json()
    restaurant = data['restaurant']
    food = data['food']
    category = data['category']
    username = data["username"]
    email = data["email"]
    status = 0
    object_id = database.add_instance(Orders,restaurant=restaurant, food=food, category=category, username=username,email=email, status=status,db=db)
    data["id"] = object_id
    send_kafka(data)
    return json.dumps("Added"), 200


@app.route('/complete', methods=['GET'])
def complete_order():
    get_orders = get_consumer()
    for order in get_orders:
        try:
            print(order)
            order = json.loads(order.value)
            database.edit_instance(Orders, id=order.get("id"), status=1, db=db)
        except:
            pass
    return json.dumps("Order was completed"), 200


@app.route('/remove/<order_id>', methods=['DELETE'])
def remove(order_id):
    database.delete_instance(Orders, id=order_id,db=db)
    return json.dumps("Deleted"), 200

@app.route('/remove_all', methods=['DELETE'])
def remove_all():
    database.delete_all(Orders,db=db)
    return json.dumps("All deleted"), 200




@app.route('/edit/<order_id>', methods=['PATCH'])
def edit(order_id):
    data = request.get_json()
    new_food = data['food']
    database.edit_instance(Orders, id=order_id, food=new_food,db=db)
    return json.dumps("Edited"), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
