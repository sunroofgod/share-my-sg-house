from flask_cors import CORS, cross_origin
from flask import Flask, request, Response
from models import end_point_action

# Instantiate object app
app = Flask(__name__)
# Add cross origin security
CORS(app)

# connect to database
from db_manager import db, setup_database
if (db == None):
    app.logger.error("Not able to connect to db")
    raise Exception("ERROR")
setup_database(db)

# defintion of the various pages
class home_page(end_point_action):
    def __call__(self, *args):
        self.response = Response("welcome to home page",status=200)
        return self.response
app.add_url_rule("/", "a", home_page(None))

if __name__ == "__main__":
    app.run()