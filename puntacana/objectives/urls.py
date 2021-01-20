from django.urls import path

from . import views

urlpatterns = [
    path('', views.ObjectiveListView.as_view(), name='objective-list'),
    path('objetivos/<int:pk>',
         views.ObjectiveCalculatorView.as_view(), name='objective-detail'),
]
