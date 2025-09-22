from flask import Flask
from config import Config
from db import create_tables, drop_all_tables
from routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        # drop_all_tables()
        create_tables()
    
    register_routes(app)
    return app

if __name__=="__main__":
    app = create_app()
    app.run(debug=True)
