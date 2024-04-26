from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserAccount


class RegistrationForm(UserCreationForm):
    birthday = forms.DateField(help_text='Required. Format: YYYY-MM-DD',widget=forms.DateInput(attrs={'type': 'date'})  )
    phone = forms.CharField(max_length=20)
    address = forms.CharField(max_length=100)
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['password1'].help_text=None
      self.fields['password2'].help_text=None
      for field in self.fields:
                self.fields[field].widget.attrs.update({
                    'class': (
                        'appearance-none block w-full bg-gray-200 '
                        'text-gray-700 border border-gray-200 rounded '
                        'py-3 px-4 leading-tight focus:outline-none '
                        'focus:bg-white focus:border-gray-500'
                    ) 
                })    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email', 'birthday', 'phone', 'address']
        
        help_texts = {
            'username': None,
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        UserAccount.objects.create(user=user,phone=self.cleaned_data['phone'],address=self.cleaned_data['address'],birthday=self.cleaned_data['birthday'])
        return user