from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

import datetime

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

#For Training and Place Cell - IIIT Vadodara    

OFFER = (
    (1, ('Job')),
    (2, ('Internship')),
    (3, ('Job + Internship'))
)
SELECTION_PROCESS = (
    (1, ('Shortlisting from Resumes')),
    (2, ('Written Test - Aptitude')),
    (3, ('Group Discussion')),
    (4, ('Personal Interview (Technical + HR)')),
    (5, ('Written Test - Technical')),
)

class OrganizationalDetails(models.Model):
    class Meta:
        verbose_name_plural = 'OrganizationalDetails'

    organization_name = models.CharField(max_length= 255, blank= True, unique= True)
    organization_email = models.EmailField(max_length= 70, blank= True, null=True, unique= True)
    organization_description = models.CharField(max_length= 255)
    #organization_logo = models.ImageField(upload_to='organization_logo', blank=True)

    def __str__(self):
        return self.organization_name

class PersonalDetails(models.Model):
    class Meta:
        verbose_name_plural = 'PersonalDetails'
    
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, blank=True, null=True)
    organization = models.OneToOneField(OrganizationalDetails,on_delete = models.CASCADE, blank=True, null=True, related_name='personal_detail') 
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField(max_length= 70,blank= True, null=True, unique= True)
    mobile = models.IntegerField()

    def __str__(self):
        return self.first_name + " " + self.last_name


class Job(models.Model):
    class Meta:
        verbose_name_plural = 'Job'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    organization = models.ForeignKey(OrganizationalDetails, on_delete = models.CASCADE, blank=True, null=True, related_name='Job')
    date_of_posting = models.DateField(default=datetime.date.today)
    offer = models.IntegerField(choices=OFFER, default=1)
    primary_profile = models.CharField(max_length= 255)
    location = models.CharField(max_length= 255)
    no_of_position = models.IntegerField()
    apply_deadline = models.DateField(default=datetime.date.today)
    drive_date = models.DateField(default=datetime.date.today)
    organization_sector = models.CharField(max_length= 255)
    job_description = models.CharField(max_length= 255)
    package = models.DecimalField(decimal_places=2,max_digits=4)
    required_skills = models.CharField(max_length= 255)
    min_CPI = models.DecimalField(decimal_places=2,max_digits=4)
    selection_process = models.IntegerField(choices=SELECTION_PROCESS, default=1)
    other_details = models.CharField(max_length= 255)


    def __str__(self):
        return (str(self.date_of_posting) + " " + str(self.offer) + " " + self.primary_profile + " " + self.location + " " + str(self.no_of_position) + " " + 
                str(self.apply_deadline) + " " + str(self.drive_date) + " " + self.organization_sector + " " + 
                self.job_description + " " + str(self.package) + " " + self.required_skills + " " + str(self.min_CPI) + " " + 
                str(self.selection_process) + " " + self.other_details)


class TakenJob(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quizes')
    applied_job = models.ForeignKey(Job, on_delete=models.CASCADE, null='TRUE',blank='TRUE' , related_name='applied_job')


class Submitter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(default=datetime.date.today)

