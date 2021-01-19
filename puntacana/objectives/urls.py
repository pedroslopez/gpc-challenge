from django.urls import path

from . import views

urlpatterns = [
    path('', views.ObjectiveListView.as_view(), name='index')
]
