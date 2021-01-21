from django.db import models
from django.urls import reverse

from .utils import linear_interpolation


class Objective(models.Model):
    metric_name = models.CharField('métrica', max_length=30)
    description = models.CharField('descripción', max_length=150)

    class Meta:
        verbose_name = 'objetivo'

    def __str__(self):
        return self.metric_name

    def get_absolute_url(self):
        return reverse('objective-detail', args=[str(self.id)])

    def _get_nearest_goals(self, target_value):
        left_goal = None
        right_goal = None

        goals = self.goal_set.all()

        is_inverse = goals[0].value > goals[1].value
        if is_inverse:
            goals = reversed(goals)

        for goal in goals:
            if goal.value < target_value:
                left_goal = goal
            elif goal.value > target_value:
                right_goal = goal
                break
            else:
                return goal

        # TODO Refactor this
        return (right_goal, left_goal) if is_inverse else (left_goal, right_goal)

    def calculate_percentage(self, value):
        nearest = self._get_nearest_goals(value)

        if isinstance(nearest, Goal):
            return nearest.percentage

        if nearest[0] is None:
            return 0

        if nearest[1] is None:
            return 100

        return linear_interpolation(
            value,
            (nearest[0].value, nearest[0].percentage),
            (nearest[1].value, nearest[1].percentage)
        )


class Goal(models.Model):
    objective = models.ForeignKey(
        Objective, on_delete=models.CASCADE, verbose_name='objetivo')
    description = models.CharField('descripción', max_length=30)
    value = models.FloatField('meta', default=0)
    percentage = models.FloatField('porcentaje', default=0)

    class Meta:
        verbose_name = 'meta'
        ordering = ['percentage']
        constraints = [
            models.UniqueConstraint(
                fields=['objective', 'value'], name='unique_objective_value'
            )
        ]

    def __str__(self):
        return self.description
