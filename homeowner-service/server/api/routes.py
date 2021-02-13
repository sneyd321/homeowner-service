from . import homeowner
from flask import request, Response, jsonify, render_template, abort
from server.api.models import Homeowner
from server.forms.HomeownerForm import HomeownerForm


@homeowner.route("/SignUp", methods=["GET", "POST"])
def get_sign_in_form():
    form = HomeownerForm()
    attrs = list(form._fields.values())
    if request.method == 'POST':
        print((request.data))
        homeowner = Homeowner(firstName=request.form.get("firstName"), lastName=request.form.get("lastName"), 
        email=request.form.get("email"), password=request.form.get("password"), phoneNumber=request.form.get("phoneNumber"))
        homeowner.generatePasswordHash(request.form.get("password"))
        if homeowner.insert():
            return "<h1>Account successfully created</h1>"
        return render_template("signupTemplate.html", form=form, fields=attrs[:-1], conflict="Error: Account already exists")
    return render_template("signupTemplate.html", form=form, fields=attrs[:-1], conflict="")


@homeowner.route("/Homeowner", methods=["GET"])
def get_homeowner():
    bearer = request.headers.get("Authorization")
    if bearer:
        homeowner = Homeowner.verify_auth_token(bearer[7:])
        if homeowner:
            return jsonify(homeowner.toJson())
        return Response(response="Not Found", status=404)
    return Response(response="Not Authenticated", status=401)



@homeowner.route("/login", methods=["POST"])
def login():
    try:
        homeowner = Homeowner.query.filter(Homeowner.email == request.authorization.username).first()
    except AttributeError:
        return Response(response="Error invalid account credentials", status=401)
    if homeowner:
        if homeowner.verifyPassword(request.authorization.password):
            return jsonify(homeowner.toJson())
        return Response(response="Error invalid account credentials", status=401)
    return Response(response="Error account not found", status=404)
    
