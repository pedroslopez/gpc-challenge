from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Objective


class ObjectiveListView(ListView):
    model = Objective
