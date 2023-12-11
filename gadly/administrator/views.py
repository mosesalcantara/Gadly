import calendar
import json

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from django.utils.crypto import get_random_string
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import make_password

from backend.models import User,Paraphrase,ParaDetail,Replacement,RepDetail
from .forms import AddUserForm,UpdUserForm


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def ind(request):
    if ('login' in request.session and request.session['login'] == True):
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
        
        cdet_res = Paraphrase.objects.raw('SELECT 1 AS para_id, Month(para_at) AS month, Count(para_id) AS count FROM `backend_paraphrase` GROUP BY Month(para_at);')
        cdet_chart['x'] = [calendar.month_name[row.month] for row in cdet_res]
        cdet_chart['y'] = [row.count for row in cdet_res]
        
        crep_res = Replacement.objects.raw('SELECT 1 AS repl_id, Month(repl_at) AS month, Count(repl_id) AS count FROM `backend_replacement` GROUP BY Month(repl_at);')
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
        return render(request,"admin/index.html",context)
    else:
        return redirect('/acc')
    
    
def para(request):
    if ('login' in request.session and request.session['login'] == True):
        return render(request,"admin/para.html")
    else:
        return redirect('/acc')
    
    
def plag(request):
    if ('login' in request.session and request.session['login'] == True):
        return render(request,'admin/plag.html')
    else:
        return redirect('/acc')
    

def users(request):
    if ('login' in request.session and request.session['login'] == True):
        if request.method == 'POST':
            users = User.objects.all()
            users = list(users.values())
            data = {
                'code' : 200,
                'users' : users,
            }
            return JsonResponse(data)
        else:
            add_user_form = AddUserForm()
            upd_user_form = UpdUserForm()
            context = {
                'add_user_form':add_user_form,
                'upd_user_form':upd_user_form,
            }
            return render(request,"admin/users.html",context)
    else:
        return redirect('/acc')
    
    
def add_user(request):
    if ('login' in request.session and request.session['login'] == True):
        if request.method == 'POST':
            code = 0
            msgs = []
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
                    pswd = make_password(pswd)
                    user = User.objects.create(name=name,phone=phone,email=email,uname=uname,pswd=pswd,utype=utype,verified=verif,token=token)
                    user.save()
                except:
                    code = 500
                    msgs.append('Insert Error')
                
                code = 200
                msgs.append('User Added')
            else:
                code = 500
                val_errs = add_user_form.non_field_errors().as_data()
                for err in val_errs[0]:
                    msgs.append(err)
                
            data = {
                'code' : code,
                'msgs' : msgs
            }
            return JsonResponse(data)
        else:
            return redirect('/admin/users/')
    else:
        return redirect('/acc')
    
    
def get_user(request):
    if ('login' in request.session and request.session['login'] == True):
        if request.method == 'POST':
            user_id = request.POST['user_id']
            user = list(User.objects.filter(user_id=user_id).values())[0]
            data={
                'user':user
            }
            return JsonResponse(data)
        else:
            return redirect('/admin/users/')
    else:
        return redirect('/acc')
       
    
def upd_user(request):
    if ('login' in request.session and request.session['login'] == True):
        if request.method == 'POST':
            code = 0
            msgs = []
            upd_user_form = UpdUserForm(request.POST)
            
            if upd_user_form.is_valid():
                user_id = upd_user_form.cleaned_data['user_id']
                name = upd_user_form.cleaned_data['name']
                phone = upd_user_form.cleaned_data['phone']
                email = upd_user_form.cleaned_data['email']
                uname = upd_user_form.cleaned_data['uname']
                pswd = upd_user_form.cleaned_data['pswd']
                con_pswd = upd_user_form.cleaned_data['con_pswd']
                utype = upd_user_form.cleaned_data['utype']
                verif = int(upd_user_form.cleaned_data['verified'])
                token = upd_user_form.cleaned_data['token']
                
                user = User.objects.get(user_id=user_id)
                user.name = name
                user.phone = phone
                user.email = email
                user.uname = uname
                if len(pswd) != 88:
                    user.pswd = make_password(pswd)
                user.utype = utype
                user.verified = verif
                user.token = token 
                user.save()
           
                code = 200
                msgs.append('User Updated')
                
            else:     
                code = 500
                val_errs = upd_user_form.non_field_errors().as_data()
                for err in val_errs[0]:
                    msgs.append(err)
                    
            data = {
                'code' : code,
                'msgs' : msgs,
            }
            return JsonResponse(data)
        else:
            return redirect('/admin/users/')
    else:
        return redirect('/acc')
    
    
