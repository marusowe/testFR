# Generated by Django 2.2.10 on 2021-05-12 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_api', '0009_questions_number_in_poll'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='number_in_poll',
            field=models.IntegerField(unique=True, verbose_name='Номер вопроса'),
        ),
    ]
