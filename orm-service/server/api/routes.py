from . import homeowner
from flask import request, Response, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer  as Serializer


from server.api.models import Homeowner, HomeownerLocation


def confirm(userToken):
    serializer = Serializer("SECRET_KEY")
    try:
        token = serializer.loads(token.encode("utf-8"))
        if token["token"] == userToken:
            return True
        return False
    except:
        return False

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
        if confirm(user.token):
            return jsonify(user.toJson())
        return Response(response="Error: Invalid user credentials", status=401)
    return Response(response="Error: Record does not exist", status=404)


@homeowner.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    homeowner = Homeowner.query.filter(Homeowner.email == data["email"]).first()
    if homeowner and homeowner.verifyPassword(data["password"]):
        return jsonify({"token": homeowner.token})
   
    return Response(response="Error account not found", status=401)