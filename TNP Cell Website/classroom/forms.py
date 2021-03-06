from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from classroom.models import (Answer, Question, Student, StudentAnswer,
                               PersonalDetails, OrganizationalDetails, Job, User, TakenJob)

class TeacherSignUpForm(UserCreationForm):

          email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

          class Meta(UserCreationForm.Meta):
           model = User

          fields = ('username', 'email', 'password1', 'password2')
          def save(self, commit=True):
             user = super().save(commit=False)
             user.is_teacher = True
             if commit:
                user.save()
                return user



class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')



    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        # student.interests.add(*self.cleaned_data.get('interests'))
        return user





class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', )


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')

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