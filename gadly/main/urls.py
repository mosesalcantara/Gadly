from django.urls import path
from . import views
from django.contrib import admin

app_name = 'main'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.sign, name='sign'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('reset/', views.reset, name='reset'),
    path('post_reset/', views.post_reset, name='post_reset'),
    path('home/', views.home, name='home'),
    path('paraphrase/', views.paraphrase, name='paraphrase'),
    path('logout/', views.logout, name="logout"),
    path('test2/', views.test2, name="test2"),
]
