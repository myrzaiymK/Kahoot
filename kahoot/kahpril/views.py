from django.shortcuts import  get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.db.models import Q
from rest_framework import viewsets, mixins, generics,filters
from rest_framework import permissions, generics, status
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend


class MyQuizListAPI(generics.ListAPIView):
    # permission_classes = [
    #     permissions.IsAuthenticated
    # ]
    serializer_class = MyQuizListSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Quiz.objects.filter(quiztaker__user=self.request.user)
        query = self.request.GET.get("q")

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            ).distinct()

        return queryset



class UserViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['group', 'username', 'number', 'last_name']



class GroupViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # permission_classes = [permissions.IsAuthenticated]



# class GroupListViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer


# class QuizListView(viewsets.ReadOnlyModelViewSet):
#     queryset = Quiz.objects.all()
#     serializer_class = QuizListSerializer


class QuizListView(generics.ListAPIView):
    serializer_class = QuizListSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Quiz.objects.filter(roll_out=True)
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__iconstains=query)
            ).distinct()
        return queryset


class QuizDetailAPI(generics.RetrieveAPIView):
    serializer_class = QuizDetailSerializer
    # permission_classes = [
    #     permissions.IsAuthenticated
    # ]
    queryset = Group.objects.all()



    # def get(self, *args, **kwargs):
    #     slug = self.kwargs["slug"]
    #     quiz = get_object_or_404(Quiz, slug=slug)
    #     last_question = None
    #     obj, created = QuizTaker.objects.get_or_create(user=self.request.user, quiz=quiz)
    #     if created:
    #         for question in Question.objects.filter(quiz=quiz):
    #             UserAnswer.objects.create(quiz_taker=obj, question=question)
    #     else:
    #         last_question = UserAnswer.objects.filter(quiz_taker=obj, answer__isnull=False)
    #         if last_question.count() > 0:
    #             last_question = last_question.last().question.id
    #         else:
    #             last_question = None
    #
    #     return Response({'quiz': self.get_serializer(quiz, context={'request': self.request}).data, 'last_question_id': last_question})




class SaveUsersAnswer(generics.CreateAPIView):
    serializer_class = UsersAnswerSerializer
    queryset = UserAnswer.objects.all()



# class SubmitQuizAPI(generics.GenericAPIView):
#     serializer_class = QuizResultSerializer
#     queryset = UserAnswer.objects.all()
#     # permission_classes = [
#     #     permissions.IsAuthenticated
#     # ]
#
#     def post(self, request, *args, **kwargs):
#         quiztaker_id = request.data['quiztaker']
#         question_id = request.data['question']
#         answer_id = request.data['answer']
#
#         quiztaker = get_object_or_404(QuizTaker, id=quiztaker_id)
#         question = get_object_or_404(Question, id=question_id)
#
#         quiz = Quiz.objects.get(slug=self.kwargs['slug'])
#
#         if quiztaker.completed:
#             return Response({
#                 "message": "This quiz is already complete. You can't submit again"},
#                 status=status.HTTP_412_PRECONDITION_FAILED
#             )
#
#         if answer_id is not None:
#             answer = get_object_or_404(Answer, id=answer_id)
#             obj = get_object_or_404(UserAnswer, quiz_taker=quiztaker, question=question)
#             obj.answer = answer
#             obj.save()
#
#         quiztaker.completed = True
#         correct_answers = 0
#
#         for users_answer in UserAnswer.objects.filter(quiz_taker=quiztaker):
#             answer = Answer.objects.get(question=users_answer.question, is_correct=True)
#             print(answer)
#             print(users_answer.answer)
#             if users_answer.answer == answer:
#                 correct_answers += 1
#
#         quiztaker.score = int(correct_answers / quiztaker.quiz.question_set.count() * 100)
#         print(quiztaker.score)
#         quiztaker.save()
#
#         return Response(self.get_serializer(quiz).data)
