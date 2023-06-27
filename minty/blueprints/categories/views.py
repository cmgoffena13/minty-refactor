from flask import Blueprint, render_template

from minty.models import CustomCategory

categories_bp = Blueprint(
    name="categories", import_name=__name__, template_folder="templates"
)


@categories_bp.route("/categories", methods=["GET"])
def categories():
    categories = CustomCategory.query.order_by(CustomCategory.custom_category_id).all()
    category_data = categories
    return render_template(
        template_name_or_list="categories/categories.html", category_data=category_data
    )
