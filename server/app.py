#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db,render_as_batch=True)

db.init_app(app)


@app.route('/')
def home():
    return ''
@app.route('/campers',methods=['GET','POST'])
def campers():
    if request.method=='GET':
        campers=[]
        for camper in Camper.query.all():
            camper_dict={
                "name":camper.name,
                "age": camper.age
            }
            campers.append(camper_dict)
            response=make_response(
                jsonify(campers),
                200
            )
        return response
    elif request.method=='POST':
        new_camper=Camper(
            name=request.form.get("name"),
            age=request.form.get("age")
        )
        db.session.add(new_camper)
        db.session.commit()
        camper_dict=new_camper.to_dict()
        response=make_response(
            camper_dict,
            201
        )
        return response
if __name__ == '__main__':
    app.run(port=5555, debug=True)
