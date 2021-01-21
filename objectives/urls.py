from django.urls import path

from . import views

urlpatterns = [
    path('',
         views.ObjectiveListView.as_view(), name='objective-list'),
    path('objetivos/nuevo/',
         views.ObjectiveCreateView.as_view(), name='objective-add'),
    path('objetivos/<int:pk>',
         views.ObjectiveCalculatorView.as_view(), name='objective-detail'),
    path('objetivos/<int:pk>/editar',
         views.ObjectiveUpdateView.as_view(), name='objective-update'),
    path('objetivos/<int:pk>/eliminar',
         views.ObjectiveDeleteView.as_view(), name='objective-delete'),
]
