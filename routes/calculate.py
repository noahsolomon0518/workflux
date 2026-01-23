from flask import Blueprint, render_template, request, jsonify
from models import Group

calculate_bp = Blueprint("calculate", __name__)

@calculate_bp.route("/", methods=["GET"])
def calculate_page():
    groups = Group.query.order_by(Group.group_name).all()
    return render_template("calculate.html", groups=groups)


@calculate_bp.route("/run", methods=["POST"])
def run_calculation():
    data = request.json
    group_ids = data.get("group_ids", [])

    # 🔧 placeholder logic
    groups = Group.query.filter(Group.id.in_(group_ids)).all()

    # TODO: calculation logic here
    return jsonify({
        "selected_groups": [g.group_name for g in groups]
    })
