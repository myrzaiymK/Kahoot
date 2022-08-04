from .models import Quiz, QuizTaker, CustomUser, Group, Answer, Question, UserAnswer
from rest_framework import serializers
from djoser.serializers import UserSerializer



class LeaderTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'group', 'number', 'email', 'all_score',
                  'rating', 'tests',
                  'is_active']


class MyQuizListSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    questions_count = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    """h"""
    class Meta:
        model = Quiz
        fields = ["id", "name", "description", "image", "slug", "questions_count", "completed", "score", "progress"]
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


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'name', 'description', 'image', 'player_passed', 'group', 'questions_count']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'label']



class QuizListSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'questions_count']
        read_only_fields = ['questions_count']

    def get_questions_count(self, obj):
        return obj.question_set.all().count()


class UserListSerializer(UserSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'group', 'number', 'email', 'password', 'all_score', 'rating', 'tests',
                  'is_active', 'date_joined']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class QuestionSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'


class UsersAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'



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



