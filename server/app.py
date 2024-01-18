#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()
    return make_response ( bakery_serialized, 200  )

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    new_baked_good = BakedGood(name=data['name'], price=data['price'], bakery_id=data['bakery_id'])
    db.session.add(new_baked_good)
    db.session.commit()
    response_data = {"id": new_baked_good.id, "name": new_baked_good.name, "price": new_baked_good.price,
                     "bakery_id": new_baked_good.bakery_id, "created_at": str(new_baked_good.created_at)}

    response = make_response(jsonify(response_data), 201)
    response.headers['Content-Type'] = 'application/json'

    return response

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get(id)
    if bakery:
        data = request.form
        bakery.name = data.get('name', bakery.name)
        db.session.commit()
        response_data = {"id": bakery.id, "name": bakery.name, "created_at": str(bakery.created_at)}

        response = make_response(jsonify(response_data), 200)
        response.headers['Content-Type'] = 'application/json'

        return response

    return make_response(jsonify({"message": "Bakery not found"}), 404)

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)
    if baked_good:
        db.session.delete(baked_good)
        db.session.commit()
        return make_response(jsonify({"message": "Baked good deleted successfully"}), 200)

    return make_response(jsonify({"message": "Baked good not found"}), 404)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

if __name__ == '__main__':
    app.run(port=5555, debug=True)