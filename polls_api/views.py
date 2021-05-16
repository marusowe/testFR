import datetime

from django.shortcuts import get_list_or_404
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from polls_api.models import AnswerOptions
from polls_api.models import Answers
from polls_api.models import Polls
from polls_api.models import Questions
from polls_api.serializers import AnswerOptionsSerializer
from polls_api.serializers import AnswersSerializer
from polls_api.serializers import PollsCreateSerializer
from polls_api.serializers import PollsSerializer
from polls_api.serializers import QuestionsSerializer


class PollsList(generics.ListAPIView):
    queryset = Polls.objects.all()
    serializer_class = PollsSerializer


class PollsActiveList(generics.ListAPIView):
    queryset = Polls.objects.all()
    serializer_class = PollsSerializer

    def get_queryset(self):
        active_polls = Polls.objects.filter(
            date_start__gte=datetime.datetime.now().date())
        return active_polls


class PollsDetail(generics.RetrieveAPIView):
    queryset = Polls.objects.all()
    serializer_class = PollsSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'poll_pk'


class PollsCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PollsCreateSerializer


class PollsUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Polls.objects.all()
    serializer_class = PollsSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'poll_pk'


class PollsDelete(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Polls.objects.all()
    serializer_class = PollsSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'poll_pk'


class QuestionDetail(generics.RetrieveAPIView):
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer

    def get_object(self):
        poll = get_object_or_404(Polls, pk=self.kwargs['poll_pk'])
        queryset = self.filter_queryset(self.get_queryset())
        question = get_object_or_404(queryset, poll=poll,
                                     number=self.kwargs['question_number'])
        return question


class QuestionCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionsSerializer

    def get_serializer_context(self):
        poll = get_object_or_404(Polls, pk=self.kwargs['poll_pk'])
        return {
            'poll': poll
        }


class QuestionUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionsSerializer
    queryset = Questions.objects.all()

    def get_object(self):
        poll = get_object_or_404(Polls, pk=self.kwargs['poll_pk'])
        queryset = self.filter_queryset(self.get_queryset())
        question = get_object_or_404(queryset, poll=poll,
                                     number=self.kwargs['question_number'])
        return question


class QuestionDelete(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionsSerializer
    queryset = Questions.objects.all()

    def get_object(self):
        poll = get_object_or_404(Polls, pk=self.kwargs['poll_pk'])
        queryset = self.filter_queryset(self.get_queryset())
        question = get_object_or_404(queryset, poll=poll,
                                     number=self.kwargs['question_number'])
        return question


class AnswerOptionsCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnswerOptionsSerializer

    def get_serializer_context(self):
        poll = get_object_or_404(Polls, pk=self.kwargs['poll_pk'])
        question = get_object_or_404(Questions, poll=poll,
                                     pk=self.kwargs['question_number'])
        return {
            'question': question
        }


class AnswerOptionsUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnswerOptionsSerializer
    queryset = AnswerOptions.objects.all()

    def get_object(self):
        poll = get_object_or_404(Polls, pk=self.kwargs['poll_pk'])
        question = get_object_or_404(Questions, poll=poll,
                                     pk=self.kwargs['question_number'])
        queryset = self.filter_queryset(self.get_queryset())
        answer_option = get_object_or_404(queryset, question=question,
                                          number=self.kwargs['answer_number'])
        return answer_option


class AnswerOptionsDelete(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnswerOptionsSerializer
    queryset = AnswerOptions.objects.all()

    def get_object(self):
        poll = get_object_or_404(Polls, pk=self.kwargs['poll_pk'])
        question = get_object_or_404(Questions, poll=poll,
                                     pk=self.kwargs['question_number'])
        queryset = self.filter_queryset(self.get_queryset())
        answer_option = get_object_or_404(queryset, question=question,
                                          number=self.kwargs['answer_number'])
        return answer_option


class AnswersList(generics.ListAPIView):
    serializer_class = AnswersSerializer
    lookup_field = 'user_id'

    def get_queryset(self):
        user = self.kwargs['user_id']
        answers = get_list_or_404(Answers, user=user)
        return answers


class AnswersCreateView(APIView):

    @staticmethod
    def generate_id():
        users_id = Answers.objects.values_list('user', flat=True)
        return max(users_id) + 1 if users_id else 1

    def post(self, request, poll_pk, question_number, reply_type):
        poll = get_object_or_404(Polls, pk=poll_pk)
        question = get_object_or_404(Questions, poll=poll, number=question_number)

        if 'user_id' not in request.session:
            request.session.save()
            request.session['user_id'] = self.generate_id()

        if question.type != reply_type:
            return Response('Wrong reply type', status=status.HTTP_400_BAD_REQUEST)
        if Answers.objects.filter(poll=poll, question=question, user=request.session['user_id']).exists():
            return Response('Answer exists', status=status.HTTP_400_BAD_REQUEST)

        serializer = AnswersSerializer(data=request.data, context={'type': question.type})
        if serializer.is_valid():
            serializer.save(poll=poll, question=question, user=request.session['user_id'])
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
