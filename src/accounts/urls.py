from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/', IndexView.as_view(), name='index'),
    path('account/change-email/', ChangeEmailView.as_view(), name='change-email'),
    path('account/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('account/change-personal-data/', ChangePersonalDataView.as_view(), name='change-personal-data'),
]