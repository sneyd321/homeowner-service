from . import homeowner
from flask import request, Response, jsonify


from server.api.models import Homeowner, HomeownerLocation


@homeowner.route("/Homeowner", methods=["POST"])
def create_homeowner():
    data = request.get_json()
    try:
        user = Homeowner(data)
        user.generatePasswordHash(data["password"])
        if user.insert():
            return Response(response="Account successfully created", status=201)
        return Response(response="Error: Conflict in database", status=409)
    except KeyError:
        return Response(response="Error: Data in invalid format", status=400)
    

@homeowner.route("/Homeowner/<int:id>", methods=["GET"])
def load_homeowner(id):
    user = Homeowner.query.get(id)
    if user:
        return jsonify(user.toJson())
    return Response(response="Error: Record does not exist", status=401)