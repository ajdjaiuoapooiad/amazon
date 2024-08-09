from django.shortcuts import render
from django.views import generic
from base.models import Item,Profile,User
from base.forms import UserCreateForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages



class SignupView(generic.CreateView):
    form_class=UserCreateForm
    success_url='/login/'
    template_name='pages/signup_login.html'
    
    #message
    def form_valid(self,form):
        messages.success(self.request,'新規登録しました。')
        return super().form_valid(form)
    
    
class Login(LoginView):
    template_name='pages/signup_login.html'
    
    #message
    def form_valid(self,form):
        messages.success(self.request,'ログインしました。')
        return super().form_valid(form)
    
    def form_invalid(self,form):
        messages.error(self.request,'エラーでログインできませんでした。')
        return super().form_valid(form)
    

    
    
class AccountUpdateView(LoginRequiredMixin,generic.UpdateView):
    model=get_user_model()
    template_name='pages/account.html'
    fields={'username','email'}
    success_url='/account/'
    
    def get_object(self):
        # URL変数ではなく、現在のユーザーから直接pkを取得
        self.kwargs['pk']=self.request.user.pk
        return super().get_object()   
    
class ProfileUpdateView(LoginRequiredMixin,generic.UpdateView):
    model=Profile
    template_name='pages/profile.html'
    fields={'name','prefecture','city','address1','address2','tel'}
    success_url='/profile/'

    def get_object(self):
        # URL変数ではなく、現在のユーザーから直接pkを取得
        self.kwargs['pk']=self.request.user.pk
        return super().get_object()   