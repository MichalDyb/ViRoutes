from django.shortcuts import render
from django.views import View 
from home.forms import SendEmailForm

class IndexView(View):
    template_name = 'home/index.html'   
    title = ''                       

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': self.title})

class PrivacyView(View):
    template_name = 'home/privacy.html'   
    title = 'Polityka Prywatności | '                       

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': self.title})

class CookiesView(View):
    template_name = 'home/cookies.html'   
    title = 'Polityka Cookies | '                       

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': self.title})

class ContactView(View):
    template_name = 'home/contact.html'   
    title = 'Kontakt | '        
    form = SendEmailForm()             

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': self.title, 'form': self.form})

    def post(self, request, *args, **kwargs):
        form = SendEmailForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            return render(request, self.template_name, {'title': self.title, 'form': self.form, 'message1': 'Witaj ' + data['name'], 'message2': 'Otrzymaliśmy twoją wiadomość email i wkrótce się odezwiemy...'})
        else:
            return render(request, self.template_name, {'title': self.title, 'form': form})

class AboutView(View):
    template_name = 'home/about.html'   
    title = 'O nas | '                       

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': self.title})



