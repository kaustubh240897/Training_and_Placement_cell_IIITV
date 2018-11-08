from .models import User, PersonalDetails, OrganizationalDetails, Job
from django.contrib.auth.models import AbstractUser
from django.contrib import admin

admin.site.register(User)
admin.site.register(PersonalDetails)
admin.site.register(OrganizationalDetails)
admin.site.register(Job)