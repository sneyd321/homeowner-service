from . import homeowner
from flask import request, Response, jsonify, render_template, abort
from server.api.models import Homeowner, HomeownerLocation
from server.api.forms import HomeownerForm, HomeownerLocationForm
from server.api.RequestManager import Zookeeper
from server import app


zookeeper = Zookeeper()


def get_homeowner_gateway():
    return "34.107.132.144"

@homeowner.route("/")
def get_sign_up_form():
    service = get_homeowner_gateway()
 
    if not service:
        return Response(response="Error: Homeowner Service Currently Unavailable", status=503)

    form = HomeownerForm()
    return render_template("signupTemplate.html", form=form, fields=list(form._fields.values()), conflict="", url="http://" + service + "/homeowner-gateway/v1/")

    

@homeowner.route("/", methods=["POST"])
def sign_up():
  
    service = get_homeowner_gateway()

    if not service:
        return Response(response="Error: Zookeeper down", status=503)

    form = HomeownerForm(request.form)
    attrs = list(form._fields.values())
    
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
    homeownerId = Homeowner.query.filter(Homeowner.email == homeowner.email).first().getId()["homeownerId"]
    homeowner.close_session()
    print(homeownerId)
    return Response(response="HomeownerLocation/" + str(homeownerId), status=201)






@homeowner.route("HomeownerLocation/<int:homeownerId>")
def get_homeowner_location_form(homeownerId):
   
    service = get_homeowner_gateway()
    if not service:
        return Response(response="Error: Homeowner Service Not Available", status=503)

    form = HomeownerLocationForm()
    return render_template("OntarioHomeownerLocation.html", form=form, fields=list(form._fields.values()), conflict="", url="http://" + service + "/homeowner-gateway/v1/HomeownerLocation/" + str(homeownerId))





@homeowner.route("HomeownerLocation/<int:homeownerId>", methods=["POST"])
def create_homeowner_location(homeownerId):
 
    service = get_homeowner_gateway()
    if not service:
        return Response(response="Error: Zookeeper down", status=503)

    form = HomeownerLocationForm(request.form)
    attrs = list(form._fields.values())
    if not request.form or "streetNumber" not in request.form or "streetName" not in request.form or "city" not in request.form or "province" not in request.form or "postalCode" not in request.form or "unitNumber" not in request.form:
        return render_template("OntarioHomeownerLocation.html", 
        form=form, 
        fields=attrs, 
        conflict="Error: Invalid Request Data", 
        url="http://" + service + "/homeowner-gateway/v1/HomeownerLocation/" + str(homeownerId))

    
    if not form.validate_on_submit():
        return render_template("OntarioHomeownerLocation.html", 
        form=form, 
        fields=attrs, 
        conflict="", 
        url="http://" + service + "/homeowner-gateway/v1/HomeownerLocation/" + str(homeownerId))


    homeownerLocation = HomeownerLocation(homeownerId=homeownerId, **request.form)
    if not homeownerLocation.insert():
        return render_template("OntarioHomeownerLocation.html", 
        form=form, 
        fields=attrs, 
        conflict="Error: Adding homeowner location", 
        url="http://" + service + "/HomeownerLocation/" + str(homeownerId))

    return Response(response="HomeownerComplete/" + str(homeownerId), status=201)




@homeowner.route("HomeownerComplete/<int:homeownerId>", methods=["POST"])
def homeowner_complete(homeownerId):
    homeowner = Homeowner.query.get(homeownerId)
    homeowner.isComplete = True
    if homeowner.update():
        return Response(response="FormComplete", status=201)
    return Response(response="Error: Failed to update", status=409)











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
        return Response(response="Error: Invalid Account Credentials", status=401)
        
    if not homeowner.verifyPassword(request.authorization.password):
        return Response(response="Error: Invalid Account Credentials", status=401)

    return jsonify(homeowner.getAuthToken())
    
@homeowner.route("Homeowner/<int:homeownerId>/imageURL", methods=["PUT"])
def update_imageURL(homeownerId):
    homeownerData = request.get_json()
    if not homeownerData or "imageURL" not in homeownerData:
        return Response(response="Error: Invalid Request", status=400)
    homeowner = Homeowner.query.get(homeownerId)
    homeowner.imageURL = homeownerData["imageURL"]
    if homeowner.update():
        return Response(status=200)
    return Response(response="Error: Failed to update tenant", status=400)


