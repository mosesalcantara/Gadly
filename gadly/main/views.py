import json
import requests
import calendar
import base64
import docx

# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('omw-1.4')

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.db.models import Count
from django.core.mail import send_mail
from statistics import mode
from datetime import datetime
from difflib import SequenceMatcher

from .main import Main
from .models import User,Paraphrase,ParaDetail,Replacement,RepDetail
from .forms import SignUpForm,SignInForm,AddUserForm


url = 'http://127.0.0.1:8000'

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def sign(request):
    if request.method == "POST":
        if 'log' in request.POST:
            sign_in(request)
        elif 'reg' in request.POST:
            sign_up(request)
    else:
        logform = SignInForm()
        regform = SignUpForm()
    return render(request,"main/sign.html",{"logform":logform,'regform':regform})


def test(request):      
        txt='mankind along with firemen, chairman, and mailmen'
        sen=''
        words_dict={}
        words=[]
        pref={}
        
        obj = Main()
        words_dict, words_data, words, sen = obj.main(txt, pref)
        print(f'Words Dictionary: {words_dict}')
        # print(f'Data: {words_data}')
        # print(f'Words: {words}')
        # print(f'Sentence: {sen}')
        return HttpResponse("Hi")
    
    
def des(request):
    return render(request,'main/user/des.html')
    
def sign_up(request):
    regform = SignUpForm(request.POST)
    if regform.is_valid():
        name = regform.cleaned_data['name']
        phone = regform.cleaned_data['phone']
        email = regform.cleaned_data['email']
        uname = regform.cleaned_data['uname']
        pswd = regform.cleaned_data['pswd']
        utype = regform.cleaned_data['utype']
        token = get_random_string(length=8)
        try:
            user = User.objects.create(name=name,phone=phone,email=email,uname=uname,pswd=pswd,utype=utype,token=token)
            user.save()
            uid=str(user.pk)
            uid_bytes=uid.encode('ascii')
            uid_b64=base64.b64encode(uid_bytes)
            uid_b64=uid_b64.decode("ascii")
            uid_b64=uid_b64.replace('=', '')
            msg = ''' 
                To initiate the account verification for your {email} Gadly App Account,
                click the link below:

                {url}/main/sign_up/confirm/{uid_b64}/{token}/

                If clicking the link above doesn't work, please copy and paste the URL in a new browser
                window instead.
            '''.format(email=user.email,url=url,uid_b64=uid_b64,token=token)
            # print(msg)
            send_mail(
                "Gadly Account Verification",
                msg,
                "gadly@gmail.com",
                [email],
                fail_silently=False,
            )
        except:
            messages.error(request,'Registration Error')
            return redirect('/main')
        
        messages.success(request,'User Registered. Check your email to verify your account.')
        return redirect('/main')
    else:
        val_errs = regform.non_field_errors().as_data()
        for err in val_errs[0]:
            messages.error(request,err)
        return redirect('/main')


def sign_up_confirm(request, uid_b64, token):
    old_link=f'/main/sign_up/confirm/{uid_b64}/{token}/'
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
        return redirect('/main/')
    user.verified = 1
    user.save(update_fields=['verified'])
    token=get_random_string(length=8)
    user.token = token
    user.save(update_fields=['token'])
    messages.success(request, "Account Verified")
    return redirect('/main')
    
    
def sign_in(request):
    logform = SignInForm(request.POST)
    if logform.is_valid():
        uname=logform.cleaned_data['uname']
        pswd=logform.cleaned_data['pswd']
        
        try:
            user=User.objects.filter(uname=uname,pswd=pswd).values()
        except:
            messages.error(request,'Database Error')
            return redirect('/main/')
        
        if len(user) > 0 and user[0]['verified'] == 1:
            user = user[0]
            request.session['user_id'] = user['user_id']
            request.session['email'] = user['email']
            request.session['uname'] = uname
            request.session['utype'] = user['utype']
            request.session['login'] = True
            return redirect('/main/home')
        else:
            messages.error(request,'Wrong Credentials')
            return redirect('/main/')
        
    else:
        return redirect('/main/')


