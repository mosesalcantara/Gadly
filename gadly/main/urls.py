from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'main'
urlpatterns = [
  path('', sign, name='index'),
  path('test/',test),
  path('des/',des),
  path('admin/para/<int:user_id>/', paraphrase_detail, name='paraphrase_detail'),
  path('admin/para/detail/', paraphrase_detailed, name='paraphrase_detailed'),
  path('admin/rep/<int:user_id>/', replacement_detail, name='replacement_detail'),
  path('admin/rep/detail/', replacement_detailed, name='replacement_detailed'),
  path('user/para/', hist, name='hist'),
  path('user/repl/', repla, name='repla'),
  path('structural_changes/', structural_changes),
  path('sign_in/', sign_in),
  path('sign_up/', sign_up),
  path('sign_up/confirm/<uid_b64>/<token>/', sign_up_confirm, name='sign_up_confirm'),
  path('reset/', reset, name='reset'),
  path('reset/confirm/<uid_b64>/<token>/', reset_confirm, name='reset_confirm'),
  path('home/', home),
  path('admin/', admin_para),
  path('paraphrase_text/', paraphrase_text),
  path('upl_file/', upl_file),
  path('plag/', plag),
  path('user/profile/', profile),
  path('user/history/', history),
  path('user/replacements/', replacements),
  path('admin/users/', all_users),
  path('admin/users/add/', add_user),
  path('admin/users/get/', get_user),
  path('admin/users/upd/', upd_user),
  path('admin/users/del/', del_user),
  path('admin/paraphrases/', all_paraphrases),
  path('admin/replacements/', all_replacements),
  path('logout/', logout),
  path('api_signin/', api_signin),
  path('api_signup/', api_signup),
  path('api_para/', api_para),
  path('check_plag/', checkPlag)
]
