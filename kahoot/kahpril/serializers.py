from .models import Quiz, QuizTaker, CustomUser, Group, Answer, Question, UserAnswer
from django.conf import settings
from rest_framework import serializers
from django.shortcuts import get_object_or_404


class MyQuizListSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    questions_count = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    """h"""
    class Meta:
        model = Quiz
        fields = ["quiz_id", "name", "description", "image", "slug", "questions_count", "completed", "score", "progress"]
        # read_only_fields = ["questions_count", "completed", "progress"]
    """test"""
    def get_completed(self, obj):
        quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
        return quiztaker.completed
    """test"""
    def get_progress(self, obj):
        quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
        if quiztaker.completed == False:
            questions_answered = UserAnswer.objects.filter(quiz_taker=quiztaker, answer__isnull=False).count()
            total_questions = obj.question_set.all().count()
            return int(questions_answered / total_questions)

    def get_questions_count(self, obj):
        return obj.question_set.all().count()

    def get_score(self, obj):
        quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
        if quiztaker.completed == True:
            return quiztaker.score


class QuizListSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()

    # id_count = serializers.SerializerMethodField()
    class Meta:
        model = Quiz
        fields = ['id', 'name', 'questions_count']
        read_only_fields = ['questions_count']
        # user_count = serializers.IntegerField(
        #     source='user_set.count',
        #     read_only=True
        # )

    def get_questions_count(self, obj):
        return obj.question_set.all().count()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'group', 'number', 'email', 'password',  'number', 'all_score', 'rating', 'tests',
                  'is_active', 'date_joined']

        def create(self, validated_data):
            user = CustomUser(
                email=validated_data['email'],
                username=validated_data['username']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'label']


class QuestionSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'


class UsersAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'

    def create(self, validated_data):
        print(Question.objects.get(validated_data['timer']))
        return UserAnswer.objects.create(**validated_data)


# class QuizListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Quiz
#         fields = ['id', 'name', 'description', 'image']


class QuizTakerSerializer(serializers.ModelSerializer):
    users_answer_set = UsersAnswerSerializer(many=True)

    class Meta:
        model = QuizTaker
        fields = '__all__'


class QuizDetailSerializer(serializers.ModelSerializer):
    quiztaker_set = serializers.SerializerMethodField()
    question_set = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = '__all__'

    def get_quiztaker_set(self, obj):
        try:
            quiztaker = QuizTaker.objects.get(user=['user'], quiz=obj)
            serializer = QuizTakerSerializer(quiztaker)
            return serializer.data()
        except QuizTaker.DoesNotExist:
            return None

# class QuizResultSerializer(serializers.ModelSerializer):
#     quiztaker_set = serializers.SerializerMethodField()
#     question_set = QuestionSerializer(many=True)
#
#     class Meta:
#         model = Quiz
#         fields = "__all__"
#
#     def get_quiztaker_set(self, obj):
#         try:
#             quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
#             serializer = QuizTakerSerializer(quiztaker)
#             return serializer.data
#
#         except QuizTaker.DoesNotExist:
#             return None