def home(request):
    if ('login' in request.session):
        if (request.session['utype'] == 'admin'):
            users = User.objects.count()
            paras = Paraphrase.objects.count()
            reps = Replacement.objects.count()
            count={'users':users,'paras':paras,'reps':reps}
            count_chart={'x':['Users','Paraphrases','Replacements'],'y':[users,paras,reps]}
            det_chart={'x':[],'y':[]}
            rep_chart={'x':[],'y':[]}
            cdet_chart={'x':[],'y':[]}
            crepl_chart={'x':[],'y':[]}
        
            det_res = ParaDetail.objects.values('det').annotate(count=Count('det'))[:5]
            det_chart['x'] = [row['det'] for row in det_res]
            det_chart['y'] = [row['count'] for row in det_res]
            rep_res = RepDetail.objects.values('rep').annotate(count=Count('rep'))[:5]
            rep_chart['x'] = [row['rep'] for row in rep_res]
            rep_chart['y'] = [row['count'] for row in rep_res]
            cdet_res = Paraphrase.objects.raw('SELECT 1 AS para_id, Month(para_at) AS month, Count(para_id) AS count FROM `main_paraphrase` GROUP BY Month(para_at);')
            cdet_chart['x'] = [calendar.month_name[row.month] for row in cdet_res]
            cdet_chart['y'] = [row.count for row in cdet_res]
            crep_res = Replacement.objects.raw('SELECT 1 AS repl_id, Month(repl_at) AS month, Count(repl_id) AS count FROM `main_replacement` GROUP BY Month(repl_at);')
            crepl_chart['x'] = [calendar.month_name[row.month] for row in crep_res]
            crepl_chart['y'] = [row.count for row in crep_res]
            
            context = {
                'count': count,
                'count_chart': count_chart,
                'det_chart': det_chart,
                'rep_chart': rep_chart,
                'cdet_chart': cdet_chart,
                'crepl_chart': crepl_chart,
            }
            return render(request,"main/admin/dash.html",context)
        elif (request.session['utype'] == 'user'):
            return render(request,"main/user/home.html")
    else:
        return redirect('/main')
            

def admin_para(request):
    if ('login' in request.session):
        if (request.session['utype'] == 'admin'):
            return render(request,"main/admin/main.html")
    else:
        return redirect('/main')


def structural_changes(request):
    if ('login' in request.session):        
        if is_ajax(request=request):
            txt = request.POST['txt']
            output = request.POST['output']
            matcher = SequenceMatcher(None, txt, output)
            
            similarity_ratio = matcher.ratio()
            difference = int((1 - similarity_ratio) * 100)
            json_data = {
                'difference':difference,
            }
            return JsonResponse(json_data)
    else:
        return redirect('/main')
    

def paraphrase_text(request):
    if ('login' in request.session):        
        txt=''
        sen=''
        words_dict={}
        rep_dict={}
        words=[]
        pref={}
        
        if is_ajax(request=request):
            txt = request.POST['txt']
            # parser = GingerIt()
            # txt = parser.parse(txt)['result']
            # txt = para(txt)
            pref,data_set = learn_user(request.session['user_id'])
            obj = Main()
            words_dict, words_data, words, sen = obj.main(txt, pref)
            # print(f'Words Dictionary: {words_dict}')
            # print(f'Data: {words_data}')
            # print(f'Words: {words}')
            # print(f'Sentence: {sen}')
                
            json_data={
                'words_dict' : words_dict,
                'words_data' : words_data,
                'words' : words,
            }           
            
            user = User.objects.get(user_id=request.session['user_id'])
            para = Paraphrase.objects.create(user=user,txt=txt)
            para.save()
            para = Paraphrase.objects.get(para_id=para.pk)
            for ind,ent in words_dict.items():
                for det,rep in ent.items():
                    paradet=ParaDetail.objects.create(det=det.lower(),rep=rep[0].lower(),para=para)
                    paradet.save()
             
            return JsonResponse(json_data)
    else:
        return redirect('/main')
    
    
