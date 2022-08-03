from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


class CustomUser(AbstractUser):
    number = PhoneNumberField(null=True, )
    all_score = models.FloatField(blank=True, null=True, default=0)
    rating = models.PositiveIntegerField(null=True)
    tests = models.PositiveIntegerField(default=0)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, )

    def save(self, *args, **kwargs):
        question = QuizTaker.objects.all().filter()
        score = sum([i.score for i in question])
        self.all_score = score
        super().save()
        #
        # question = QuizTaker.objects.all().filter()
        # # score = sum([i.score for i in question])
        # self.all_score = question.score
        # # self.score.save()
        # super().save()



    # def save(self, *args, **kwargs):
        rating = self.all_score / 10
        self.rating = rating
        super().save()

    class Meta:
        ordering = ['-rating']


class Quiz(models.Model):
    # quiz_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='new/%Y/%m/%d')
    slug = models.SlugField(blank=True)
    roll_out = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp', ]
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    label = models.CharField(max_length=1000)
    order = models.IntegerField(default=4)
    timer = models.PositiveIntegerField(default=20)

    def __str__(self):
        return self.label

    def get_correct_answer(self):
        return self.answer_set.get(is_correct=True)



class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_set')
    label = models.CharField(max_length=1000)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.label



class QuizTaker(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CharField)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    date_finished = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     user_score = UserAnswer.objects.all().filter(quiz_taker=self)
    #     for i in user_score:
    #         score = sum([i.score])
    #         self.score = score
    #         # self.score.save()
    #     super().save()

    def save(self, *args, **kwargs):
        question = UserAnswer.objects.all().filter(quiz_taker=self)
        UserAnswer.score = sum([i.score for i in question])
        self.score = UserAnswer.score
        # self.score.save()
        super().save(*args, **kwargs)


    # def save(self, *args, **kwargs):
    #     question = UserAnswer.objects.all().filter(quiz_taker=self)
    #     self.score = sum([i.score for i in question])
    #
    #     self.user.total_score = self.score
    #     self.user.save()
    #     super().save(*args, **kwargs)


    def __str__(self):
        return self.user.username


class UserAnswer(models.Model):
    quiz_taker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    time = models.PositiveIntegerField()
    score = models.IntegerField(default=0)

    def save(self,  *args, **kwargs):
        quest = Question.objects.get(pk = self.question_id)
        quiz = Quiz.objects.get(pk=self.quiz_id)
        user_answer = quest.answer_set.get(label=self.answer)
        if quest.get_correct_answer().label == user_answer.label:
        # if str(self.answer) == str(self.answer.label):
            if self.time == 1:
                self.score = (100 - (100 / int(self.question.timer) * int(self.time)) + 100 / int(self.question.timer))
            elif self.time > 1:
                self.score = (100 - (100 / int(self.question.timer) * int(self.time)))
            else:
                self.score = 0
        super().save()


    def __str__(self):
        return f'{self.quiz_taker.user} : {self.score}'



@receiver(pre_save, sender=Quiz)
def slugify_name(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.name)


