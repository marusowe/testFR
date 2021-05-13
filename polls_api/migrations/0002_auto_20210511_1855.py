# Generated by Django 2.2.10 on 2021-05-11 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answeroptions',
            options={'verbose_name': 'Вариант ответа', 'verbose_name_plural': 'Варианты ответа'},
        ),
        migrations.AlterModelOptions(
            name='answers',
            options={'verbose_name': 'Ответ', 'verbose_name_plural': 'Ответы'},
        ),
        migrations.AlterModelOptions(
            name='polls',
            options={'verbose_name': 'Опросы', 'verbose_name_plural': 'Опрос'},
        ),
        migrations.AlterModelOptions(
            name='questions',
            options={'verbose_name': 'Вопросы', 'verbose_name_plural': 'Вопрос'},
        ),
        migrations.AlterField(
            model_name='polls',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]