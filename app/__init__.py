from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    from .blueprints.users import main_routes as users_routes 
    from .blueprints.dashboard_principal.sesion import main_routes as sesion_routes
    from .blueprints.dashboard_principal.transcripcion import main_routes as trans_routes
    from .blueprints.dashboard_principal.resumen import main_routes as resumen_routes  
    from .blueprints.dashboard_principal.feedback import main_routes as feedback_routes

    app.register_blueprint(users_routes)
    app.register_blueprint(sesion_routes)
    app.register_blueprint(trans_routes) 
    app.register_blueprint(resumen_routes)
    app.register_blueprint(feedback_routes) 



    return app
