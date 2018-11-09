from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.http import JsonResponse, request
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from ..decorators import student_required
from ..forms import  StudentSignUpForm, TakeQuizForm
from ..models import Quiz, Student, TakenQuiz, User, Job, OrganizationalDetails, TakenJob
from django.http import HttpResponseRedirect


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:quiz_list')


# @method_decorator([login_required, student_required], name='dispatch')
# class StudentInterestsView(UpdateView):
#     model = Student
#     form_class = StudentInterestsForm
#     template_name = 'classroom/students/interests_form.html'
#     success_url = reverse_lazy('students:quiz_list')
#
#     def get_object(self):
#         return self.request.user.student
#
#     def form_valid(self, form):
#         messages.success(self.request, 'Interests updated with success!')
#         return super().form_valid(form)


@method_decorator([login_required, student_required], name='dispatch')
class QuizListView(ListView):
        model = Job
        #model = OrganizationalDetails
        template_name = 'classroom/students/quiz_list.html'
        context_object_name = 'job_list'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['job_list'] = Job.objects.all()

            print(context['job_list'])
            return context

    # model = Job
    # ordering = ('name',)
    # context_object_name = 'quizzes'
    # template_name = 'classroom/students/quiz_list.html'
    #
    # # def post(self, request, *args, **kwargs):
    # #     # self.status_form = StatusForm(self.request.POST or None)
    # #     print(args)
    # #     print(kwargs)
    # #     if self.status_form.is_valid():
    # #         pass
    # #     else:
    # #         # return super(List, self).post(request, *args, **kwargs)
    # #         pass
    #
    # def get_queryset(self):
    #     student = self.request.user.student
    #     student_interests = student.interests.values_list('pk', flat=True)
    #     taken_quizzes = student.quizzes.values_list('pk', flat=True)
    #     queryset = Quiz.objects.filter(subject__in=student_interests) \
    #         .exclude(pk__in=taken_quizzes) \
    #         .annotate(questions_count=Count('questions')) \
    #         .filter(questions_count__gt=0)
    #     return queryset


@method_decorator([login_required, student_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'classroom/students/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes \
            .select_related('quiz', 'quiz__subject') \
            .order_by('quiz__name')
        return queryset


@login_required
@student_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student
    print(request.POST)
    if 'password' in request.POST:
        if request.POST['password'] == quiz.password or quiz.password is None:
            if student.quizzes.filter(pk=pk).exists():
                return render(request, 'students/taken_quiz_list.html')
        else:
            return JsonResponse({'error': 'Password did not match'})
    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_questions(quiz).exists():
                    return redirect('students:take_quiz', pk)
                else:
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
                    else:
                        messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, score))
                    return redirect('students:quiz_list')
        else:
            form = TakeQuizForm(question=question)

        return render(request, 'classroom/students/take_quiz_form.html', {
            'quiz': quiz,
            'question': question,

            'form': form,
            'progress': progress
        })






@method_decorator([login_required, student_required], name='dispatch')
class TakenJobListView(ListView):
    model = TakenJob
    context_object_name = 'object_list'
    template_name = 'classroom/students/taken_quiz_list.html'
 
    def get_queryset(self):
        return self.kwargs['pk']

    def get_context_data(self, *args, **kwargs):
        print(args)
        context = super().get_context_data(**kwargs)
        jb = Job.objects.get(pk=self.get_queryset())
        check_student = TakenJob.objects.all()
        flag = True
        for i in check_student:
            if(i.student == self.request.user.student and i.applied_job == jb):
                flag = False
        if flag:
            messages.success(self.request, 'Applied Successfully !!!')
            taken_job = TakenJob(student=self.request.user.student, applied_job=jb).save()
        else :
            messages.error(self.request, 'Already registered for this job!!!!')
        context['object_list'] = TakenJob.objects.filter( applied_job=jb)
        return context



@method_decorator([login_required, student_required], name='dispatch')
class TakenJobsListView(ListView):
    model = TakenJob
    context_object_name = 'object_list'
    template_name = 'classroom/students/TakenJobs.html'
    def get_context_data(self, *args, **kwargs):
        print(args)
        context = super().get_context_data(**kwargs)
        check_student = TakenJob.objects.all().filter(student=self.request.user.student)
        context['object_list'] = TakenJob.objects.filter(student=self.request.user.student)
        return context