from django.urls import path
from .views import connect_group, delete_document, delete_group, documents, groups, index, detail, registration

urlpatterns = [
    path("", index, name="index"),
    path("documents/<int:id>/", detail, name="document"), 
    path("register/", registration, name="register"),
    path("connect-group/", connect_group, name="connect_group"),
    path("documents/", documents, name="documents"),
    path("delete-document/<int:doc_id>/", delete_document, name="delete_document"),
    path("groups/", groups, name="groups"),
    path("delete-group/<int:group_id>/", delete_group, name="delete_group"),
]