def learn_user(user_id):
    data_set={}
    pref_dict={}

    repdets = RepDetail.objects.select_related('repl').filter(repl__user=user_id)
    if len(repdets) > 0:
        uname=repdets[0].repl.user.uname
        data_set[uname]={}
        for repdet in repdets:
            if repdet.det in data_set[uname]:
                data_set[uname][repdet.det].append(repdet.rep)
            else:
                data_set[uname][repdet.det]=[repdet.rep]
                
        for user,data in data_set.items():
            for det,reps in data.items():
                pref_dict[det] = mode(reps)

    # print(repdets)
    # print(data_set)
    # print(pref_dict)
    return pref_dict,data_set


def para(txt):
    url = "https://rewriter-paraphraser-text-changer-multi-language.p.rapidapi.com/rewrite"

    payload = {
        "language": "en",
        "strength": 3,
        "text": txt
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "430b49110amsh12ca3cabdfba9bbp13b194jsnce0c8d092cf6",
        "X-RapidAPI-Host": "rewriter-paraphraser-text-changer-multi-language.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    rephrased = response.json()['rewrite']
    return rephrased


def upl_file(request):
    file = request.FILES['file']
    file = docx.Document(file)
    txt = " ".join([paragraph.text for paragraph in file.paragraphs])
    data={
        'txt':txt
    }
    return JsonResponse(data)
    
def plag(request):
    if ('login' in request.session):
        if (request.session['utype'] == 'admin'):
            return render(request,'main/admin/plag.html')
        elif (request.session['utype'] == 'user'):
            return render(request,'main/user/plag.html')
    else:
        return redirect('/main')


def profile(request):
    if ('login' in request.session):
        acc = User.objects.filter(user_id=request.session['user_id']).values().first()
        context = {
            'acc':acc
        }
        return render(request,'main/user/profile.html',context)
    else:
        return redirect('/main')


def history(request):
    if ('login' in request.session):
        top_words = {}
        top_det = ParaDetail.objects.select_related('para').values('det').filter(para__user=request.session['user_id']).annotate(count=Count('det')).order_by('-count').first()
        top_rep = ParaDetail.objects.select_related('para').values('rep').filter(para__user=request.session['user_id']).annotate(count=Count('rep')).order_by('-count').first()
        top_words['dets'] = top_det['det']
        top_words['reps'] = top_rep['rep']
        
        paras = Paraphrase.objects.values('para_id', 'para_at', 'txt').filter(user=request.session['user_id']).order_by('-para_at')
        # print(paras)
        for para in paras:
            para['rep_dict'] = ParaDetail.objects.values('det','rep').filter(para=para['para_id'])
            
        # print(paras)
        context = {
            'paras' : paras,
            'top_words' : top_words,
        }
        return render(request,'main/user/history.html',context)
    else:
        return redirect('/main')
    
    
def hist(request):
    if ('login' in request.session):
        if is_ajax(request=request):
            para_dets = []
            para_id = request.POST['para_id']
            para_dets = ParaDetail.objects.select_related('para').filter(para=para_id)
            para_dets = list(para_dets.values())
            # print(para_dets)
            json_data = {
                'para_dets' : para_dets,
            }
            return JsonResponse(json_data)
    else:
        return redirect('/main')  


def replacements(request):
    if ('login' in request.session):
        top_words = {}
        top_det = RepDetail.objects.select_related('repl').values('det').filter(repl__user=request.session['user_id']).annotate(count=Count('det')).order_by('-count').first()
        top_rep = RepDetail.objects.select_related('repl').values('rep').filter(repl__user=request.session['user_id']).annotate(count=Count('rep')).order_by('-count').first()
        top_words['reps'] = top_rep['rep']
        top_words['dets'] = top_det['det']
        
        reps = Replacement.objects.values('repl_id', 'repl_at').filter(user=request.session['user_id']).order_by('-repl_at')
        for rep in reps:
            rep['rep_dict'] = RepDetail.objects.values('det','rep').filter(repl=rep['repl_id'])
      
        context = {
            'reps':reps,
            'top_words':top_words,
        }
        return render(request,'main/user/replacements.html',context)
    else:
        return redirect('/main')


def repla(request):
    if ('login' in request.session):
        if is_ajax(request=request):
            repl_dets = []
            repl_id = request.POST['repl_id']
            repl_dets = RepDetail.objects.select_related('repl').filter(repl=repl_id)
            repl_dets = list(repl_dets.values())
            # print(para_dets)
            json_data = {
                'repl_dets' : repl_dets,
            }
            return JsonResponse(json_data)
    else:
        return redirect('/main')  


def all_users(request):
    if ('login' in request.session):
        if request.method == 'POST':
            pass
        else:
            users = User.objects.all()  
            add_user_form = AddUserForm()
            context = {
                'users':users,
                'add_user_form':add_user_form,
            }
            return render(request,"main/admin/users.html",context)
    else:
        return redirect('/main')
    

def add_user(request):
    if 'login' in request.session:
        if request.method == 'POST':
            add_user_form = AddUserForm(request.POST)
            if add_user_form.is_valid():
                name = add_user_form.cleaned_data['name']
                phone = add_user_form.cleaned_data['phone']
                email = add_user_form.cleaned_data['email']
                uname = add_user_form.cleaned_data['uname']
                pswd = add_user_form.cleaned_data['pswd']
                utype = add_user_form.cleaned_data['utype']
                verif = 1
                token = get_random_string(length=8)
                
                try:
                    user = User.objects.create(name=name,phone=phone,email=email,uname=uname,pswd=pswd,utype=utype,verified=verif,token=token)
                    user.save()
                except:
                    messages.error(request,'Insert Error')
                    return redirect('/main/admin/users/')
                
                messages.success(request,'User Added')
                return redirect('/main/admin/users/')
            else:
                messages.error(request,'Insert Error')
                return redirect('/main/admin/users/')
        else:
            return redirect('/main/admin/users/')
    else:
        return redirect('/main')
    
    
def get_user(request):
    if 'login' in request.session:
        if request.method == 'POST':
            user_id = request.POST['upd_id']
            user = list(User.objects.filter(user_id=user_id).values())[0]
            data={
                'user':user
            }
            return JsonResponse(data)
        else:
            return redirect('/main/admin/users/')
    else:
        return redirect('/main')
       
    
def upd_user(request):
    if 'login' in request.session:
        if request.method == 'POST':
            user_id = request.POST['upd_id']
            name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']
            uname = request.POST['uname']
            pswd = request.POST['pswd']
            con_pswd = request.POST['con_pswd']
            utype = request.POST['utype']
            verif = int(request.POST['verif'])
            token = request.POST['token']
            
            if pswd == con_pswd:
                user = User.objects.get(user_id=user_id)
                user.name = name
                user.phone = phone
                user.email = email
                user.uname = uname
                user.pswd = pswd
                user.utype = utype
                user.verified = verif
                user.token = token 
                user.save()

                messages.add_message(request, messages.INFO, 'User Updated', extra_tags='suc')                
                # messages.success(request,'User Updated')
                return redirect('/main/admin/users/')
            else:
                messages.add_message(request, messages.INFO, 'Update Error', extra_tags='err')       
                # messages.error(request,'Update Error')
                return redirect('/main/admin/users/')
        else:
            return redirect('/main/admin/users/')
    else:
        return redirect('/main')
    

def del_user(request):
    if 'login' in request.session:
        if request.method == 'POST':
            user_id = request.POST['del_id']
            try:
                user = User.objects.get(user_id=user_id)
                user.delete()
            except:
                messages.error(request,'Delete Error')
                return redirect('/main/admin/users/')
            messages.success(request,'User Deleted')
            return redirect('/main/admin/users/')
        else:
            return redirect('/main/admin/users/')
    else:
        return redirect('/main')
    
    
def all_paraphrases(request):
    if ('login' in request.session):
        top_words={}
        count=0
        users=User.objects.all()
        # print(users)
        for user in users:
            top_words[count] = {}
            top_words[count]['user_id']=user.user_id
            top_words[count]['uname']=user.uname
            top_det = ParaDetail.objects.select_related('para').values('det').filter(para__user=user.user_id).annotate(count=Count('det')).order_by('-count').first()
            top_rep = ParaDetail.objects.select_related('para').values('rep').filter(para__user=user.user_id).annotate(count=Count('rep')).order_by('-count').first()
            if top_det == None or top_rep == None:
                top_words[count]['dets']=''
                top_words[count]['reps']=''
            else:
                top_words[count]['dets']=top_det['det']
                top_words[count]['reps']=top_rep['rep']
            count += 1
        context={
            'top_words':top_words
        }
        # print(top_words)
        return render(request,"main/admin/paraphrases.html",context)
    else:
        return redirect('/main')
    
    
def paraphrase_detail(request, user_id):
    if ('login' in request.session):
        paras = Paraphrase.objects.values('para_id', 'para_at', 'txt').filter(user=user_id).order_by('-para_at')
        # print(paras)
        for para in paras:
            para['rep_dict'] = ParaDetail.objects.values('det','rep').filter(para=para['para_id'])
            
        # print(paras)
        context = {
            'paras' : paras,
        } 
        return render(request,"main/admin/paradetail.html",context)
    else:
        return redirect('/main') 
    
    
def paraphrase_detailed(request):
    if ('login' in request.session):
        if is_ajax(request=request):
            para_dets = []
            para_id = request.POST['para_id']
            para_dets = ParaDetail.objects.select_related('para').filter(para=para_id)
            para_dets = list(para_dets.values())
            # print(para_dets)
            json_data = {
                'para_dets' : para_dets,
            }
            return JsonResponse(json_data)
    else:
        return redirect('/main')  

    
def all_replacements(request):
    if ('login' in request.session):
        top_words={}
        count=0
        users=User.objects.all()
        # print(users)
        for user in users:
            top_words[count] = {}
            top_words[count]['user_id']=user.user_id
            top_words[count]['uname']=user.uname
            top_det = RepDetail.objects.select_related('repl').values('det').filter(repl__user=user.user_id).annotate(count=Count('det')).order_by('-count').first()
            top_rep = RepDetail.objects.select_related('repl').values('rep').filter(repl__user=user.user_id).annotate(count=Count('rep')).order_by('-count').first()
            if top_det == None or top_rep == None:
                top_words[count]['dets']=''
                top_words[count]['reps']=''
            else:
                top_words[count]['dets']=top_det['det']
                top_words[count]['reps']=top_rep['rep']
            count += 1
        context={
            'top_words':top_words
        }
        # print(top_words)
        return render(request,"main/admin/replacements.html",context)
    else:
        return redirect('/main')
    
    
def replacement_detail(request, user_id):
    if ('login' in request.session):
        reps = Replacement.objects.values('repl_id', 'repl_at').filter(user=user_id).order_by('-repl_at')
        # print(paras)
        for rep in reps:
            rep['rep_dict'] = RepDetail.objects.values('det','rep').filter(repl=rep['repl_id'])
            
        # print(reps)
        context = {
            'reps' : reps,
        } 
        return render(request,"main/admin/repdetail.html",context)
    else:
        return redirect('/main')   
    
    
def replacement_detailed(request):
    if ('login' in request.session):
        if is_ajax(request=request):
            repl_dets = []
            repl_id = request.POST['repl_id']
            repl_dets = RepDetail.objects.select_related('repl').filter(repl=repl_id)
            repl_dets = list(repl_dets.values())
            # print(para_dets)
            json_data = {
                'repl_dets' : repl_dets,
            }
            return JsonResponse(json_data)
    else:
        return redirect('/main')  


def logout(request):
    replacements = {}
    if is_ajax(request=request):
        reps = json.loads(request.POST['reps'])
        user = User.objects.get(user_id=request.session['user_id'])
        repl = Replacement.objects.create(user=user)
        repl.save()
        repl = Replacement.objects.get(repl_id=repl.pk)
        if reps != {}:
            for det,rep in reps.items():
                repdet=RepDetail.objects.create(det=det.lower(),rep=rep.lower(),repl=repl)
                repdet.save()

    try:
        del request.session['user_id']
        del request.session['email']
        del request.session['uname']
        del request.session['utype']
        del request.session['login']
    except:
        pass
    if (is_ajax(request=request)):
        return JsonResponse(reps)
    else:
        return redirect("/main")


def reset(request):
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

                {url}/main/reset/confirm/{uid_b64}/{token}/

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
            messages.success(request, "A email to reset password is successfully sent")
            return redirect('/main')
        except:
            messages.error(request, "Something went wrong, Please check the email you provided is registered or not")
            return redirect('/main/reset/')
    else:
	    return render(request, "main/reset.html")


def reset_confirm(request, uid_b64, token):
    old_link=f'/main/reset/confirm/{uid_b64}/{token}/'
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
        return redirect('/main/')
        
    if request.POST:
        pswd = request.POST['pswd']
        con_pswd = request.POST['con_pswd']
        if pswd == con_pswd:
            user.pswd = pswd
            user.save(update_fields=['pswd'])
            token=get_random_string(length=8)
            user.token = token
            user.save(update_fields=['token'])
            messages.success(request, "Password Changed")
            return redirect('/main')
        else:
            messages.error(request, "Passwords Do Not Match")
            return redirect(old_link)
    else:
        return render(request,'main/reset_pswd.html')


@csrf_exempt
def api_signin(request):
    if request.method == 'POST':
        uname=request.POST['uname']
        pswd=request.POST['pswd']
        
        # print(email,pasw)
        try:
            user=User.objects.filter(uname=uname,pswd=pswd).values()
        except:
            return JsonResponse({"login":False})
        
        if len(user) > 0 and user[0]['verified'] == 1:
            return JsonResponse({"login":True,'uname':uname})
        else:
            return JsonResponse({"login":False})
        

@csrf_exempt
def api_signup(request):
    if request.method == 'POST':
        name=request.POST['name']
        phone=request.POST['phone']
        email=request.POST['email']
        uname=request.POST['uname']
        pswd=request.POST['pswd']
        con_pswd=request.POST['con_pswd']
        utype=request.POST['utype']
        token = get_random_string(length=8)
        
        if pswd != con_pswd:
            return JsonResponse({"registered":False}) 
        
        try:
            user = User.objects.create(name=name,phone=phone,email=email,uname=uname,pswd=pswd,utype=utype,token=token)
            user.save()
            uid=str(user.pk)
            uid_bytes=uid.encode('ascii')
            uid_b64=base64.b64encode(uid_bytes)
            uid_b64=uid_b64.decode("ascii")
            uid_b64=uid_b64.replace('=', '')
            msg = ''' 
                To initiate the account verification for your {email} Gadly App Account,
                click the link below:

                {url}/main/sign_up/confirm/{uid_b64}/{token}/

                If clicking the link above doesn't work, please copy and paste the URL in a new browser
                window instead.
            '''.format(email=user.email,url=url,uid_b64=uid_b64,token=token)
            # print(msg)
            send_mail(
                "Gadly Account Verification",
                msg,
                "gadly@gmail.com",
                [email],
                fail_silently=False,
            )
        except:
            return JsonResponse({"registered":False})
        
        return JsonResponse({"registered":True})


@csrf_exempt
def api_para(request):
    txt=''
    sen=''
    words_dict={}
    rep_dict={}
    words=[]
    pref={}
    
    txt = request.POST['txt']
    # parser = GingerIt()
    # txt = parser.parse(txt)['result']
    # txt = para(txt)
    # pref = learn_user(request.session['email'])
    user=User.objects.filter(uname=request.POST['uname']).values().first()
    pref,data_set = learn_user(user['user_id'])
    obj = Main()
    words_dict, words_data, words, sen = obj.main(txt, pref)
    print(words_dict,words,sen)
    
    for ind,ent in words_dict.items():
        for det,rep in ent.items():
            rep_dict[det.lower()] = rep[0].lower()    
    # db.child("users").child(request.session['user_id']).child("paraphrases").push(rep_dict)
    json_data={
        'words_dict' : words_dict,
        'words_data' : words_data,
        'words' : words,
    }            
    return JsonResponse(json_data)

def checkPlag(request):
    if is_ajax(request=request):
        try:
            txt = request.POST['txt']
            url = 'https://www.prepostseo.com/apis/checkPlag'
            key = '40aa8e0aa049ed3e2e2847ab10fbf4b4'
            data = {
                'key' : key,
                'data' : txt
            }
            response = requests.post(url, data=data)
            res = response.json()
            json_data={
                'percent' : res['plagPercent']
            }
            # json_data={
            #     'percent' : 0
            # }
            return JsonResponse(json_data)
        except:
            json_data={
                'percent' : 0
            }
            return JsonResponse(json_data)
        



