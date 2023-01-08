from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm, PwdChangeForm


app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="registration/login.html",
                                                authentication_form=UserLoginForm), name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit, name='edit'),
    path('profile/delete/', views.delete_user, name='deleteuser'),
    path('register/', views.accounts_register, name='register'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name="registration/password_change_form.html",
                                                                   form_class=PwdChangeForm), name='pwdforgot'),
    path('friendlist/', views.friendlist, name='friendlist'),
    path('sentrequest/<str:username>', views.sentrequest, name='sentrequest'),
    path('accept/<str:username>', views.accept, name='accept'),
    path('decline/<str:username>', views.decline, name='decline'),
    path('cancel/<str:username>', views.cancel, name='cancel'),
]
