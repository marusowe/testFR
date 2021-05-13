from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from polls_api.models import Polls
from polls_api.models import Questions
from polls_api.models import Answers
from polls_api.models import AnswerOptions
from polls_api.serializers import PollsSerializer
from polls_api.serializers import QuestionsSerializer
from polls_api.serializers import QuestionsUpdateSerializer
from polls_api.serializers import AnswerOptionsSerializer
from polls_api.serializers import AnswersSerializer
from django.http import Http404
from rest_framework.permissions import IsAuthenticated


def get_poll(pk):
    try:
        return Polls.objects.get(pk=pk)
    except Polls.DoesNotExist:
        raise Http404


def get_question(poll, number):
    try:
        return Questions.objects.get(poll=poll, number=number)
    except Questions.DoesNotExist:
        raise Http404


def get_answer_number(question, number):
    try:
        return AnswerOptions.objects.get(question=question, number=number)
    except AnswerOptions.DoesNotExist:
        raise Http404


def get_answers(user_id):
    try:
        return Answers.objects.filter(user=user_id).select_related()
    except Answers.DoesNotExist:
        raise Http404


def generate_id():
    try:
        max_id_answer = Answers.objects.latest('user')
    except Answers.DoesNotExist:
        return 1
    return max_id_answer.user + 1


class PollsView(APIView):
    def get(self, request, pk=None):
        if pk:
            polls = get_poll(pk=pk)
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
        poll = get_poll(pk=poll_pk)
        serializer = PollsSerializer(poll, data=request.data)
        if serializer.is_valid():
            serializer.update(poll, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class PollsDeleteAdminView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, poll_pk):
        poll = get_poll(pk=poll_pk)
        poll.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionCreateAdminView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, poll_pk):
        poll = get_poll(pk=poll_pk)
        serializer = QuestionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(poll=poll)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class QuestionUpdateAdminView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, poll_pk, question_number):
        poll = get_poll(pk=poll_pk)
        question = get_question(poll=poll, number=question_number)
        serializer = QuestionsUpdateSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class QuestionDeleteAdminView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, poll_pk, question_number):
        poll = get_poll(pk=poll_pk)
        question = get_question(poll=poll, number=question_number)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerCreateOptionsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, poll_pk, question_number):
        poll = get_poll(pk=poll_pk)
        question = get_question(poll=poll, number=question_number)
        serializer = AnswerOptionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(question=question)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class AnswerUpdateOptionsView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, poll_pk, question_number, answer_number):
        poll = get_poll(pk=poll_pk)
        question = get_question(poll=poll, number=question_number)
        answer = get_answer_number(question=question, number=answer_number)
        serializer = AnswerOptionsSerializer(answer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class AnswerDeleteOptionsView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, poll_pk, question_number, answer_number):
        poll = get_poll(pk=poll_pk)
        question = get_question(poll=poll, number=question_number)
        answer = get_answer_number(question=question, number=answer_number)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswersView(APIView):

    def get(self, request, user_id):
        answers = get_answers(user_id)
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

    def post(self, request, poll_pk, question_number, reply_type):
        poll = get_poll(pk=poll_pk)
        question = get_question(poll=poll, number=question_number)
        if 'user_id' in request.COOKIES:
            if Answers.objects.filter(user=request.COOKIES['user_id']).exists():
                user_id = request.COOKIES['user_id']
            else:
                user_id = generate_id()
        else:
            user_id = generate_id()
        if question.type != reply_type:
            return Response('Wrong reply type', status=status.HTTP_400_BAD_REQUEST)
        if Answers.objects.filter(poll=poll, question=question, user=user_id).exists():
            return Response('Answer exists', status=status.HTTP_400_BAD_REQUEST)
        serializer = AnswersSerializer(data=request.data, context={'type': question.type})
        if serializer.is_valid():
            serializer.save(poll=poll, question=question, user=user_id)
            response = Response(serializer.data, status=status.HTTP_200_OK)
            response.set_cookie('user_id', user_id)
            return response
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
