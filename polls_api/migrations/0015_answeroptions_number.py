# Generated by Django 2.2.10 on 2021-05-13 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_api', '0014_auto_20210512_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='answeroptions',
            name='number',
            field=models.IntegerField(default=1, verbose_name='Номер вопроса'),
        ),
    ]
