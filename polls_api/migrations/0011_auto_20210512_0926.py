# Generated by Django 2.2.10 on 2021-05-12 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls_api', '0010_auto_20210512_0922'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questions',
            old_name='number_in_poll',
            new_name='number',
        ),
    ]