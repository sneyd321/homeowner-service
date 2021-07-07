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
    service = zookeeper.get_service("homeowner-gateway")
 
    if not service:
        return Response(response="Error: Zookeeper down", status=503)

    form = HomeownerForm()
    return render_template("signupTemplate.html", form=form, fields=list(form._fields.values()), conflict="", url="http://" + service + "/homeowner-gateway/v1/")

    

@homeowner.route("/", methods=["POST"])
def sign_up():
    service = zookeeper.get_service("homeowner-gateway")

    if not service:
        return Response(response="Error: Zookeeper down", status=503)

    form = HomeownerForm(request.form)
    attrs = list(form._fields.values())
    print(vars(request))



    
    if not request.form or "firstName" not in request.form or "lastName" not in request.form or "email" not in request.form or "phoneNumber" not in request.form or "password" not in request.form or "reTypePassword" not in request.form:
        return render_template("signupTemplate.html", 
        form=form, 
        fields=attrs, 
        conflict="Error Invalid Request Data", 
        url="http://" + service + "/homeowner-gateway/v1/")

    
    if not form.validate():
        return render_template("signupTemplate.html", 
        form=form, 
        fields=attrs, 
        conflict="", 
        url="http://" + service + "/homeowner-gateway/v1/")


    homeowner = Homeowner(**request.form)
    homeowner.generatePasswordHash(request.form.get("password"))
    if not homeowner.insert():
        return render_template("signupTemplate.html", 
        form=form, 
        fields=attrs, 
        conflict="Error: Account already exists", 
        url="http://" + service + "/homeowner-gateway/v1/")

    return Response(response="FormComplete", status=201)
   



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
        homeowner = Homeowner.verify_auth_token(bearer[7:])
        if homeowner:
            return jsonify(homeowner.getId())
        return Response(response="Not Found", status=404)
    return Response(response="Not Authenticated", status=401)


@homeowner.route("/Login", methods=["POST"])
def login():
    if request.authorization == None:
        return Response(response="Missing Authrozation", status=400)
  
    homeowner = Homeowner.query.filter(Homeowner.email == request.authorization.username).first()
    if not homeowner:
        return Response(response="Error account not found", status=404)
        
    if homeowner.verifyPassword(request.authorization.password):
        return jsonify(homeowner.getAuthToken())
    return Response(response="Error invalid account credentials", status=401)

    
    
@homeowner.route("Homeowner/<int:homeownerId>/imageURL", methods=["PUT"])
def update_imageURL(homeownerId):
    homeownerData = request.get_json()
    if "imageURL" in homeownerData and "homeownerId" in homeownerData:
        homeowner = Homeowner.query.get(homeownerData["homeownerId"])
        homeowner.imageURL = homeownerData["imageURL"]
        if homeowner.update():
            return Response(status=200)
        return Response(response="Error: Failed to update tenant", status=400)
    else:
        return Response(response="Error: Invalid Request", status=400)