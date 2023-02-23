from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# home = ""

urlpatterns = [
    path('', views.home, name='web-home'),
    path('login/', auth_views.LoginView.as_view(template_name='xxhungry/loginpage.html'), name='web-login'),
    # path('login/', views.log_in, name='web-login'),
    path('log-out/', views.log_out, name='web-logout'),
    path('create-account/', views.create_account, name='web-create-account'),
    path('profile/', views.profile, name='web-profile'),
    path('upload-data/', views.upload_data, name='web-upload-data'),
    path('common-disease/', views.common_disease, name='web-common-disease'),
]
