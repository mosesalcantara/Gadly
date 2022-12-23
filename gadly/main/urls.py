from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.sign, name='sign'),
    path('sign_in/', views.sign_in),
    path('sign_up/', views.sign_up),
    path('reset/', views.reset),
    path('post_reset/', views.post_reset),
    path('home/', views.home),
    path('paraphrase_text/', views.paraphrase_text),
    path('logout/', views.logout),
]
