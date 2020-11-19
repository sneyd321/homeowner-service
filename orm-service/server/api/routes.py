from . import homeowner
from flask import request, Response, jsonify


from server.api.models import Homeowner, HomeownerLocation




@homeowner.route("/Homeowner", methods=["POST"])
def create_homeowner():
    data = request.get_json()
    try:
        homeowner = Homeowner(data)
        homeowner.generatePasswordHash(data["password"])
        if homeowner.insert():
            return jsonify(homeowner.toJson)
        return Response(response="Error: Conflict in database", status=409)
    except KeyError:
        return Response(response="Error: Data in invalid format", status=400)
    

@homeowner.route("/Homeowner/<int:id>", methods=["GET"])
def load_homeowner(id):
    homeowner = Homeowner.query.get(id)
    if homeowner:
        return jsonify(homeowner.toJson())
    return Response(response="No content", status=204)

@homeowner.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    homeowner = Homeowner.query.filter(Homeowner.email == data["email"]).first()
    if homeowner and homeowner.verifyPassword(data["password"]):
        return jsonify(homeowner.toJson())
    return Response(response="Error account not found", status=401)

@homeowner.route("/Homeowner/<int:id>", methods=["DELETE"])
def remove_homeowner(id):
    data = request.get_json()
    try:
        homeowner = Homeowner.query.get(id)
        if homeowner:
            homeowner.delete()
            return Response(response="Successfully deleted", status=200)
        return Response(response="No content", status=204)
    except KeyError:
        return Response(response="Error: Data in invalid format", status=400)