from django.shortcuts import render, redirect

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Sum
from django.urls import reverse_lazy
from django import forms
from django.forms import EmailField
from django.contrib.auth.models import User

from . import models

class UserCreationForm(UserCreationForm):
    email = EmailField(label= ("Email address"), required=True,
        help_text= ("Required."))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class login_view(LoginView):
    template_name = 'base/login.html'
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task_list')



class register_view(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(register_view, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task_list')
        return super(register_view, self).get(*args, **kwargs)


class list_tasks(LoginRequiredMixin, ListView):
    model = models.task
    context_object_name = 'tasks'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        context['exp_sum'] = models.task.objects.aggregate(Sum('exp'))['exp__sum']%100
        context['current_lvl'] = models.task.objects.aggregate(Sum('exp'))['exp__sum']//100
        context['exp_left'] = 100 - models.task.objects.aggregate(Sum('exp'))['exp__sum']%100
        tmp = models.Profile.objects.filter(user=self.request.user)[0]
        print("\n\n")
        print(tmp)
        print("\n\n")




        search_input = self.request.GET.get('search_text_area') or ''

        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)

        context[search_input] = search_input

        return context


class task_detail(LoginRequiredMixin, DetailView):
    model = models.task
    context_object_name = 'task_detail'

class task_create(LoginRequiredMixin, CreateView):
    model = models.task
    fields = ['title', 'description', 'exp', 'dateTime_created']
    success_url = reverse_lazy('task_list')

    def get_form(self, form_class = None):
        form = super(task_create, self).get_form(form_class)
        form.fields['dateTime_created'].widget = forms.SelectDateWidget()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(task_create, self).form_valid(form)


class task_update(LoginRequiredMixin, UpdateView):

    model = models.task
    fields = ['title', 'description', 'complete', 'exp']
    success_url = reverse_lazy('task_list')


class task_delete(LoginRequiredMixin, DeleteView):
    model = models.task
    success_url = reverse_lazy('task_list')

