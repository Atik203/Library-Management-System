from django.db import models

from accounts.models import UserAccount
from books.models import Book

from .constants import HISTORY_TYPE


# Create your models here.
class History(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='history')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='history', null=True, blank=True)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    returned = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    balance_after_borrow = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    balance_after_return = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    history_type = models.CharField(max_length=10, choices=HISTORY_TYPE, null=True, blank=True)
    def __str__(self):
        return self.user.user.username
    
    class Meta:
        ordering = ['return_date']