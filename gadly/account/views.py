import base64

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password

from backend.models import User
from .forms import RegForm, LogForm

url = 'http://127.0.0.1:8000'


def ind(request):
    if request.method == "GET":
        logform = LogForm()
        regform = RegForm()
    return render(request, "acc/index.html", {"logform":logform,'regform':regform})


def reg(request):
    code = 0
    msgs = []
    regform = RegForm(request.POST)
    
    if regform.is_valid():
        name = regform.cleaned_data['name']
        phone = regform.cleaned_data['phone']
        email = regform.cleaned_data['email']
        uname = regform.cleaned_data['uname']
        pswd = regform.cleaned_data['pswd']
        utype = regform.cleaned_data['utype']
        token = get_random_string(length=8)
        
        try:
            pswd = make_password(pswd)
            user = User.objects.create(name=name,phone=phone,email=email,uname=uname,pswd=pswd,utype=utype,token=token)
            user.save()
            
            if utype == 'user':
                uid=str(user.pk)
                uid_bytes=uid.encode('ascii')
                uid_b64=base64.b64encode(uid_bytes)
                uid_b64=uid_b64.decode("ascii")
                uid_b64=uid_b64.replace('=', '')
                
                msg = ''' 
                    To initiate the account verification for your {email} Gadly App Account,
                    click the link below:

                    {url}/acc/register/confirm/{uid_b64}/{token}/

                    If clicking the link above doesn't work, please copy and paste the URL in a new browser
                    window instead.
                '''.format(email=user.email,url=url,uid_b64=uid_b64,token=token)
                
                send_mail(
                    "Gadly Account Verification",
                    msg,
                    "gadly@gmail.com",
                    [email],
                    fail_silently=False,
                )
        except:
            code = 500
            msgs.append('Registration Error')
        
        code = 200
        if utype == 'user':
            msgs.append('User Registered. Check your email to verify your account.')
        else: 
            msgs.append('User Registered')
    else:
        code = 500
        val_errs = regform.non_field_errors().as_data()
        for err in val_errs[0]:
            msgs.append(err)
            
    data = {
        'code' : code,
        'msgs' : msgs,
    }
    return JsonResponse(data)    


def reg_con(request, uid_b64, token):
    old_link=f'/acc/register/confirm/{uid_b64}/{token}/'
    uid_b64=uid_b64+'=='
    uid_b64=uid_b64.encode('ascii')
    uid_bytes=base64.b64decode(uid_b64)
    uid=uid_bytes.decode('ascii')
    uid=int(uid)
    token=token
    
    try:
        user=User.objects.get(user_id=uid,token=token)        
    except:
        messages.error(request, "Invalid User Token")
        return redirect('/acc')
    
    user.verified = 1
    user.save(update_fields=['verified'])
    token=get_random_string(length=8)
    user.token = token
    user.save(update_fields=['token'])
    messages.success(request, "Account Verified")
    return redirect('/acc')
    
    
def log(request):
    code = 0
    msgs = []
    logform = LogForm(request.POST)
    
    if logform.is_valid():
        uname = logform.cleaned_data['uname']
        user=User.objects.filter(uname=uname).values()
        user = user[0]
        
        request.session['user_id'] = user['user_id']
        request.session['email'] = user['email']
        request.session['uname'] = uname
        request.session['utype'] = user['utype']
        request.session['login'] = True
        
        code = 200
        msgs.append(user['utype'])
        
    else:
        code = 500
        val_errs = logform.non_field_errors().as_data()
        for err in val_errs[0]:
            msgs.append(err)
            
    data = {
        'code' : code,
        'msgs' : msgs,
    }
    return JsonResponse(data)
    
    
def res(request):
    if request.POST:
        try:
            email = request.POST['email']
            user=User.objects.get(email=email)
            uid=str(user.user_id)
            uid_bytes=uid.encode('ascii')
            uid_b64=base64.b64encode(uid_bytes)
            uid_b64=uid_b64.decode("ascii")
            uid_b64=uid_b64.replace('=', '')
            token=user.token
            
            msg = ''' 
                To initiate the password reset process for your {email} Gadly App Account,
                click the link below:

                {url}/acc/reset/confirm/{uid_b64}/{token}/

                If clicking the link above doesn't work, please copy and paste the URL in a new browser
                window instead.
            '''.format(email=user.email,url=url,uid_b64=uid_b64,token=token)
            # print(msg)
            
            send_mail(
                "Gadly Password Reset",
                msg,
                "gadly@gmail.com",
                [email],
                fail_silently=False,
            )
            messages.success(request, "A email to reset password was successfully sent")
            return redirect('/acc')
        except:
            messages.error(request, "Something went wrong. Please check if the email you provided was registered.")
            return redirect('/acc/reset/')
    else:
	    return render(request, "acc/reset.html")


def res_con(request, uid_b64, token):
    old_link=f'/acc/reset/confirm/{uid_b64}/{token}/'
    uid_b64=uid_b64+'=='
    uid_b64=uid_b64.encode('ascii')
    uid_bytes=base64.b64decode(uid_b64)
    uid=uid_bytes.decode('ascii')
    uid=int(uid)
    token=token
    
    try:
        user=User.objects.get(user_id=uid,token=token)        
    except:
        messages.error(request, "Invalid User Token")
        return redirect('/acc')
        
    if request.POST:
        pswd = request.POST['pswd']
        con_pswd = request.POST['con_pswd']
        
        if pswd == con_pswd:
            pswd = make_password(pswd)
            user.pswd = pswd
            user.save(update_fields=['pswd'])
            token=get_random_string(length=8)
            user.token = token
            user.save(update_fields=['token'])
            messages.success(request, "Password Changed")
            return redirect('/acc')
        else:
            messages.error(request, "Passwords Do Not Match")
            return redirect(old_link)
    else:
        return render(request,'acc/reset_pswd.html')