def del_user(request):
    if ('login' in request.session and request.session['login'] == True):
        if request.method == 'POST':
            code=0
            msgs=[]
            user_id = request.POST['del_id']
            try:
                user = User.objects.get(user_id=user_id)
                user.delete()
            except:
                code=500
                msgs.append('Delete Error')
            
            code=200
            msgs.append('User Deleted')
            data = {
                'code':code,
                'msgs':msgs,
            }
            return JsonResponse(data)
        else:
            return redirect('/admin/users/')
    else:
        return redirect('/acc')
    
    
def paras(request):
    if ('login' in request.session and request.session['login'] == True):
        top_words=[]
        users=User.objects.all()
        # print(users)
        
        for user in users:
            top_det = ParaDetail.objects.select_related('para').values('det').filter(para__user=user.user_id).annotate(count=Count('det')).order_by('-count').first()
            top_rep = ParaDetail.objects.select_related('para').values('rep').filter(para__user=user.user_id).annotate(count=Count('rep')).order_by('-count').first()
            
            if top_det == None or top_rep == None:
                top_det = ''
                top_rep = ''
            else:
                top_det = top_det['det']
                top_rep = top_rep['rep']
                
            top_words.append({
                'user_id' : user.user_id,
                'uname' : user.uname,
                'top_det' : top_det,
                'top_rep' : top_rep,
            })
            
        context={
            'top_words':top_words
        }
        
        return render(request,"admin/paras.html",context)
    else:
        return redirect('/acc')
    
    
def paras_user(request, user_id):
    if ('login' in request.session and request.session['login'] == True):
        paras = Paraphrase.objects.values('para_id', 'para_at', 'txt').filter(user=user_id).order_by('-para_at')
        # print(paras)
        
        for para in paras:
            para['rep_dict'] = ParaDetail.objects.values('det','rep').filter(para=para['para_id'])
            
        # print(paras)
        context = {
            'paras' : paras,
        } 
        return render(request,"admin/paras_user.html",context)
    else:
        return redirect('/acc') 
    
    
def paras_det(request):
    if ('login' in request.session and request.session['login'] == True):
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
        return redirect('/acc')  
    
    
def reps(request):
    if ('login' in request.session and request.session['login'] == True):
        top_words=[]
        users=User.objects.all()
        # print(users)
        
        for user in users:
            top_det = RepDetail.objects.select_related('repl').values('det').filter(repl__user=user.user_id).annotate(count=Count('det')).order_by('-count').first()
            top_rep = RepDetail.objects.select_related('repl').values('rep').filter(repl__user=user.user_id).annotate(count=Count('rep')).order_by('-count').first()
            
            if top_det == None or top_rep == None:
                top_det = ''
                top_rep = ''
            else:
                top_det = top_det['det']
                top_rep = top_rep['rep']
                
            top_words.append({
                'user_id' : user.user_id,
                'uname' : user.uname,
                'top_det' : top_det,
                'top_rep' : top_rep,
            })
            
        context={
            'top_words':top_words
        }
        # print(top_words)
        return render(request,"admin/reps.html",context)
    else:
        return redirect('/acc')
    
    
def reps_user(request, user_id):
    if ('login' in request.session and request.session['login'] == True):
        reps = Replacement.objects.values('repl_id', 'repl_at').filter(user=user_id).order_by('-repl_at')
        # print(paras)
        for rep in reps:
            rep['rep_dict'] = RepDetail.objects.values('det','rep').filter(repl=rep['repl_id'])
            
        # print(reps)
        context = {
            'reps' : reps,
        } 
        return render(request,"admin/reps_user.html",context)
    else:
        return redirect('/acc')  
    
    
def reps_det(request):
    if ('login' in request.session and request.session['login'] == True):
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
        return redirect('/acc')  
    
    
def logout(request):
    replacements = {}
    if is_ajax(request=request):
        reps = json.loads(request.POST['reps'])
        if reps != {}:
            user = User.objects.get(user_id=request.session['user_id'])
            repl = Replacement.objects.create(user=user)
            repl.save()
            repl = Replacement.objects.get(repl_id=repl.pk)
        
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
        return redirect("/acc")