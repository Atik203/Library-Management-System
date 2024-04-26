from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from books.forms import ReviewForm
from books.models import Book, Category, Review
from history.constants import BORROW, RETURN
from history.models import History


def send_transaction_email(user,amount,subject,template_name,book):
    mail_subject = subject
    message = render_to_string(template_name, {
        'user': user,
        'amount': amount,
        'book': book,
    })
    send_email = EmailMessage(
        mail_subject,
        message,
        to=[user.user.email]
    )
    send_email.content_subtype = 'html'
    send_email.send()



class HomeView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        context['categories'] = Category.objects.all()
        return context


class CategoryWiseBooksView(ListView):
    model = Book
    template_name = 'index.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Book.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class BookDetailsView(DetailView):
    model = Book
    template_name = 'book_details.html'
    context_object_name = 'book'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(book=self.object)
        context['form'] = ReviewForm()
        if self.request.user.is_authenticated:
            context['can_review'] = History.objects.filter(user=self.request.user.account, 
                                                       book=self.get_object()).exists()
        else:
            context['can_review'] = False    
        return context
    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = self.get_object()
            try:
               review.user = request.user.account
            except ObjectDoesNotExist:
                messages.error(request, 'You need to create a user account before you can post a review.')
                return self.get(request, *args, **kwargs)
            review.save()
            messages.success(request, 'Review submitted successfully')
            return redirect('book_details', id=self.get_object().id)
        else:
            messages.error(request, 'Invalid data')
        return self.get(request, *args, **kwargs)

class BorrowBookView(View):
    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, id=self.kwargs['id'])
        user_account = request.user.account
        if user_account.balance < book.borrow_price:
            messages.error(request, 'You do not have enough balance to borrow this book')
            return redirect('book_details', id=book.id)
        balance_after_borrow = user_account.balance - book.borrow_price
        user_account.balance -= book.borrow_price
        user_account.save()
        History.objects.create(user=user_account, book=book,history_type=BORROW, amount=book.borrow_price, balance_after_borrow = balance_after_borrow, balance_after_return=None, returned=False, return_date=None)
        messages.success(request, 'Book borrowed successfully')
        send_transaction_email(user_account,book.borrow_price,'Book Borrowed','borrow_email.html',book)
        return redirect('profile')


class ReturnBookView(View):
    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, id=self.kwargs['id'])
        user_account = request.user.account
        history_record = History.objects.filter(user=user_account, book=book, returned=False).first() 
        
        history_record.balance_after_borrow = user_account.balance
        history_record.returned = True
        history_record.return_date = timezone.now()
        history_record.balance_after_return = user_account.balance + book.borrow_price
        history_record.amount = book.borrow_price
        user_account.balance += book.borrow_price
        history_record.history_type = RETURN
        
        user_account.save()
        history_record.save()

        messages.success(request, 'Book returned successfully')
        send_transaction_email(user_account,book.borrow_price,'Book Returned','return_email.html',book)
        return redirect('profile')    