# Generated by Django 3.1.5 on 2021-01-20 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objectives', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goal',
            options={'ordering': ['percentage'], 'verbose_name': 'meta'},
        ),
        migrations.AddConstraint(
            model_name='goal',
            constraint=models.UniqueConstraint(fields=('objective', 'value'), name='unique_objective_value'),
        ),
    ]