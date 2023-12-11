import json

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse, HttpResponse

from backend.models import User,Paraphrase,ParaDetail,Replacement,RepDetail


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def ind(request):
    if ('login' in request.session and request.session['login'] == True):
        return render(request,"user/index.html")
    else:
        return redirect('/acc')
    
    
def plag(request):
    if ('login' in request.session and request.session['login'] == True):
        return render(request,'user/plag.html')
    else:
        return redirect('/acc')
    
    
def prof(request):
    if ('login' in request.session and request.session['login'] == True):
        acc = User.objects.filter(user_id=request.session['user_id']).values().first()
        context = {
            'acc':acc
        }
        return render(request,'user/prof.html',context)
    else:
        return redirect('/acc')
    
    
def paras(request):
    if ('login' in request.session and request.session['login'] == True):
        top_words = {}
        top_det = ParaDetail.objects.select_related('para').values('det').filter(para__user=request.session['user_id']).annotate(count=Count('det')).order_by('-count').first()
        top_rep = ParaDetail.objects.select_related('para').values('rep').filter(para__user=request.session['user_id']).annotate(count=Count('rep')).order_by('-count').first()
        
        if top_det == None or top_rep == None:
            top_det = ''
            top_rep = ''
        else:
            top_det = top_det['det']
            top_rep = top_rep['rep']
        top_words = {'top_det':top_det, 'top_rep':top_rep}   
            
        paras = Paraphrase.objects.values('para_id', 'para_at', 'txt').filter(user=request.session['user_id']).order_by('-para_at')
        # print(paras)
        for para in paras:
            para['rep_dict'] = ParaDetail.objects.values('det','rep').filter(para=para['para_id'])
        
        context = {
            'paras' : paras,
            'top_words' : top_words,
        }
        return render(request,'user/paras.html',context)
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
        top_words = {}
        top_det = RepDetail.objects.select_related('repl').values('det').filter(repl__user=request.session['user_id']).annotate(count=Count('det')).order_by('-count').first()
        top_rep = RepDetail.objects.select_related('repl').values('rep').filter(repl__user=request.session['user_id']).annotate(count=Count('rep')).order_by('-count').first()
            
        if top_det == None or top_rep == None:
            top_det = ''
            top_rep = ''
        else:
            top_det = top_det['det']
            top_rep = top_rep['rep']
        top_words = {'top_det':top_det, 'top_rep':top_rep}   
            
        reps = Replacement.objects.values('repl_id', 'repl_at').filter(user=request.session['user_id']).order_by('-repl_at')
        for rep in reps:
            rep['rep_dict'] = RepDetail.objects.values('det','rep').filter(repl=rep['repl_id'])
    
        context = {
            'reps':reps,
            'top_words':top_words,
        }
        return render(request,'user/reps.html',context)
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