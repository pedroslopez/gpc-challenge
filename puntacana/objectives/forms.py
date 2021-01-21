from django import forms
from crispy_forms.helper import FormHelper

from .models import Objective, Goal


class CalculatorForm(forms.Form):
    value = forms.FloatField(label='Valor logrado')


class GoalFormSetHelper(FormHelper):
    template = 'objectives/objective_goals_formset.html'
    form_tag = False


class BaseGoalFormSet(forms.BaseInlineFormSet):
    def clean(self):
        """Checks that order is strictly ascending or descending"""
        if any(self.errors):
            return

        sorted_validation_error = forms.ValidationError(
            'Los valores de meta deben ser estrictamente ascendientes o estrictamente descendientes.'
        )

        filled_forms = filter(
            lambda f: 'value' in f.cleaned_data and not self._should_delete_form(f),
            self.forms
        )

        sorted_forms = sorted(
            filled_forms,
            key=lambda f: f.cleaned_data.get('percentage', 0)
        )

        goal_ascending = None
        for i in range(1, len(sorted_forms)):
            form = sorted_forms[i]

            previous_value = sorted_forms[i-1].cleaned_data['value']
            current_value = form.cleaned_data['value']

            if current_value > previous_value:
                if goal_ascending is None:
                    goal_ascending = True
                elif not goal_ascending:
                    raise sorted_validation_error
            elif current_value < previous_value:
                if goal_ascending is None:
                    goal_ascending = False
                elif goal_ascending:
                    raise sorted_validation_error
            else:
                raise forms.ValidationError('Los valores de meta deben ser únicos.')


GoalFormSet = forms.inlineformset_factory(
    Objective, Goal, fields=[
        'description',
        'value',
        'percentage'
    ], min_num=2, validate_min=True, extra=2, formset=BaseGoalFormSet)
