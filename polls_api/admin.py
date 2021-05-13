from django.contrib import admin
from polls_api.models import Polls, Questions, AnswerOptions, Answers


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'type', 'poll')


@admin.register(Polls)
class PollsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_start', 'date_end', 'description')


@admin.register(AnswerOptions)
class AnswerOptionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'question', 'number')


@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ('user', 'answer', 'poll', 'question')
