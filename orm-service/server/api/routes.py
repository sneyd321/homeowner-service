from . import homeowner
from flask import request, Response, jsonify, render_template
from server.api.models import Homeowner
from server.forms.HomeownerForm import HomeownerForm


@homeowner.route("/", methods=["GET"])
def get_sign_in_form():
    form = HomeownerForm()
    attrs = list(form._fields.values())
    return render_template("signupTemplate.html", form=form, fields=attrs[:-1])


@homeowner.route("/Homeowner", methods=["POST"])
def create_homeowner():
    print("PING")
    data = request.form
    print(data)
    
    return data
    """
    data = request.get_json()
    homeowner = Homeowner(data)
    homeowner.generatePasswordHash(data["password"])
    if homeowner.insert():
        return jsonify(homeowner.toJson())
    return Response(response="Error: Email already exists in database", status=409)
   """

@homeowner.route("/Homeowner/<int:id>", methods=["GET"])
def load_homeowner(id):
    homeowner = Homeowner.query.get(id)
    if homeowner:
        return jsonify(homeowner.toJson())
    return Response(response="No content", status=204)


@homeowner.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        homeowner = Homeowner.query.filter(Homeowner.email == data["email"]).first()
        if homeowner and homeowner.verifyPassword(data["password"]):
            return jsonify(homeowner.toJson())
        return Response(response="Error account not found", status=204)
    except KeyError:
        return Response(response="Error: Data in invalid format", status=400)

@homeowner.route("/Homeowner/<int:id>", methods=["DELETE"])
def remove_homeowner(id):
    homeowner = Homeowner.query.get(id)
    if homeowner:
        homeowner.delete()
        return Response(response="Successfully deleted", status=200)
    return Response(response="No content", status=204)
  