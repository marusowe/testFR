from django.db import models
from testFR import settings


class Polls(models.Model):
    title = models.CharField(verbose_name='Название', max_length=500)
    date_start = models.DateField(verbose_name='Начало')
    date_end = models.DateField(verbose_name='Конец')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    class Meta:
        verbose_name = "Опросы"
        verbose_name_plural = "Опрос"

    def __str__(self):
        return self.title


class Questions(models.Model):
    TYPE_QUESTION = (
        (settings.ANSWER_TYPE_TEXT, 'Текст'),
        (settings.ANSWER_TYPE_CHOICE, 'Выбор одного варианта'),
        (settings.ANSWER_TYPE_MULTI_CHOICE, 'Выбор нескольких вариантов'),
    )
    poll = models.ForeignKey(Polls, verbose_name='Опрос', related_name='questions', on_delete=models.CASCADE)
    number = models.IntegerField(verbose_name='Номер вопроса', default=1, unique=True)
    title = models.CharField(verbose_name='Вопрос', max_length=500)
    type = models.CharField(verbose_name='Тип вопроса', max_length=20, choices=TYPE_QUESTION)

    class Meta:
        verbose_name = "Вопросы"
        verbose_name_plural = "Вопрос"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Автоинкремент поля number
        # Если запись создается
        if self._state.adding is True:
            last_number = Questions.objects.filter(poll=self.poll).count()
            if last_number != 0:
                self.number = last_number + 1
        super(Questions, self).save(*args, **kwargs)


class AnswerOptions(models.Model):
    question = models.ForeignKey(
        Questions,
        verbose_name='Вопрос',
        related_name='answer_options',
        on_delete=models.CASCADE
    )
    number = models.IntegerField(verbose_name='Номер вопроса', default=1, unique=True)
    title = models.CharField(verbose_name='Вариант ответа', max_length=500)

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответа"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Автоинкремент поля number
        # Если запись создается
        if self._state.adding is True:
            last_number = AnswerOptions.objects.filter(question=self.question).count()
            if last_number != 0:
                self.number = last_number + 1
        super(AnswerOptions, self).save(*args, **kwargs)


class Answers(models.Model):
    user = models.IntegerField(verbose_name='ID пользователя')
    poll = models.ForeignKey(Polls, verbose_name='Опрос', related_name='answer_poll', on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, verbose_name='Вопрос', related_name='question_poll', on_delete=models.CASCADE)
    answer = models.TextField(verbose_name='Ответ', blank=True, null=True)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.poll.title
