from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from classroom.models import (PersonalDetails, OrganizationalDetails, Job, User)

class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):
    # interests = forms.ModelMultipleChoiceField(
    #     queryset=Subject.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=True
    # )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        # student = Student.objects.create(user=user)
        # student.interests.add(*self.cleaned_data.get('interests'))
        return user

class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = PersonalDetails
        fields = ('first_name','last_name','email','mobile')
        
class OrganizationalDetailsForm(forms.ModelForm):
    class Meta:
        model = OrganizationalDetails
        fields = ('organization_name','organization_email','organization_description')

class PostJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('date_of_posting','offer','primary_profile','location','no_of_position','apply_deadline','drive_date','organization_sector','job_description','package','required_skills','min_CPI','selection_process','other_details')



