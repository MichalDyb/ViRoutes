from django.shortcuts import redirect, render
from django.views import View
from.forms import UserChangePasswordForm, UserLoginForm, UserRegisterForm, UserChangeEmailForm, UserChangePersonalDataForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User

class RegisterView(View):
    template_name = 'accounts/register.html'   
    title = 'Rejestracja | '                       
    form = UserRegisterForm()          

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:index')
        return render(request, self.template_name, {'title': self.title, 'form': self.form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:index')
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('home:index')
        else:
            return render(request, self.template_name, {'title': self.title, 'form': form})

class LoginView(View):
    template_name = 'accounts/login.html'   
    title = 'Logowanie | '        
    form = UserLoginForm()            

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:index')
        return render(request, self.template_name, {'title': self.title, 'form': self.form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:index')
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            next = request.GET.get('next')
            login(request, user)
            if next:
                return redirect(next)
            else:
                return redirect('home:index')
        else:
            return render(request, self.template_name, {'title': self.title, 'form': form})

class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home:index')

class IndexView(LoginRequiredMixin, View):
    template_name = 'accounts/index.html'   
    title = 'Moje konto | '               

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': self.title})

class ChangeEmailView(LoginRequiredMixin, View):
    template_name = 'accounts/change-email.html'   
    title = 'Zmień email | Moje konto | '                           

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': self.title, 'form': UserChangeEmailForm({'email': request.user.email}, request=request)})

    def post(self, request, *args, **kwargs):
        form = UserChangeEmailForm(request.POST, request=request)
        if form.is_valid():
            user = User.objects.get(username = request.user.username)
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            return redirect('accounts:index')
        else:
            return render(request, self.template_name, {'title': self.title, 'form': form})

class ChangePasswordView(LoginRequiredMixin, View):
    template_name = 'accounts/change-password.html'   
    title = 'Zmień hasło | Moje konto | '                          

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': self.title, 'form': UserChangePasswordForm(request=request)})

    def post(self, request, *args, **kwargs):
        form = UserChangePasswordForm(request.POST, request=request)
        if form.is_valid():
            user = User.objects.get(username = request.user.username)
            user.set_password(form.cleaned_data['newPassword'])
            user.save()
            login(request, user)
            return redirect('accounts:index')
        else:
            return render(request, self.template_name, {'title': self.title, 'form': form})

class ChangePersonalDataView(LoginRequiredMixin, View):
    template_name = 'accounts/change-personal-data.html'   
    title = 'Zmień dane personalne | Moje konto | '    

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': self.title, 'form': UserChangePersonalDataForm({'first_name': request.user.first_name, 'last_name': request.user.last_name})})

    def post(self, request, *args, **kwargs):
            form = UserChangePersonalDataForm(request.POST)
            if form.is_valid():
                user = User.objects.get(username = request.user.username)
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()
                login(request, user)
                return redirect('accounts:index')
            else:
                return render(request, self.template_name, {'title': self.title, 'form': form})