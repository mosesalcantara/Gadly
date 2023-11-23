import docx
import requests

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from difflib import SequenceMatcher
from statistics import mode

from .para_txt import Para_txt
from .models import Dataset,User,Paraphrase,ParaDetail,Replacement,RepDetail


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def train(request):
    return HttpResponse('Training ')


def upl_file(request):
    file = request.FILES['file']
    file = docx.Document(file)
    txt = " ".join([paragraph.text for paragraph in file.paragraphs])
    data={
        'txt':txt
    }
    return JsonResponse(data)


def para_txt(request):
    if ('login' in request.session):        
        txt=''
        sen=''
        words_list={}
        rep_dict={}
        words=[]
        pref={}
        
        if is_ajax(request=request):
            txt = request.POST['txt']
            # parser = GingerIt()
            # txt = parser.parse(txt)['result']
            # txt = para(txt)
            pref,dataset = learn_user(request.session['user_id'])
            obj = Para_txt()
            words_list, words_data, words, sen = obj.para_txt(txt, pref)
            # print(f'Words List: {words_list}')
            # print(f'Data: {words_data}')
            # print(f'Words: {words}')
            # print(f'Sentence: {sen}')
                
            json_data={
                'words_list' : words_list,
                'words_data' : words_data,
                'words' : words,
            }           
            
            user = User.objects.get(user_id=request.session['user_id'])
            para = Paraphrase.objects.create(user=user,txt=txt)
            para.save()
            para = Paraphrase.objects.get(para_id=para.pk)
            
            for ent in words_list:
                for det,rep in ent.items():
                    paradet=ParaDetail.objects.create(det=det.lower(),rep=rep[0].lower(),para=para)
                    paradet.save()
             
            return JsonResponse(json_data)
    else:
        return redirect('/acc')
    
   
# def para(txt):
#     url = "https://rewriter-paraphraser-text-changer-multi-language.p.rapidapi.com/rewrite"

#     payload = {
#         "language": "en",
#         "strength": 3,
#         "text": txt
#     }
#     headers = {
#         "content-type": "application/json",
#         "X-RapidAPI-Key": "430b49110amsh12ca3cabdfba9bbp13b194jsnce0c8d092cf6",
#         "X-RapidAPI-Host": "rewriter-paraphraser-text-changer-multi-language.p.rapidapi.com"
#     }

#     response = requests.request("POST", url, json=payload, headers=headers)
#     rephrased = response.json()['rewrite']
#     return rephrased 


def paraphrase(request):
    if ('login' in request.session):        
        if is_ajax(request=request):
            sen = ''
            txt = request.POST['txt']
            obj = Para_txt()
            sen = obj.paraphrase(txt)[1]
            
            json_data = {
                'sentence' : sen
            }
            return JsonResponse(json_data)
    else:
        return redirect('/acc')
    

def learn_user(user_id):
    dataset={}
    pref_dict={}

    repdets = RepDetail.objects.select_related('repl').filter(repl__user=user_id)
    if len(repdets) > 0:
        uname=repdets[0].repl.user.uname
        dataset[uname]={}
        for repdet in repdets:
            if repdet.det in dataset[uname]:
                dataset[uname][repdet.det].append(repdet.rep)
            else:
                dataset[uname][repdet.det]=[repdet.rep]
                
        for user,data in dataset.items():
            for det,reps in data.items():
                pref_dict[det] = mode(reps)

    # print(repdets)
    # print(data_set)
    # print(pref_dict)
    return pref_dict,dataset


def struct_changes(request):
    if ('login' in request.session):        
        if is_ajax(request=request):
            txt = request.POST['txt']
            output = request.POST['output']
            matcher = SequenceMatcher(None, txt, output)
            
            sim_ratio = matcher.ratio()
            diff = int((1 - sim_ratio) * 100)
            json_data = {
                'diff':diff,
            }
            return JsonResponse(json_data)
    else:
        return redirect('/acc')


def check_plag(request):
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