
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import (BookDetailsView, BorrowBookView, CategoryWiseBooksView,
                        HomeView, ReturnBookView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('accounts.urls')),
    path('history/', include('history.urls')),
    path('category/<slug:slug>/', CategoryWiseBooksView.as_view(), name='category_wise_books'),
    path('book/<int:id>/', BookDetailsView.as_view(), name='book_details'),
    path('book/borrow/<int:id>/', BorrowBookView.as_view(), name='borrow_book'),
    path('book/return/<int:id>/', ReturnBookView.as_view(), name='return_book'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)