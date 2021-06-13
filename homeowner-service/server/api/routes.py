from . import homeowner
from flask import request, Response, jsonify, render_template, abort
from server.api.models import Homeowner
from server.api.forms import HomeownerForm
from server.api.RequestManager import Zookeeper


zookeeper = Zookeeper()

def get_homeowner_gateway():
    return "192.168.0.108:8080"




@homeowner.route("/")
def get_sign_up_form():
    global zookeeper
    service = zookeeper.get_service("homeowner-gateway")
    service = get_homeowner_gateway()
    if service:
        form = HomeownerForm()
        return render_template("signupTemplate.html", form=form, fields=list(form._fields.values()), conflict="", url="http://" + service + "/homeowner-gateway/v1/")
    return Response(response="Error: Zookeeper down", status=503)

    

@homeowner.route("/", methods=["POST"])
def sign_up():
    global zookeeper
    service = zookeeper.get_service("homeowner-gateway")
    service = get_homeowner_gateway()
    if service:
        form = HomeownerForm(request.form)
        attrs = list(form._fields.values())
        if form.validate():
            homeowner = Homeowner(**request.form)
            homeowner.generatePasswordHash(request.form.get("password"))
            if homeowner.insert():
                return Response(response="FormComplete", status=201)
            return render_template("signupTemplate.html", form=form, fields=attrs, conflict="Error: Account already exists", url="http://" + service + "/homeowner-gateway/v1/")
        return render_template("signupTemplate.html", form=form, fields=attrs, conflict="", url="http://" + service + "/homeowner-gateway/v1/")
    return Response(response="Error: Zookeeper down", status=503)
   

@homeowner.route("/Homeowner/<int:homeownerId>")
def get_homeowner_by_id(homeownerId):
    homeowner = Homeowner.query.get(homeownerId)
    if homeowner:
        return jsonify(homeowner.toJson())
    return Response(response="Not Found", status=404)



@homeowner.route("/Homeowner", methods=["GET"])
def get_homeowner():
    bearer = request.headers.get("Authorization")
    if bearer:
        homeowner = Homeowner.verify_auth_token(bearer[7:])
        if homeowner:
            return jsonify(homeowner.toJson())
        return Response(response="Not Found", status=404)
    return Response(response="Not Authenticated", status=401)


@homeowner.route("/Verify", methods=["GET"])
def verify_homeowner():
    bearer = request.headers.get("Authorization")
    if bearer:
        print("Homeowner", bearer, flush=True)
        
        homeowner = Homeowner.verify_auth_token(bearer[7:])
        
        if homeowner:
            return jsonify(homeowner.getId())
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
    
