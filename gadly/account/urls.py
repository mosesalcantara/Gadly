from django.urls import path
from .views import *

app_name = 'account'
urlpatterns = [
    path('', ind, name='index'),
    path('login/', log, name='login'),
    path('register/', reg, name='register'),
    path('register/confirm/<uid_b64>/<token>/', reg_con, name='register_confirm'),
    path('reset/', res, name='reset'),
    path('reset/confirm/<uid_b64>/<token>/', res_con, name='reset_confirm'),
]