from django.db import models

from accounts.models import UserAccount


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    borrow_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    author = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    def __str__(self):
        return  self.review[:10] + '...' if len(self.review) > 10 else self.review 