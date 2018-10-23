from .models import User, Student, StudentAnswer,Subject,Answer,Question,Quiz,TakenQuiz
from django.contrib.auth.models import AbstractUser
from django.contrib import admin

admin.site.register(User)
admin.site.register(Student)
admin.site.register(StudentAnswer)
admin.site.register(Subject)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(TakenQuiz)
