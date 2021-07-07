from flask import Flask, Response
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql
pymysql.install_as_MySQLdb()

from kazoo.client import KazooClient, KazooState

zk = KazooClient()




db = SQLAlchemy()
app = Flask(__name__)

@app.route("/Health")
def health_check():
    return Response(status=200)

def create_app(env):
    global app

    config = Config(app)
    if env == "prod":
        app = config.productionConfig()
    elif env == "dev":
        app = config.developmentConfig()
    else:
        return None
    
    migrate = Migrate(app, db)
    db.init_app(app)
    zk.set_hosts(app.config["ZOOKEEPER"])
    zk.start()
    
    #Intialize modules
    from server.api.routes import homeowner
    app.register_blueprint(homeowner, url_prefix="/homeowner/v1")
    return app