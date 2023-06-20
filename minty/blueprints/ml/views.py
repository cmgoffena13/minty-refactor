import numpy as np
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from sqlalchemy import delete

from minty.blueprints.ml.forms import CreateNewModel
from minty.blueprints.ml.view_utils import (
    create_active_forms,
    create_delete_forms,
    is_active_bool,
    is_active_text,
)
from minty.db_utils import get_models_ongoing_accuracy
from minty.extensions import db
from minty.models import AccuracyHistory, Classifier

ml_bp = Blueprint(name="ml", import_name=__name__, template_folder="templates")


@ml_bp.route("/models", methods=["GET", "POST"])
def models():
    form = CreateNewModel()
    models = Classifier.query.order_by(Classifier.classifier_id.asc()).all()
    accuracy_dict = get_models_ongoing_accuracy()
    extracted_models = []
    for model in models:
        model_instance = model.load_model(model.classifier_name)
        model_instance.ongoing_accuracy = accuracy_dict.get(model.classifier_name)
        extracted_models.append(model_instance)

    delete_forms = create_delete_forms(models=models)
    active_forms = create_active_forms(models=models)
    models_data = zip(extracted_models, delete_forms, active_forms, models)

    if form.validate_on_submit():
        new_model = Classifier(classifier_name=str(form.classifier_name.data))
        new_model.train(
            date_filter=form.date_filter.data,
            feature_importance_threshold=form.feature_importance_threshold.data,
            training_split=float(form.training_split.data),
        )
        new_model.save_model()
        db.session.add(new_model)
        db.session.commit()
        flash(
            f'Created new model: "{new_model.classifier_name}" - Accuracy: {new_model.training_accuracy}'
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
    models_data = zip(extracted_models, delete_forms, active_forms, models)

    for delete_form in delete_forms:
        if delete_form.validate_on_submit():
            model = Classifier.get_by_classifier_name(
                classifier_name=delete_form.classifier_name.data
            )
            delete_query = delete(AccuracyHistory).where(
                AccuracyHistory.classifier_id == model.classifier_id
            )
            db.session.execute(delete_query)
            db.session.delete(model)
            db.session.commit()
            flash(f'Deleted model: "{model.classifier_name}"')
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
    models_data = zip(extracted_models, delete_forms, active_forms, models)

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
                flash(f'Updated model "{active_form.classifier_name.data}" to {t}')
            return redirect(url_for("ml.models", form=form, models_data=models_data))


@ml_bp.route("/models/batch-predict/", methods=["POST"])
def predict_batch():
    transactions = request.json["transactions"]

    current_model_record = Classifier.query.filter_by(is_active=True).first()
    current_model = current_model_record.load_model(
        current_model_record.classifier_name
    )

    response_dict = dict()
    for transaction in transactions:
        transaction_id = list(transaction.keys())[0]
        transaction_data = list(transaction.values())[0]
        transaction_description_v = current_model.vectorizer.transform(
            [transaction_data["transaction_description"]]
        )
        transaction_amount_a = np.array(transaction_data["transaction_amount"]).reshape(
            -1, 1
        )
        account_id_a = np.array(transaction_data["account_id"]).reshape(-1, 1)

        features = np.concatenate(
            (
                transaction_description_v.toarray(),
                transaction_amount_a,
                account_id_a,
            ),
            axis=1,
        )
        # if current_model.features_remove is not None:
        #    features = np.delete(features, current_model.features_remove, axis=1)

        prediction = current_model.classify(transaction_features=features)
        response_dict[int(transaction_id)] = int(prediction)

    response_json = {"predictions": response_dict}
    return jsonify(response_json)
