import docx
import requests
import spacy
import ai21

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from difflib import SequenceMatcher
from statistics import mode

from .para_txt import Para_txt
from .models import Dataset,User,Paraphrase,ParaDetail,Replacement,RepDetail


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def train(request):
    return HttpResponse('Training')


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
        if is_ajax(request=request):
            txt=''
            words_list = []
            words_data = []
            words = []
            sen = ''
            
            txt = request.POST['txt']
            nlp = spacy.load('en_core_web_sm')
            obj = Para_txt()
            
            pref,dataset = learn_user(request.session['user_id'])         
            doc = nlp(txt)
            
            for sent in list(doc.sents):
                sent = str(sent)
                sent_words_list, sent_words_data, sent_words, sent_sen = obj.para_txt(sent, pref)
                
                words_list.extend(sent_words_list)
                words_data.append(sent_words_data)
                words.extend(sent_words)
                sen = f'{sen} {sent_sen}'
                         
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


def paraphrase(request):
    if ('login' in request.session):        
        if is_ajax(request=request):
            sentences = []
            txt = request.POST['txt']
            
            ai21.api_key = 'SDEDDTir9F9aqsOIE3l2CpQo4LRs84t5'
            res = ai21.Paraphrase.execute(text=txt)
            res = res['suggestions']
            for sentence in res:
                sentences.append(sentence['text'])

            json_data = {
                'sentences' : sentences
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
        txt = request.POST['txt']
        url = 'https://www.prepostseo.com/apis/checkPlag'
        key = '40aa8e0aa049ed3e2e2847ab10fbf4b4'
        data = {
            'key' : key,
            'data' : txt
        }
        
        try:
            response = requests.post(url, data=data)
            response = response.json()
            
            json_data={
                'response' : response,
                'code' : 200
            }
        except:
            json_data={
                'response' : '',
                'code' : 500
            }
        return JsonResponse(json_data)


# def check_plag(request):
#     if is_ajax(request=request):
#         url = "https://plagiarism-checker-and-auto-citation-generator-multi-lingual.p.rapidapi.com/plagiarism"
#         headers = {
#             "content-type": "application/json",
#             "X-RapidAPI-Key": "430b49110amsh12ca3cabdfba9bbp13b194jsnce0c8d092cf6",
#             "X-RapidAPI-Host": "plagiarism-checker-and-auto-citation-generator-multi-lingual.p.rapidapi.com"
#         }
#         data = {
#             "text": request.POST['txt'],
#             "language": "en",
#             "includeCitations": False,
#             "scrapeSources": False
#         }
        
#         try: 
#             response = requests.post(url, headers=headers, json=data)
#             print(response.json())
#             json_data={
#                 'percent' : response.json()['percentPlagiarism']
#             }
#         except:
#             json_data={
#                 'percent' : 0
#             }
#         return JsonResponse(json_data)
        