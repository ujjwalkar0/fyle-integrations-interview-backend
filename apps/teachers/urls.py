from django.urls import path
from apps.teachers.views import ListAssignmentsView

urlpatterns = [
    path("assignments/", ListAssignmentsView.as_view(), name='teachers-assignments')
]
