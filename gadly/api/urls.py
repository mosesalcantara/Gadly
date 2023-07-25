from django.urls import path
from .views import *

app_name = 'api'
urlpatterns = [
    path('register/', reg, name='register'),
    path('login/', log, name='login'),
    path('para_txt/', para_txt, name='paraphrase_text'),
]