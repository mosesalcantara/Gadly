import calendar
import json

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from django.utils.crypto import get_random_string
from django.http import JsonResponse, HttpResponse

from backend.models import User,Paraphrase,ParaDetail,Replacement,RepDetail
from .forms import AddUserForm


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def ind(request):
    if ('login' in request.session):
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
    if ('login' in request.session):
        return render(request,"admin/para.html")
    else:
        return redirect('/acc')
    
    
def plag(request):
    if ('login' in request.session):
        return render(request,'admin/plag.html')
    else:
        return redirect('/acc')
    

def users(request):
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
            return render(request,"admin/users.html",context)
    else:
        return redirect('/acc')
    
    
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
                    return redirect('/admin/users/')
                
                messages.success(request,'User Added')
                return redirect('/admin/users/')
            else:
                messages.error(request,'Insert Error')
                return redirect('/admin/users/')
        else:
            return redirect('/admin/users/')
    else:
        return redirect('/acc')
    
    
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
            return redirect('/admin/users/')
    else:
        return redirect('/acc')
    
    
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
                return redirect('/admin/users/')
            else:
                messages.add_message(request, messages.INFO, 'Update Error', extra_tags='err')       
                # messages.error(request,'Update Error')
                return redirect('/admin/users/')
        else:
            return redirect('/admin/users/')
    else:
        return redirect('/acc')
    
    
def del_user(request):
    if 'login' in request.session:
        if request.method == 'POST':
            user_id = request.POST['del_id']
            
            try:
                user = User.objects.get(user_id=user_id)
                user.delete()
            except:
                messages.error(request,'Delete Error')
                return redirect('/admin/users/')
            
            messages.success(request,'User Deleted')
            return redirect('/admin/users/')
        else:
            return redirect('/admin/users/')
    else:
        return redirect('/acc')
    
    
def paras(request):
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
        
        return render(request,"admin/paras.html",context)
    else:
        return redirect('/acc')
    
    
def paras_user(request, user_id):
    if ('login' in request.session):
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
        return redirect('/acc')  
    
    
def reps(request):
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
        return render(request,"admin/reps.html",context)
    else:
        return redirect('/acc')
    
    
def reps_user(request, user_id):
    if ('login' in request.session):
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