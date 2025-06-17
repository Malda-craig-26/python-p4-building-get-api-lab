#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakeries = Bakery.query.all()
    bakeries_list = [
        {
            "id": bakery.id,
            "name": bakery.name,
            "created_at": bakery.created_at
        }
        for bakery in all_bakeries
    ]
    return jsonify(bakeries_list)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = db.session.get(Bakery, id)
    if not bakery:
        return jsonify({'error': 'Bakery not found'}), 404

    baked_goods_list = [
        {
            'id': bg.id,
            'name': bg.name
        }
        for bg in bakery.baked_goods
    ]
    return jsonify({
        'id': bakery.id,
        'name': bakery.name,
        'created_at': bakery.created_at.isoformat() if bakery.created_at else None,
        'baked_goods': baked_goods_list
    })

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    result = [
        {
            "id": bg.id,
            "name": bg.name,
            "price": bg.price,
            "created_at": bg.created_at.isoformat() if bg.created_at else None
        } for bg in baked_goods
    ]
    return jsonify(result), 200


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    # Query to get the most expensive baked good
    baked_good = BakedGood.query.order_by(desc(BakedGood.price)).limit(1).first()
    
    if baked_good:
        return jsonify({
            'id': baked_good.id,
            'name': baked_good.name,
            'price': baked_good.price,
            'created_at': baked_good.created_at.isoformat() if baked_good.created_at else None
        })
    else:
        return jsonify({'error': 'No baked goods found'}), 404
if __name__ == '__main__':
    app.run(port=5555, debug=True)
