from flask import Blueprint, render_template
from models import Group, BaseStock
from app import db

groups_bp = Blueprint("groups", __name__, url_prefix="/groups")

@groups_bp.route("/")
def all_groups():
    groups = Group.query.all()
    return render_template("groups.html", groups=groups)


@groups_bp.route("/<int:group_id>", methods=["DELETE"])
def delete_group(group_id):
    group = Group.query.get_or_404(group_id)
    stock_parts = BaseStock.query.filter_by(group_id=group.id).all()
    for part in stock_parts:
        lathe_parts = part.lathe_stocks[0]
        if lathe_parts:
            db.session.delete(lathe_parts)
        db.session.delete(part) 
    db.session.delete(group)
    db.session.commit()
    return "", 204