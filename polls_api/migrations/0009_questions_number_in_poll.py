# Generated by Django 2.2.10 on 2021-05-12 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_api', '0008_auto_20210512_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='number_in_poll',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
