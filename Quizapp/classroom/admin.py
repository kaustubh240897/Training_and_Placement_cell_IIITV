from .models import User, Student, StudentAnswer,Answer,Question,Quiz,TakenQuiz, PersonalDetails, OrganizationalDetails,TakenJob, Job
from django.contrib.auth.models import AbstractUser
from django.contrib import admin

admin.site.register(User)
admin.site.register(Student)
admin.site.register(StudentAnswer)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(TakenQuiz)
admin.site.register(PersonalDetails)
admin.site.register(OrganizationalDetails)
admin.site.register(Job)
admin.site.register(TakenJob)