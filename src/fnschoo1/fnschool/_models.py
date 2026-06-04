from django.db.models.fields.related import RelatedField


def get_model_field_names(model):
    field_names = []
    for field in model._meta.get_fields():
        if not field.is_relation:
            field_names.append(field.name)
        else:
            if isinstance(field, RelatedField):
                related_model = field.related_model
                field_names.append(f"{field.name}_id")
                for rel_field in related_model._meta.local_fields:
                    if not rel_field.is_relation:
                        field_names.append(f"{field.name}__{rel_field.name}")

    return field_names


# The end.
