from minty.blueprints.ml.forms import DeleteModel


def create_delete_forms(models):
    delete_forms = list()
    for model in models:
        form = DeleteModel(prefix=f"{model.classifier_name}")
        delete_forms.append(form)
    return delete_forms
