from .views import *
from django.urls import include, path, re_path
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupListViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('my-quizzes', MyQuizListAPI.as_view()),
    path('quizzes/', QuizListView.as_view()),
    path('quiz_list/create/', QuizViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('quiz_list/<int:pk>/delete/', QuizViewSet.as_view({'delete': 'destroy'})),
    path("save-answer", SaveUsersAnswer.as_view()),
    path('leader_table', LeaderTableViewSet.as_view({'get': 'list'})),
    re_path(r"quizzes/(?P<group>[\w\-]+)/$", QuizDetailAPI.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
urlpatterns += router.urls

