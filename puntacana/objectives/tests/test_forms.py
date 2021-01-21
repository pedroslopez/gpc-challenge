from django.test import TestCase
from django.forms import inlineformset_factory

from objectives.models import Objective, Goal
from objectives.forms import GoalFormSet


class GoalFormSetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.objective = Objective.objects.create(
            metric_name='Test objective',
            description='This is a test objective'
        )

    def test_non_increasing_values_in_increasing_set_are_not_valid(self):
        """Values that are not strictly increasing on an increasing set are invalid"""
        data = {
            'goal_set-TOTAL_FORMS': '3',
            'goal_set-INITIAL_FORMS': '0',
            'goal_set-0-description': 'Uno',
            'goal_set-0-value': '5',
            'goal_set-0-percentage': '80',
            'goal_set-1-description': 'Dos',
            'goal_set-1-value': '6',
            'goal_set-1-percentage': '90',
            'goal_set-2-description': 'Tres',
            'goal_set-2-value': '4',
            'goal_set-2-percentage': '100',
        }

        formset = GoalFormSet(data, instance=self.objective)

        self.assertFalse(formset.is_valid())
    
    def test_non_decreasing_values_in_decreasing_set_are_not_valid(self):
        """Values that are not strictly decreasing on a decreasing set are invalid"""
        data = {
            'goal_set-TOTAL_FORMS': '3',
            'goal_set-INITIAL_FORMS': '0',
            'goal_set-0-description': 'Uno',
            'goal_set-0-value': '5',
            'goal_set-0-percentage': '80',
            'goal_set-1-description': 'Dos',
            'goal_set-1-value': '4',
            'goal_set-1-percentage': '90',
            'goal_set-2-description': 'Tres',
            'goal_set-2-value': '6',
            'goal_set-2-percentage': '100',
        }

        formset = GoalFormSet(data, instance=self.objective)

        self.assertFalse(formset.is_valid())

    def test_increasing_values_are_valid(self):
        """Values that are strictly increasing should be valid"""
        data = {
            'goal_set-TOTAL_FORMS': '3',
            'goal_set-INITIAL_FORMS': '0',
            'goal_set-0-description': 'Minimo',
            'goal_set-0-value': '5',
            'goal_set-0-percentage': '80',
            'goal_set-1-description': 'Medio',
            'goal_set-1-value': '6',
            'goal_set-1-percentage': '90',
            'goal_set-2-description': 'Maximo',
            'goal_set-2-value': '7',
            'goal_set-2-percentage': '100',
        }

        formset = GoalFormSet(data, instance=self.objective)

        self.assertTrue(formset.is_valid())

    def test_decreasing_values_are_valid(self):
        """Values that are strictly decreasing should be valid"""
        data = {
            'goal_set-TOTAL_FORMS': '3',
            'goal_set-INITIAL_FORMS': '0',
            'goal_set-0-description': 'Maximo',
            'goal_set-0-value': '7',
            'goal_set-0-percentage': '80',
            'goal_set-1-description': 'Medio',
            'goal_set-1-value': '6',
            'goal_set-1-percentage': '90',
            'goal_set-2-description': 'Minimo',
            'goal_set-2-value': '5',
            'goal_set-2-percentage': '100',
        }

        formset = GoalFormSet(data, instance=self.objective)

        self.assertTrue(formset.is_valid())

    def test_unsorted_percentage_causes_no_effect(self):
        """Percentages should be auto-sorted in order to determine whether values are decreasing"""
        data = {
            'goal_set-TOTAL_FORMS': '3',
            'goal_set-INITIAL_FORMS': '0',
            'goal_set-0-description': 'Maximo',
            'goal_set-0-value': '7',
            'goal_set-0-percentage': '80',
            'goal_set-1-description': 'Minimo',
            'goal_set-1-value': '5',
            'goal_set-1-percentage': '100',
            'goal_set-2-description': 'Medio',
            'goal_set-2-value': '6',
            'goal_set-2-percentage': '90',
        }

        formset = GoalFormSet(data, instance=self.objective)

        self.assertTrue(formset.is_valid())

    def test_unsorted_percentage_causes_no_effect_2(self):
        """Percentages should be auto-sorted in order to determine whether values are increasing"""
        data = {
            'goal_set-TOTAL_FORMS': '3',
            'goal_set-INITIAL_FORMS': '0',
            'goal_set-0-description': 'Minimo',
            'goal_set-0-value': '5',
            'goal_set-0-percentage': '80',
            'goal_set-1-description': 'Maximo',
            'goal_set-1-value': '7',
            'goal_set-1-percentage': '100',
            'goal_set-2-description': 'Medio',
            'goal_set-2-value': '6',
            'goal_set-2-percentage': '90',
        }

        formset = GoalFormSet(data, instance=self.objective)

        self.assertTrue(formset.is_valid())
