from minty.blueprints.ml.forms import ActiveModel, DeleteModel


def create_delete_forms(models):
    delete_forms = list()
    for model in models:
        form = DeleteModel(prefix=f"{model.classifier_name}")
        delete_forms.append(form)
    return delete_forms


def create_active_forms(models):
    active_forms = list()
    for model in models:
        form = ActiveModel(prefix=f"{model.classifier_name}", active=model.is_active)
        active_forms.append(form)
    return active_forms


def is_active_text(value):
    _value = None
    if value.lower() == "true":
        _value = "active"
    if value.lower() == "false":
        _value = "not active"
    return _value


def is_active_bool(value):
    _bool = None
    if value.lower() == "false":
        _bool = False
    if value.lower() == "true":
        _bool = True
    return _bool
