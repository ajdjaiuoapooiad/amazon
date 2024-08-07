from django import forms
from base.models import User
from django.contrib.auth import get_user_model



class UserCreateForm(forms.ModelForm):
    password=forms.CharField()
    
    #signupのnameで受け取った値をuserに格納する
    class Meta:
        model=get_user_model()
        fields={'username','email','password'}
        
    def clean_password(self):
        password=self.cleaned_data.get('password')
        return password
    
    def save(self,commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
        return user
            