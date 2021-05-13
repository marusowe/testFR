# Generated by Django 2.2.10 on 2021-05-12 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls_api', '0003_auto_20210511_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answeroptions',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_options', to='polls_api.Questions', verbose_name='Вопрос'),
        ),
        migrations.RemoveField(
            model_name='questions',
            name='poll',
        ),
        migrations.AddField(
            model_name='questions',
            name='poll',
            field=models.ManyToManyField(to='polls_api.Polls', verbose_name='Опрос'),
        ),
    ]
