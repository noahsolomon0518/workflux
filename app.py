from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, Customer
from urllib.parse import quote_plus

PW = quote_plus('temp')

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://noahsolomon:{PW}@10.0.0.122:5432/workflux"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


def register_blueprints():
    from routes.create import create_bp
    from routes.groups import groups_bp
    from routes.calculate import calculate_bp
    app.register_blueprint(create_bp, url_prefix="/create")
    app.register_blueprint(groups_bp, url_prefix="/groups")
    app.register_blueprint(calculate_bp, url_prefix="/calculate")
    return app

@app.route("/")
def base():
    return render_template('base.html')

@app.route("/customers")
def customers():
    customers = Customer.query.order_by(Customer.company_name).all()
    return {
        "customers": [c.company_name for c in customers]
    }

app = register_blueprints()
db.init_app(app)
if __name__ == '__main__':
    app.run(debug=True, port=5000)
