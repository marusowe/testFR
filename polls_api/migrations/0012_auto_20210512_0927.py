# Generated by Django 2.2.10 on 2021-05-12 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_api', '0011_auto_20210512_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='number',
            field=models.IntegerField(verbose_name='Номер вопроса'),
        ),
    ]
