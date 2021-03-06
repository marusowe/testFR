from rest_framework import serializers

from polls_api.models import AnswerOptions
from polls_api.models import Answers
from polls_api.models import Polls
from polls_api.models import Questions
from testFR import settings


class AnswerOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOptions
        fields = ['number', 'title']
        extra_kwargs = {
            'number': {'read_only': True},
        }

    def create(self, validated_data):
        question = self.context['question']
        return AnswerOptions.objects.create(**validated_data, question=question)


class QuestionsSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionsSerializer(many=True, required=False)

    class Meta:
        model = Questions
        fields = ['id', 'title', 'number', 'type', 'answer_options']
        extra_kwargs = {
            'number': {'read_only': True},
            'poll': {'read_only': True},
        }

    def create(self, validated_data):
        poll = self.context['poll']
        return Questions.objects.create(**validated_data, poll=poll)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.type = validated_data.get('type', instance.type)
        instance.number = validated_data.get('number', instance.number)
        instance.save()
        return instance

    def validate_number(self, number):
        if Questions.objects.filter(number=number).exists():
            raise serializers.ValidationError(dict(message='Number exists', status='error'))
        return number


class PollsCreateSerializer(serializers.ModelSerializer):
    questions = QuestionsSerializer(many=True, required=False)

    class Meta:
        model = Polls
        fields = '__all__'


class PollsSerializer(serializers.ModelSerializer):
    questions = QuestionsSerializer(many=True, required=False)

    class Meta:
        model = Polls
        fields = ['id', 'title', 'date_end', 'description', 'questions']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.date_end = validated_data.get('date_end', instance.date_end)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class AnswersSerializer(serializers.ModelSerializer):
    poll = serializers.StringRelatedField()
    question = serializers.StringRelatedField()

    class Meta:
        model = Answers
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'poll': {'read_only': True},
            'question': {'read_only': True},
        }

    def save(self, *args, **kwargs):
        type_answer = self.context.get('type', '')
        validated_data = dict(
            list(self.validated_data.items()) + list(kwargs.items())
        )
        if type_answer != settings.ANSWER_TYPE_TEXT:
            try:
                validated_answer = validated_data['answer'].split()
                answer_without_spaces = ''.join(validated_answer)
                if type_answer == settings.ANSWER_TYPE_CHOICE:
                    answer_in_model = AnswerOptions.objects.get(
                        question=validated_data['question'], number=int(answer_without_spaces))
                    answer = answer_in_model.title
                else:
                    answer_in_model = AnswerOptions.objects.filter(
                        question=validated_data['question'], number__in=answer_without_spaces.split(','))
                    answer = ','.join([i.title for i in answer_in_model])
            except ValueError:
                raise serializers.ValidationError(f'Wrong answer for {type_answer}')
            except AnswerOptions.DoesNotExist:
                raise serializers.ValidationError('Answer does not exists')
            else:
                validated_data['answer'] = answer

        self.instance = self.create(validated_data)
        return self.instance
