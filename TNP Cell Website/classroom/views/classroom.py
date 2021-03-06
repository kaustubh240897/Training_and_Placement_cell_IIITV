from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

#homePage
def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:my_jobs')
        else:
            return redirect('students:quiz_list')
    return render(request, 'classroom/SE_home.html')

#why_we

def why_we(request):
    return render(request, 'classroom/WHY_we.html')
