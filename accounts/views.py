from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from history.models import History

from .forms import RegistrationForm
from .models import UserAccount


def send_confirm_email(user,subject,template_name):
    mail_subject = subject
    message = render_to_string(template_name, {
        'user': user,
    })
    send_email = EmailMessage(
        mail_subject,
        message,
        to=[user.email]
    )
    send_email.content_subtype = 'html'
    send_email.send()

# Create your views here.
class UserRegistrationView(FormView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Register'
        return context
    
    def form_valid(self, form):
        user=form.save()
        account = user.account
        print(account)
        login(self.request, user)
        messages.success(self.request, 'Account created successfully')
        send_confirm_email(user, 'Welcome to Library Management System', 'register_email.html')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.warning(self.request, 'Account creation failed')
        messages.warning(self.request, form.errors.as_text())
        return super().form_invalid(form)
    
class UserLoginView(LoginView):
    template_name = 'Login.html'
    success_url = reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context
    
    def form_valid(self, form):
        user=form.get_user()
        login(self.request, user)
        messages.success(self.request, 'Login successful')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.warning(self.request, 'Login failed')
        messages.warning(self.request, form.errors.as_text())
        return super().form_invalid(form)
    

def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful')
    return redirect('home')
   

class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'profile.html'
    model = History
    balance = 0.0
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user.account)
        self.balance = self.request.user.account.balance
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user.account
        return context
  

