from django.shortcuts import render
from django.http import HttpResponse

def handle_bad_request_view(request, exception, *args, **kwargs):
    template_name = 'error/400.html'
    title = 'Nieprawidłowe żądanie | '                         
    return render(request, template_name, {'title': title})

def handle_permission_denied_view(request, exception, *args, **kwargs):
    template_name = 'error/403.html'
    title = 'Odmowa dostępu | '                         
    return render(request, template_name, {'title': title})

def handle_page_not_found_view(request, exception, *args, **kwargs):
    template_name = 'error/404.html'
    title = 'Strona nieodnaleziona | '                         
    context = {'title': title}
    return render(request, template_name, {'title': title})
    
def handle_server_error_view(request, *args, **kwargs):
    template_name = 'error/500.html'
    title = 'Błąd serwera | '                         
    context = {'title': title}
    return render(request, template_name, {'title': title})