from django.urls import path
from .views import *

app_name = 'user'
urlpatterns = [
    path('', ind, name='index'),
    path('plag/', plag, name='plagiarism'),
    path('prof/', prof, name='profile'),
    path('paras/', paras, name='paraphrases'),
    path('paras/det/', paras_det, name='paraphrases_detail'),
    path('reps/', reps, name='replacements'),
    path('reps/det/', reps_det, name='replacements_detail'),
    path('logout/', logout, name='logout'),
]