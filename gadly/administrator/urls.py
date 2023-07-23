from django.urls import path
from .views import *

app_name = 'administrator'
urlpatterns = [
    path('', ind, name='index'),
    path('para/', para, name='paraphrase'),
    path('plag/', plag, name='plagiarism'),
    path('users/', users, name='users'),
    path('users/add/', add_user, name='add_user'),
    path('users/get/', get_user, name='get_user'),
    path('users/upd/', upd_user, name='update_user'),
    path('users/del/', del_user, name='delete_user'),
    path('paras/', paras, name='paraphrases'),
    path('paras/<int:user_id>/', paras_user, name='paraphrases_user'),
    path('paras/det/', paras_det, name='paraphrases_detail'),
    path('reps/', reps, name='replacements'),
    path('reps/<int:user_id>/', reps_user, name='replacements_user'),
    path('reps/det/', reps_det, name='replacements_detail'),
    path('logout/', logout, name='logout'),
]