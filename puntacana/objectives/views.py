from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from django.forms import inlineformset_factory

from .models import Objective, Goal
from .forms import CalculatorForm, GoalFormSet, GoalFormSetHelper


class ObjectiveListView(ListView):
    model = Objective


class ObjectiveCreateView(CreateView):
    model = Objective
    fields = ['metric_name', 'description']

    def get_context_data(self, **kwargs):
        context = super(ObjectiveCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['goals_formset'] = GoalFormSet(self.request.POST)
        else:
            context['goals_formset'] = GoalFormSet()

        context['goals_formset_helper'] = GoalFormSetHelper()

        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['goals_formset']

        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)


class ObjectiveUpdateView(UpdateView):
    model = Objective
    fields = ['metric_name', 'description']

    def get_context_data(self, **kwargs):
        context = super(ObjectiveUpdateView, self).get_context_data(**kwargs)
        objective = self.get_object()

        if self.request.POST:
            context['goals_formset'] = GoalFormSet(
                self.request.POST,
                instance=objective
            )
        else:
            context['goals_formset'] = GoalFormSet(instance=objective)

        context['goals_formset_helper'] = GoalFormSetHelper()

        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['goals_formset']

        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)


class ObjectiveDeleteView(DeleteView):
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
