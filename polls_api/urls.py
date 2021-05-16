from django.urls import path

from polls_api.views import AnswerOptionsCreate
from polls_api.views import AnswerOptionsDelete
from polls_api.views import AnswerOptionsUpdate
from polls_api.views import AnswersCreateView
from polls_api.views import AnswersList
from polls_api.views import PollsActiveList
from polls_api.views import PollsCreate
from polls_api.views import PollsDelete
from polls_api.views import PollsDetail
from polls_api.views import PollsList
from polls_api.views import PollsUpdate
from polls_api.views import QuestionCreate
from polls_api.views import QuestionDelete
from polls_api.views import QuestionDetail
from polls_api.views import QuestionUpdate

urlpatterns = [
    # Администратор
    path('polls/create/', PollsCreate.as_view(), name='create_polls'),
    path('polls/<int:poll_pk>/update/', PollsUpdate.as_view(), name='update_polls'),
    path('polls/<int:poll_pk>/delete/', PollsDelete.as_view(), name='delete_polls'),
    path('polls/<int:poll_pk>/questions/create/', QuestionCreate.as_view(), name='create_question'),
    path('polls/<int:poll_pk>/questions/<int:question_number>/update/',
         QuestionUpdate.as_view(),
         name='update_question'
         ),
    path('polls/<int:poll_pk>/questions/<int:question_number>/delete/',
         QuestionDelete.as_view(),
         name='delete_question'),
    path('polls/<int:poll_pk>/questions/<int:question_number>/answer/create/',
         AnswerOptionsCreate.as_view(),
         name='create_answer'),
    path('polls/<int:poll_pk>/questions/<int:question_number>/answer/<int:answer_number>/update/',
         AnswerOptionsUpdate.as_view(),
         name='update_answer'),
    path('polls/<int:poll_pk>/questions/<int:question_number>/answer/<int:answer_number>/delete/',
         AnswerOptionsDelete.as_view(),
         name='delete_answer'),

    # Юзер
    path('polls/all/', PollsList.as_view(), name='all_polls'),
    path('polls/active/', PollsActiveList.as_view(), name='active_polls'),
    path('polls/<int:poll_pk>/', PollsDetail.as_view(), name='get_polls'),
    path('polls/<int:poll_pk>/questions/<int:question_number>/', QuestionDetail.as_view(), name='get_polls'),
    path('polls/passed/user/<int:user_id>/', AnswersList.as_view(), name='passed_polls'),
    path('polls/<int:poll_pk>/questions/<int:question_number>/reply/<str:reply_type>/',
         AnswersCreateView.as_view(),
         name='reply_polls'),
]
