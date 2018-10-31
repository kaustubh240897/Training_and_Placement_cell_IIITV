from .models import User, Student, StudentAnswer,Subject,Answer,Question,Quiz,TakenQuiz, PersonalDetails, OrganizationalDetails, Job
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
admin.site.register(PersonalDetails)
admin.site.register(OrganizationalDetails)
admin.site.register(Job)
admin.site.register(Resume)
admin.site.register(Education)
