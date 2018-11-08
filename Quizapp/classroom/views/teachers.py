from django.contrib import messages
from django.contrib.auth import login

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import teacher_required
from ..forms import TeacherSignUpForm
from ..models import PersonalDetails, OrganizationalDetails, Job,  User
from django.http import HttpResponseRedirect


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('teachers:add_personal')

## For Recruiter's Panel:

@method_decorator([login_required, teacher_required], name='dispatch')
class PersonalDetailsView(CreateView):
    model = PersonalDetails
    fields = ('first_name','last_name','email','mobile')
    template_name = 'classroom/teachers/personal_detail_form.html'
    context_object_name = 'personal'

    def form_valid(self, form):
        personal_details = form.save(commit=False)
        personal_details.user = self.request.user
        personal_details.save()
        messages.success(self.request, 'Added Personal Details Successfully.') 
        return HttpResponseRedirect("teachers:add_organization", personal_details.pk)
   

@method_decorator([login_required, teacher_required], name='dispatch')
class OrganizationDetailsView(CreateView):
    model = OrganizationalDetails
    fields = ('organization_name','organization_email','organization_description')
    template_name = 'classroom/teachers/organization_detail_form.html'

    def form_valid(self, form):
        organization_details = form.save(commit=False)
        organization_details.owner = self.request.user

        organization_details.save()
        messages.success(self.request, 'Added Organizational Details Successfully. ')
        #return HttpResponseRedirect("")
        return redirect('teachers:post_job', organization_details.pk)
        #return redirect('teachers:post_job')

@method_decorator([login_required, teacher_required], name='dispatch')
class PostJobView(CreateView):
    model = Job
    fields = ('date_of_posting','offer','primary_profile','location','no_of_position','apply_deadline','drive_date','organization_sector','job_description','package',
                'required_skills','min_CPI','selection_process','other_details')
    template_name = 'classroom/teachers/post_job_form.html'

    def form_valid(self, form):
        job = form.save(commit=False)
        # job.owner = self.request.user
        current_user = PersonalDetails.objects.filter(user=self.request.user)
        job.user = self.request.user
        # if(current_user[0])
        if len(current_user)==0:
            messages.error(self.request, 'please fill personal detail and organisation')
        else:
            job.organization = current_user[0].organization
            job.save()
            messages.success(self.request, 'Added Job Successfully.')
        return redirect('teachers:my_jobs', job.pk)
        #return HttpResponseRedirect("")
        #return redirect('teachers:my_jobs')

@method_decorator([login_required, teacher_required], name='dispatch')
class my_jobsView(ListView):
    model = Job
    template_name='classroom/teachers/quiz_change_list.html'
    context_object_name = 'jobs'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobs'] = Job.objects.all().filter(user = self.request.user)
        print(context['jobs'])
        return context


@method_decorator([login_required, teacher_required], name='dispatch')
class PersonalDetailListView(ListView):
    model = PersonalDetails
    context_object_name = 'personal'
    template_name = 'classroom/teachers/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['personal'] = PersonalDetails.objects.all().filter(user=self.request.user)
        print(context['personal'])
        return context
