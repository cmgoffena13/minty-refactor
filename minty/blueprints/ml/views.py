from flask import Blueprint, flash, redirect, render_template, url_for

from minty.blueprints.ml.forms import CreateNewModel
from minty.blueprints.ml.view_utils import (
    create_active_forms,
    create_delete_forms,
    is_active_bool,
    is_active_text,
)
from minty.extensions import db
from minty.models import Classifier

ml_bp = Blueprint(name="ml", import_name=__name__, template_folder="templates")


@ml_bp.route("/models", methods=["GET", "POST"])
def models():
    form = CreateNewModel()
    models = Classifier.query.all()
    extracted_models = []
    for model in models:
        extracted_models.append(model.load_model(model.classifier_name))

    delete_forms = create_delete_forms(models=models)
    active_forms = create_active_forms(models=models)
    models_data = zip(extracted_models, delete_forms, active_forms)

    if form.validate_on_submit():
        new_model = Classifier(
            classifier_name=str(form.classifier_name.data)
            + "_"
            + str(form.date_filter.data),
            date_filter=form.date_filter.data,
        )
        new_model.train(date_filter=form.date_filter.data)
        new_model.save_model()
        db.session.add(new_model)
        db.session.commit()
        flash(
            f"Created new model: {new_model.classifier_name} - Accuracy: {new_model.accuracy}"
        )
        return redirect(url_for("ml.models", form=form, models_data=models_data))

    return render_template(
        template_name_or_list="ml/classifiers.html",
        title="ML",
        form=form,
        models_data=models_data,
    )


@ml_bp.route("/models/delete", methods=["POST"])
def delete_model():
    form = CreateNewModel()
    models = Classifier.query.all()
    extracted_models = []
    for model in models:
        extracted_models.append(model.load_model(model.classifier_name))

    delete_forms = create_delete_forms(models=models)
    active_forms = create_active_forms(models=models)
    models_data = zip(extracted_models, delete_forms, active_forms)

    for delete_form in delete_forms:
        if delete_form.validate_on_submit():
            model = Classifier.get_by_classifier_name(
                classifier_name=delete_form.classifier_name.data
            )
            db.session.delete(model)
            db.session.commit()
            flash(f"Deleted model: {model.classifier_name}")
            return redirect(url_for("ml.models", form=form, models_data=models_data))


@ml_bp.route("/models/update", methods=["POST"])
def update_model():
    form = CreateNewModel()
    models = Classifier.query.all()
    extracted_models = []
    for model in models:
        extracted_models.append(model.load_model(model.classifier_name))

    delete_forms = create_delete_forms(models=models)
    active_forms = create_active_forms(models=models)
    models_data = zip(extracted_models, delete_forms, active_forms)

    for active_form in active_forms:
        if active_form.validate_on_submit():
            current_model = Classifier.query.filter_by(is_active=True).first()

            if (
                current_model is not None
                and current_model.classifier_name != active_form.classifier_name.data
                and is_active_bool(str(active_form.active.data))
            ):
                flash(f"Cannot have two models active at the same time!")
            else:
                t = is_active_text(str(active_form.active.data))
                b = is_active_bool(str(active_form.active.data))
                model = Classifier.query.filter_by(
                    classifier_name=active_form.classifier_name.data
                ).first()
                setattr(model, "is_active", b)
                db.session.commit()
                flash(f"Updated model {active_form.classifier_name.data} to {t}")
            return redirect(url_for("ml.models", form=form, models_data=models_data))
