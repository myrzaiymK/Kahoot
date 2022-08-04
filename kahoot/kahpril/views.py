from django.shortcuts import  get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.db.models import Q
from rest_framework import viewsets, mixins, generics,filters
from rest_framework import permissions, generics, status
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend


class LeaderTableViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LeaderTableSerializer
    queryset = CustomUser.objects.all()
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['group', 'username',  'first_name', 'last_name', 'number']


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
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['group', 'username', 'number', 'last_name']



class GroupListViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # permission_classes = [permissions.IsAuthenticated]


class QuizViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    # permission_classes = [permissions.IsAuthenticated]


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
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Group.objects.all()




class SaveUsersAnswer(generics.CreateAPIView):
    serializer_class = UsersAnswerSerializer
    queryset = UserAnswer.objects.all()


