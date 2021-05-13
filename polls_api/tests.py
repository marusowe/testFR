from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from polls_api.models import Polls
from polls_api.models import Questions


class PollsAPITestCase(APITestCase):

    def setUp(self):
        self.test_poll = {
            'title': 'test',
            'date_start': '2021-05-15',
            'date_end': '2021-05-21',
            'description': 'test_description',
        }
        self.test_question = {
            'title': 'test',
            'type': 'text'
        }
        User.objects.create(
            username='kk',
            email='k@k.ru',
            password='123',
            is_active=True
        )
        poll = Polls.objects.create(**self.test_poll)
        self.poll_pk = poll.pk
        user = User.objects.get(username='kk')
        self.client.force_authenticate(user=user)

    def test_create_poll(self):
        url = reverse('create_polls')
        response = self.client.post(url, format='json', data=self.test_poll)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.test_poll)

    def test_update_poll(self):
        url = reverse('update_polls', kwargs={'poll_pk': self.poll_pk})
        updated_poll = self.test_poll.copy()
        updated_poll['title'] = 'test update'
        response = self.client.put(url, format='json', data=updated_poll)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], updated_poll['title'])

    def test_delete_poll(self):
        url = reverse('delete_polls', kwargs={'poll_pk': self.poll_pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_question(self):
        poll = Polls.objects.create(**self.test_poll)
        url = reverse('create_question', kwargs={'poll_pk': poll.pk})
        response = self.client.post(url, format='json', data=self.test_question)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.test_question['title'])

    def test_update_question(self):
        poll = Polls.objects.create(**self.test_poll)
        question = Questions.objects.create(poll=poll, **self.test_question)
        url = reverse('update_question', kwargs={'poll_pk': poll.pk, 'question_number': question.number})
        updated_question = self.test_question.copy()
        updated_question['title'] = 'test updated'
        response = self.client.put(url, format='json', data=updated_question)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], updated_question['title'])

    def test_delete_question(self):
        poll = Polls.objects.create(**self.test_poll)
        question = Questions.objects.create(poll=poll, **self.test_question)
        url = reverse('delete_question', kwargs={'poll_pk': poll.pk, 'question_number': question.number})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)