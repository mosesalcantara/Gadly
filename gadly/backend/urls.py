from django.urls import path
from .views import *

app_name = 'backend'
urlpatterns = [
    path('upl_file/', upl_file, name='upload_file'),
    path('train/', train, name='train'),
    path('para_txt/', para_txt, name='paraphrase_text'),
    path('struct_changes/', struct_changes, name='structural_changes'),
    path('check_plag/', check_plag, name='check_plagiarism'),
]