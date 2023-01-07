import pyrebase

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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


def home(request):
    if ('login' in request.session):
        #return render(request,"main/home.html")
        #return render(request,"main/test.html")
        return render(request,"main/argon-dashboard-master/index.html")
    else:
        return redirect('/main')


def paraphrase_text(request):
    input_text=''
    words=''
    output_text=''
    filtered_list=''
    replacement_words=''
    synonym_list=''
    
    if is_ajax(request=request):
        input_text = request.POST['input_text']
        obj = Main()
        words, output_text, filtered_list, replacement_words, synonym_list = obj.main(input_text)
                
        json_data={
            'input_text': input_text, 
            'words' : words,
            'output_text': output_text,
            'filtered_list' : filtered_list, 
            'synonym_list' : synonym_list,  
            'replacement_words' : replacement_words
        }
        
        db_data={
            'sensitive_words' : filtered_list,
            'replacement_words' : replacement_words
        }
        
        db.child("users").child(request.session['user_id']).child("detection").push(db_data)
        return JsonResponse(json_data)
    
    
@csrf_exempt
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
    
    users = db.child('users').order_by_child('account/email').equal_to(email).get()
    for user in users.each():
        request.session['user_id'] = user.key()
        
    return redirect('/main/home')


@csrf_exempt
def sign_up(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']

    try:
        # creating a user with the given email and password
        user=auth.create_user_with_email_and_password(email,password)
    except:
        return redirect('/main')
    
    db_data = {
        'account' : {
            'username' : username,
            'email' : email,
            'password' : password,
        }
    }

    db.child("users").push(db_data)
    return redirect('/main')
 
 
def logout(request):
    try:
        del request.session['session_id']
        del request.session['email']
        del request.session['login']
        del request.session['user_id']
    except:
        pass
    return redirect('/main')
 
 
def reset(request):
	return render(request, "main/reset.html")


def post_reset(request):
	email = request.POST.get('email')
	try:
		auth.send_password_reset_email(email)
		message = "A email to reset password is successfully sent"
		return render(request, "main/reset.html", {"msg":message})
	except:
		message = "Something went wrong, Please check the email you provided is registered or not"
		return render(request, "main/reset.html", {"msg":message})
