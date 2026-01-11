from flask import Flask, render_template, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:password@localhost:5432/part_tracking"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# In-memory storage (will be replaced with a database later)
parts = []
material_cache = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parts')
def parts_list():
    return render_template('parts.html', parts=parts)



if __name__ == '__main__':
    app.run(debug=True, port=5000)
