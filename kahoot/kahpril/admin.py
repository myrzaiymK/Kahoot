from django.contrib import admin
from nested_inline.admin import  NestedModelAdmin, NestedStackedInline
from .models import Quiz, Question, Answer, QuizTaker, UserAnswer, CustomUser


class AnswerInline(NestedStackedInline):
	model = Answer
	# extra = 4
	# max_num = 4


class QuestionInline(NestedStackedInline):
	model = Question
	inlines = [AnswerInline, ]
	# extra = 5



class QuizAdmin(NestedModelAdmin):
	inlines = [QuestionInline, ]


class UsersAnswerInline(admin.TabularInline):
	model = UserAnswer


class QuizTakerAdmin(admin.ModelAdmin):
	inlines = [UsersAnswerInline, ]


class UserAdmin(admin.ModelAdmin):
	model = CustomUser
	fields = ('username', 'first_name', 'last_name', 'group', 'email', 'number', 'password', 'all_score', 'rating', 'tests',)
	list_display = ('username', 'first_name', 'last_name', 'group', 'email', 'number', 'password', 'all_score', 'rating', 'tests',)


admin.site.register(Quiz, QuizAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuizTaker, QuizTakerAdmin)
admin.site.register(UserAnswer)




#
#
# from django.contrib import admin
# from nested_inline.admin import NestedStackedInline, NestedModelAdmin
# from .models import *
# import nested_admin
#
#
# # class CustomUserAdmin(admin.ModelAdmin):
# #     model = CustomUser
# #     fields = ('first_name', 'last_name', 'group', 'number', 'gmail', 'password', 'all_score', 'rating', 'passed_tests', )
# #     readonly_fields = ('name', 'last_name', 'number', 'gmail','all_score', 'rating', 'passed_tests',)
#
#
# class AnswerAdmin(admin.StackedInline):
#     model = Answer
#
#
# class QuestionAdmin(admin.ModelAdmin):
#     inlines = [AnswerAdmin, ]
#
#
# class UserAnswerInline(nested_admin.NestedTabularInline):
#     model = UserAnswer
#
#
# admin.site.register(Quiz)
# admin.site.register(CustomUser)
# # admin.site.register(QuestionInline)
# admin.site.register(Answer)
# admin.site.register(UserAnswer)
# admin.site.register(Question, QuestionAdmin)
# admin.site.register(QuizTaker)
#

