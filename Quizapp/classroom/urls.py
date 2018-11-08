from django.urls import include, path

from .views import classroom, students, teachers

urlpatterns = [
    path('', classroom.home, name='home'),

    path('students/', include(([
        path('', students.QuizListView.as_view(), name='quiz_list'),
        path('taken/<int:pk>/', students.TakenJobListView.as_view(), name='taken_quiz_list'),
        path('takenjobs/', students.TakenJobsListView.as_view(), name='taken_job_list'),
        path('quiz/<int:pk>/', students.take_quiz, name='take_quiz'),
      ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.my_jobsView.as_view(), name='my_jobs'),
        path('quiz/details', teachers.PersonalDetailListView.as_view(), name='details_list'),
        path('quiz/add/personal', teachers.PersonalDetailsView.as_view(), name='add_personal'),
        path('quiz/add/organization', teachers.OrganizationDetailsView.as_view(), name='add_organization'),
        path('quiz/add/job', teachers.PostJobView.as_view(), name='post_job'),
        #path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),
        path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'classroom'), namespace='teachers')),
]
