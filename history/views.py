import time

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.db.models import Sum
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from accounts.models import UserAccount

from .constants import BORROW, DEPOSIT, RETURN
from .forms import DepositForm, HistoryForm
from .models import History


# Create your views here.
def send_transaction_email(user,amount,subject,template_name):
    mail_subject = subject
    message = render_to_string(template_name, {
        'user': user,
        'amount': amount,
    })
    send_email = EmailMessage(
        mail_subject,
        message,
        to=[user.email]
    )
    send_email.content_subtype = 'html'
    send_email.send()

class HistoryViewMixin(LoginRequiredMixin,CreateView):
    model = History
    template_name = 'history_form.html'
    title = ''
    success_url = reverse_lazy('home')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user.account})
        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

class DepositView(HistoryViewMixin):
    form_class = DepositForm
    title = 'Deposit'
    
    def form_invalid(self, form):
        messages.warning(self.request, 'Deposit failed')
        return super().form_invalid(form)
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        user = self.request.user
        user_account = UserAccount.objects.get(user=user)
        user_account.balance += amount
        user_account.save(update_fields=['balance'])
        History.objects.create(
            user=user_account,
            amount=amount,
            balance_after_borrow=None,
            balance_after_return=None,
            history_type=DEPOSIT
        )
        messages.success(self.request, 'Deposit successful')
        send_transaction_email(user,amount,'Deposit','deposit_email.html')
        return super().form_valid(form)
    
    