from flask import Flask, render_template
from flask_cors import CORS
from flask_migrate import Migrate
from models.database import db, ma
from events import pagos_event
from routes import register_blueprint
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return "SERVIDOR CORRIENDO"

@app.route('/invoice')
def invoice():
    return render_template('remito.html')

from routes import register_blueprint
register_blueprint(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

