from .views import *
from django.urls import include, path, re_path
from rest_framework import routers
# from rest_framework



router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)



urlpatterns = [
    path('api/', include(router.urls)),
    path('my-quizzes', MyQuizListAPI.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('quizzes/', QuizListView.as_view()),
    path("save-answer", SaveUsersAnswer.as_view()),
    re_path(r"quizzes/(?P<group>[\w\-]+)/$", QuizDetailAPI.as_view()),
    # re_path(r"quizzes/(?P<slug>[\w\-]+)/submit/$", SubmitQuizAPI.as_view()),

    # re_path('quizzes/(?P<slug>[\w\-]/$', QuizDetailView.as_view()),


]
urlpatterns += router.urls


