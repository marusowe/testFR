from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from polls_api.models import Answers
from polls_api.models import Polls
from polls_api.models import Questions
from polls_api.models import AnswerOptions
from polls_api.serializers import AnswerOptionsSerializer
from polls_api.serializers import AnswersSerializer
from polls_api.serializers import PollsSerializer
from polls_api.serializers import QuestionsSerializer
from polls_api.serializers import QuestionsUpdateSerializer

from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404


class PollsView(APIView):
    def get(self, request, pk=None):
        if pk:
            polls = get_object_or_404(Polls, pk=pk)
            data = PollsSerializer(polls).data
        else:
            polls = Polls.objects.all().select_related()
            data = PollsSerializer(polls, many=True).data

        return Response(data, status.HTTP_200_OK)


class PollsCreateAdminView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PollsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class PollsUpdateAdminView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, poll_pk):
        poll = get_object_or_404(Polls, pk=poll_pk)
        serializer = PollsSerializer(poll, data=request.data)
        if serializer.is_valid():
            serializer.update(poll, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class PollsDeleteAdminView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, poll_pk):
        poll = get_object_or_404(Polls, pk=poll_pk)
        poll.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionCreateAdminView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, poll_pk):
        poll = get_object_or_404(Polls, pk=poll_pk)
        serializer = QuestionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(poll=poll)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class QuestionUpdateAdminView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, poll_pk, question_number):
        poll = get_object_or_404(Polls, pk=poll_pk)
        question = get_object_or_404(Questions, poll=poll, number=question_number)
        serializer = QuestionsUpdateSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class QuestionDeleteAdminView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, poll_pk, question_number):
        poll = get_object_or_404(Polls, pk=poll_pk)
        question = get_object_or_404(Questions, poll=poll, number=question_number)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerCreateOptionsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, poll_pk, question_number):
        poll = get_object_or_404(Polls, pk=poll_pk)
        question = get_object_or_404(Questions, poll=poll, number=question_number)
        serializer = AnswerOptionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(question=question)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class AnswerUpdateOptionsView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, poll_pk, question_number, answer_number):
        poll = get_object_or_404(Polls, pk=poll_pk)
        question = get_object_or_404(Questions, poll=poll, number=question_number)
        answer = get_object_or_404(AnswerOptions, question=question, number=answer_number)
        serializer = AnswerOptionsSerializer(answer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class AnswerDeleteOptionsView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, poll_pk, question_number, answer_number):
        poll = get_object_or_404(Polls, pk=poll_pk)
        question = get_object_or_404(Questions, poll=poll, number=question_number)
        answer = get_object_or_404(AnswerOptions, question=question, number=answer_number)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswersView(APIView):

    def get(self, request, user_id):
        answers = get_list_or_404(Answers, user=user_id)
        data = [{
            'poll': i.poll.title,
            'description': i.poll.description,
            'date_start': i.poll.date_start,
            'date_end': i.poll.date_end,
            'question': i.question.title,
            'answer': i.answer
        } for i in answers]
        return Response(data, status.HTTP_200_OK)


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
