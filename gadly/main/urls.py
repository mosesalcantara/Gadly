from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.sign),
    path('sign_in/', views.sign_in),
    path('sign_up/', views.sign_up),
    path('reset/', views.reset),
    path('post_reset/', views.post_reset),
    path('home/', views.home),
    path('paraphrase_text/', views.paraphrase_text),
    path('user/profile/', views.profile),
    path('user/history/', views.history),
    path('user/replacements/', views.replacements),
    path('admin/users/', views.all_users),
    path('admin/paraphrases/', views.all_paraphrases),
    path('admin/replacements/', views.all_replacements),
    path('grammar_check/', views.grammar_check),
    path('logout/', views.logout),
]
