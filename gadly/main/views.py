from gingerit.gingerit import GingerIt

import pyrebase
import json

from django.shortcuts import render, redirect
from django.http import JsonResponse

from .main import Main

config={
  "apiKey": "AIzaSyCnqRG_3w5Gb4JTlNwyMIVJs98crMBRULM",
  "authDomain": "gadly-610fb.firebaseapp.com",
  "databaseURL": "https://gadly-610fb-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "gadly-610fb",
  "storageBucket": "gadly-610fb.appspot.com",
  "messagingSenderId": "350424029795",
  "appId": "1:350424029795:web:9d900d96122c6d43f97656",
  "measurementId": "G-MQYBSZQ38P"
}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database()

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def sign(request):
    return render(request,"main/sign.html")


def sign_up(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    type = request.POST['type']

    try:
        # creating a user with the given email and password
        user=auth.create_user_with_email_and_password(email,password)
    except:
        return redirect('/main')
    
    db_data = {
        'username' : username,
        'email' : email,
        'password' : password,
        'type' : type,
    }

    db.child("users").push(db_data)
    return redirect('/main')


def sign_in(request):
    email=request.POST['email']
    pasw=request.POST['password']
    
    try:
        # if there is no error then signin the user with given email and password
        user=auth.sign_in_with_email_and_password(email,pasw)
    except:
        message="Invalid Credentials!!Please Check your Data"
        # return render(request,"Login.html",{"message":message})
        return redirect('/main/')
    
    session_id=user['idToken']
    request.session['session_id']=str(session_id)
    request.session['email'] = email
    request.session['login'] = True
    # return render(request,"main/paraphrase.html",{"email":email})
    
    user = db.child('users').order_by_child('email').equal_to(email).get().val()
    for user_id,acc in user.items():
        request.session['user_id'] = user_id
        request.session['type'] = acc['type']
        
    return redirect('/main/home')


def home(request):
    if ('login' in request.session):
        if (request.session['type'] == 'admin'):
            count_users = 0
            count_paras = 0
            count_reps = 0
            users = db.child('users').get().val()
            for id,field in users.items():
                count_users += 1
                if ('paraphrases' in field):
                    for par_id,par_dict in field['paraphrases'].items():
                        count_paras += 1
                if ('replacements' in field):
                    for rep_id,rep_dict in field['replacements'].items():
                        count_reps += 1
            
            context = {
                'count_users':count_users,
                'count_paras':count_paras,
                'count_reps':count_reps,
            }
                    
            return render(request,"main/admin/home.html",context)
        elif (request.session['type'] == 'user'):
            return render(request,"main/user/home.html")
    else:
        return redirect('/main')


def paraphrase_text(request):
    if ('login' in request.session):
        input_text=''
        words=''
        output_text=''
        filtered_list=''
        replacement_words=''
        synonym_list=''
        rep_dict=''
        new_rep_dict={}
        
        if is_ajax(request=request):
            input_text = request.POST['input_text']
            parser = GingerIt()
            input_text = parser.parse(input_text)
            input_text = input_text['result']
            print(input_text)
            obj = Main()
            words, output_text, filtered_list, replacement_words, synonym_list, rep_dict = obj.main(input_text)

            for det, rep in rep_dict.items():
                det = det.lower()
                rep = rep.lower()
                new_rep_dict[det] = rep
            
            json_data={
                'input_text': input_text, 
                'words' : words,
                'output_text': output_text,
                'filtered_list' : filtered_list, 
                'synonym_list' : synonym_list,  
                'replacement_words' : replacement_words,
                'rep_dict' : new_rep_dict
            }            
            db.child("users").child(request.session['user_id']).child("paraphrases").push(new_rep_dict)
            return JsonResponse(json_data)
    else:
        return redirect('/main')
def grammar_check(request):
    if ('login' in request.session):
        if is_ajax(request=request):

            output_text = request.POST['output_text']
            parser = GingerIt()
            output = parser.parse(output_text)
            json_data={
            'output':output['result']
            }
            return JsonResponse(json_data)
    else:
        return redirect('/main')
def profile(request):
    if ('login' in request.session):
        acc = db.child("users").child(request.session['user_id']).get().val()
        context = {
            'acc':acc
        }
        return render(request,'main/user/profile.html',context)
    else:
        return redirect('/main')


def history(request):
    if ('login' in request.session):
        paras = db.child("users").child(request.session['user_id']).child("paraphrases").get().val()
        context = {
            'paras':paras
        }
        return render(request,'main/user/history.html',context)
    else:
        return redirect('/main')
    

def replacements(request):
    if ('login' in request.session):
        reps = db.child("users").child(request.session['user_id']).child("replacements").get().val()
        context = {
            'reps':reps
        }
        return render(request,'main/user/replacements.html',context)
    else:
        return redirect('/main')
    

def all_users(request):
    if ('login' in request.session):
        accs = {}
        users = db.child('users').get().val()
        for id,field in users.items():
            accs[id] = field
        context = {
            'accs':accs,
        }
                
        return render(request,"main/admin/users.html",context)
    else:
        return redirect('/main')
 
 
def all_paraphrases(request):
    if ('login' in request.session):
        paras = {}
        users = db.child('users').get().val()
        for id,field in users.items():
            username = field['username']
            if ('paraphrases' in field):
                paras[username] = field['paraphrases']
        context = {
            'paras':paras,
        }
                
        return render(request,"main/admin/paraphrases.html",context)
    else:
        return redirect('/main')
   
    
def all_replacements(request):
    if ('login' in request.session):
        reps = {}
        users = db.child('users').get().val()
        for id,field in users.items():
            username = field['username']
            if ('replacements' in field):
                reps[username] = field['replacements']
        context = {
            'reps':reps,
        }
                
        return render(request,"main/admin/replacements.html",context)
    else:
        return redirect('/main') 


def logout(request):
    replacements = {}
    if is_ajax(request=request):
        replacements = json.loads(request.POST['replacements'])
        db.child("users").child(request.session['user_id']).child("replacements").push(replacements)
    try:
        del request.session['session_id']
        del request.session['email']
        del request.session['login']
        del request.session['user_id']
        del request.session['type']
    except:
        pass
    if (is_ajax(request=request)):
        return JsonResponse(replacements)
    else:
        return redirect("/main")


def reset(request):
	return render(request, "main/reset.html")


def post_reset(request):
	email = request.POST['email']
	try:
		auth.send_password_reset_email(email)
		message = "A email to reset password is successfully sent"
		return render(request, "main/reset.html", {"msg":message})  
	except:
		message = "Something went wrong, Please check the email you provided is registered or not"
		return render(request, "main/reset.html", {"msg":message})
