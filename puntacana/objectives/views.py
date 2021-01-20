from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Objective
from .forms import CalculatorForm


class ObjectiveListView(ListView):
    model = Objective


class ObjectiveCalculatorView(View):
    template_name = 'objectives/objective_detail.html'
    form = CalculatorForm

    def get(self, request, pk, **kwargs):
        objective = get_object_or_404(Objective, id=pk)
        context = {'objective': objective, 'form': self.form()}
        return render(request, self.template_name, context)

    def post(self, request, pk, **kwargs):
        objective = get_object_or_404(Objective, id=pk)

        form = self.form(request.POST)
        context = {'objective': objective, 'form': form}

        if form.is_valid():
            value = form.cleaned_data['value']
            result = objective.calculate_percentage(value)
            context['result'] = {'value': value, 'percentage': result}

        return render(request, self.template_name, context)
