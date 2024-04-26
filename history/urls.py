
from django.urls import path

from .views import DepositView

urlpatterns = [
    path('deposit/', DepositView.as_view(), name='deposit_money'),
]
