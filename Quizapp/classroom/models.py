from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from django.contrib.auth.models import User
import datetime


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Subject(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)


class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')
    password = models.CharField(blank=True, null=True, max_length=10)

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    interests = models.ManyToManyField(Subject, related_name='interested_students')

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return self.user.username


class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')
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
class RecruiterDetails(models.Model):
    first_name = models.CharField(max_length= 255)
    last_name = models.CharField(max_length= 255)
    email = models.EmailField(max_length= 70,blank= True, null=True, unique= True)
    mobile = models.IntegerField(max_length= 10)
    organization_name = models.CharField(max_length= 255, blank= True, unique= True)
    organization_email = models.EmailField(max_length= 70, blank= True, null=True, unique= True)
    organization_description = models.CharField(max_length= 255)
    # organization_logo = models.ImageField(upload_to='organization_logo', blank=True)

    def __str__(self):
        return (self.first_name + "  " + self.last_name + "  " + str(self.email) + "  " + str(self.mobile) + "  " + self.organization_name + "  " + str(self.organization_email)
                + "  " + self.organization_description)

class Job(models.Model):
    offer = models.IntegerField(choices=OFFER, default=1)
    primary_profile = models.CharField(max_length= 255)
    location = models.CharField(max_length= 255)
    no_of_position = models.IntegerField()
    apply_deadline = models.DateField(default=datetime.date.today)
    drive_date = models.DateField(default=datetime.date.today)
    organization_sector = models.CharField(max_length= 255)
    job_description = models.CharField(max_length= 255)
    package = models.DecimalField(decimal_places=1,max_digits=2)
    required_skills = models.CharField(max_length= 255)
    min_CPI = models.DecimalField(decimal_places=2,max_digits=4)
    selection_process = models.IntegerField(choices=SELECTION_PROCESS, default=1)
    other_details = models.CharField(max_length= 255)

    def __str__(self):
        #return (str(self.offer) + " " + self.primary_profile + " " + self.location + " " + str(self.no_of_position) + " " + str(self.apply_deadline) + " " + str(self.drive_date) + " " + self.organization_sector + " " + self.job_description + " " + str(self.package) + " " + self.required_skills + " " + str(self.min_CPI) + " " + str(self.selection_process) + " " + self.other_details)
        return (self.primary_profile + " " + self.location + " " + self.no_of_position + " " + self.apply_deadline + " " + self.organization_sector
                + " " + self.job_description + " " + self.package + " " + self.required_skills)

class Resume(models.Model):
    resume_field = models.CharField(max_length=256)

    def __str__(self):
        return self.resume_field

class Education(models.Model):
    resume_field = models.ForeignKey(Resume, on_delete=models.CASCADE)
    graduation_year = models.IntegerField()
    graduation_institute = models.CharField(max_length=256)
    graduation_percentage = models.DecimalField(decimal_places=2,max_digits=4)
    X_year = models.IntegerField()
    X_institute = models.CharField(max_length=256)
    X_percentage = models.DecimalField(decimal_places=2,max_digits=4)
    XII_year = models.IntegerField()
    XII_institute = models.CharField(max_length=256)
    XII_percentage = models.DecimalField(decimal_places=2,max_digits=4)
    postgrad_year = models.IntegerField()
    postgrad_institute = models.CharField(max_length=256)
    postgrad_percentage = models.DecimalField(decimal_places=2,max_digits=4)

    def __str__(self):
        return (self.graduation_year + " " + self.graduation_institute + " " + self.graduation_percentage)
