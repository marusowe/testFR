from django.urls import path
from polls_api.views import PollsView
from polls_api.views import PollsCreateAdminView
from polls_api.views import PollsUpdateAdminView
from polls_api.views import PollsDeleteAdminView
from polls_api.views import QuestionCreateAdminView
from polls_api.views import QuestionUpdateAdminView
from polls_api.views import QuestionDeleteAdminView
from polls_api.views import AnswerCreateOptionsView
from polls_api.views import AnswerUpdateOptionsView
from polls_api.views import AnswerDeleteOptionsView
from polls_api.views import AnswersView
from polls_api.views import AnswersCreateView

urlpatterns = [
    # Администратор
    path('polls/create/', PollsCreateAdminView.as_view(), name='create_polls'),
    path('polls/<int:poll_pk>/update/', PollsUpdateAdminView.as_view(), name='update_polls'),
    path('polls/<int:poll_pk>/delete/', PollsDeleteAdminView.as_view(), name='delete_polls'),
    path('polls/<int:poll_pk>/questions/create/', QuestionCreateAdminView.as_view(), name='create_question'),
    path('polls/<int:poll_pk>/questions/<int:question_number>/update/',
         QuestionUpdateAdminView.as_view(),
         name='update_question'
         ),
    path('polls/<int:poll_pk>/questions/<int:question_number>/delete/',
         QuestionDeleteAdminView.as_view(),
         name='delete_question'),
    path('polls/<int:poll_pk>/questions/<int:question_number>/answer/create/',
         AnswerCreateOptionsView.as_view(),
         name='create_answer'),
    path('polls/<int:poll_pk>/questions/<int:question_number>/answer/<int:answer_number>/update/',
         AnswerUpdateOptionsView.as_view(),
         name='update_answer'),
    path('polls/<int:poll_pk>/questions/<int:question_number>/answer/<int:answer_number>/delete/',
         AnswerDeleteOptionsView.as_view(),
         name='delete_answer'),

    # Юзер
    path('polls/all/', PollsView.as_view(), name='all_polls'),
    path('polls/<int:pk>/', PollsView.as_view(), name='get_polls'),
    path('polls/passed/user/<int:user_id>/', AnswersView.as_view(), name='passed_polls'),
    path('polls/<int:poll_pk>/questions/<int:question_number>/reply/<str:reply_type>/',
         AnswersCreateView.as_view(),
         name='reply_polls'),
]
