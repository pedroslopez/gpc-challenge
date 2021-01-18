from django.db import models


class Objective(models.Model):
    metric_name = models.CharField('métrica', max_length=30)
    description = models.CharField('descripción', max_length=150)

    class Meta:
        verbose_name = 'objetivo'

    def __str__(self):
        return self.metric_name


class Goal(models.Model):
    objective = models.ForeignKey(
        Objective, on_delete=models.CASCADE, verbose_name='objetivo')
    description = models.CharField('descripción', max_length=30)
    value = models.FloatField('meta', default=0)
    percentage = models.FloatField('porcentaje', default=0)

    class Meta:
        verbose_name = 'meta'

    def __str__(self):
        return self.description
