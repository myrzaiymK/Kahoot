from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline
from .models import Quiz, Question, Answer, QuizTaker, UserAnswer, CustomUser


class AnswerInline(NestedStackedInline):
	model = Answer
	extra = 4
	max_num = 4


class QuestionInline(NestedStackedInline):
	model = Question
	inlines = [AnswerInline, ]
	extra = 5

#
# class Quiz1(admin.ModelAdmin):
# 	model = Quiz
# 	fields = ('name', 'description', 'image', 'slug', 'roll_out', 'player_passed', 'group', 'timestamp', 'questions_count')
# 	# list_display = ('username', 'group', 'email', 'all_score', 'group_rating', 'rating', 'tests', 'is_active')


class QuizAdmin(NestedModelAdmin):
	inlines = [QuestionInline, ]
	list_display = ('name', 'questions_count', 'player_passed')


class UsersAnswerInline(admin.TabularInline):
	model = UserAnswer


class QuizTakerAdmin(admin.ModelAdmin):
	inlines = [UsersAnswerInline, ]
	list_display = ('user', 'score', 'quiz')


class UserAdmin(admin.ModelAdmin):
	model = CustomUser
	fields = ('username', 'first_name', 'last_name', 'group', 'email', 'number', 'password', 'all_score', 'group_rating', 'rating', 'tests', 'is_active')
	list_display = ('username', 'group', 'email', 'all_score', 'group_rating', 'rating', 'tests', 'is_active')


admin.site.register(Quiz, QuizAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuizTaker, QuizTakerAdmin)
admin.site.register(UserAnswer)


