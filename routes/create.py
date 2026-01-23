from flask import Blueprint, render_template, request, jsonify
from app import db
from models import Group, BaseStock, LatheStock, Customer

create_bp = Blueprint("create", __name__, url_prefix="/create")

@create_bp.route("/", methods=["GET"])
def create_group():
    group_id = request.args.get("group_id")
    group = Group.query.get(group_id) if group_id else None
    return render_template("create.html", group=group)


@create_bp.route("/save-parts", methods=["POST"])
def save_parts():
    data = request.json
    try:
        group = Group(group_name=data["group"]["group_name"])
        db.session.add(group)
        db.session.flush()  # get group.id

        for part in data["parts"]:
            customer = Customer.query.filter_by(company_name=part["base_stock"]["customer_id"]).first()
            if not customer:
                customer = Customer(company_name=part["base_stock"]["customer_id"])
                db.session.add(customer)
                db.session.commit()

            base = BaseStock(
                group_id=group.id,
                customer_id=customer.id,
                external_part_number=part["base_stock"]["external_part_number"],
                external_part_name=part["base_stock"]["external_part_name"],
                quantity=part["base_stock"]["quantity"],
                extra_parts=part["base_stock"]["extra_parts"],
                revision_number=part["base_stock"]["revision_number"],
                approval_engineer=part["base_stock"].get("approval_engineer"),
            )
            db.session.add(base)
            db.session.flush()

            lathe = LatheStock(
                id=base.id,
                overall_outer_dimensions=part["lathe_stock"]["overall_outer_dimensions"],
                overall_length=part["lathe_stock"]["overall_length"],
                bar_or_slug=part["lathe_stock"]["bar_or_slug"],
                workholding_grip=part["lathe_stock"].get("workholding_grip"),
                clearance=part["lathe_stock"].get("clearance"),
                cutoff_blade_width=part["lathe_stock"].get("cutoff_blade_width"),
                clean_axial_stock=part["lathe_stock"].get("clean_axial_stock"),
                clean_radial_stock=part["lathe_stock"].get("clean_radial_stock"),
                round_outer_dimensions=part["lathe_stock"].get("round_outer_dimensions"),
                round_length=part["lathe_stock"].get("round_length")
            )
            db.session.add(lathe)

        db.session.commit()
        return jsonify({"status": "ok"}), 201

    except Exception as e:
        db.session.rollback()
        print("error"+ e)
        return jsonify({"error": str(e)}), 400