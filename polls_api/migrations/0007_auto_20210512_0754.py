# Generated by Django 2.2.10 on 2021-05-12 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_api', '0006_auto_20210512_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='polls',
            name='date_start',
            field=models.DateField(verbose_name='Начало'),
        ),
    ]