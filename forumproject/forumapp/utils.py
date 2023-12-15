from django.apps import apps


def get_related_model():
    try:
        return apps.get_model('forumapp', 'RelatedModel')
    except LookupError:
        return None
