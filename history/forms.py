
from django import forms

from .models import History


class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ['amount', 'returned', 'balance_after_borrow', 'balance_after_return']
    
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('user')
        super(HistoryForm, self).__init__(*args,**kwargs)
    
    def save(self, commit=True):
        instance = super(HistoryForm, self).save(commit=False)
        instance.user = self.user
        return instance
         


class DepositForm(HistoryForm):
    
    class Meta(HistoryForm.Meta):
        fields = ['amount']
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount < 0:
            raise forms.ValidationError('Amount must be greater than 0')

        return amount