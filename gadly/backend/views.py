import docx
import requests
import ai21
import spacy

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
        words_list=[]
        rep_dict={}
        words=[]
        pref={}
        
        if is_ajax(request=request):
            nlp = spacy.load('en_core_web_sm')
            obj = Para_txt()

            txt = request.POST['txt']
            words_list = []
            words_data = []
            words= []
            sen = []
            
            pref,dataset = learn_user(request.session['user_id'])         
            doc = nlp(txt)
            
            for sent in list(doc.sents):
                sent = str(sent)
                sent_words_list, sent_words_data, sent_words, sent_sen = obj.para_txt(sent, pref)
                
                words_list.extend(sent_words_list)
                words_data.extend(sent_words_data)
                words.extend(sent_words)
                sen.extend(sent_sen)
                
            # print(f'Words List last: {words_list}')
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
            
            ai21.api_key = 'w64QGccan6g6iOZ0O63Aao06ZLKhXVRi'
            sen = ai21.Paraphrase.execute(text=txt)
            sen = sen['suggestions'][0]['text']

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
            
            # response = {
            #     'isQueriesFinished': 'false', 
            #     'sources': [
            #         {'link': 'https://www.nytimes.com/2022/04/21/t-magazine/work-life-balance-art.html', 'count': 3, 'percent': 100},
            #         {'link': 'https://www.nytimes.com/2022/04/21/t-magazine/work-life-balance-art.html', 'count': 3, 'percent': 100}, 
            #         {'link': 'https://www.nytimes.com/2022/04/21/t-magazine/work-life-balance-art.html', 'count': 3, 'percent': 100},
            #     ], 
            #     'totalQueries': 1, 
            #     'plagPercent': 100, 
            #     'paraphrasePercent': 0, 
            #     'uniquePercent': 0, 
            #     'excludeURL': None, 
            #     'details': [{
            #         'query': 'SAY “THE ARTIST’S LIFE” and already we are in thrall to the old romantic myths: the garret in winter with wind lisping through the cracks, the dissolving nights at mirrored bars nursing absinthe, the empty pockets, the feral hair, the ever-looming madhouse.', 
            #         'version': 3, 
            #         'unique': 'false',
            #         'display': {
            #             'url': 'https://www.nytimes.com/2022/04/21/t-magazine/work-life-balance-art.html', 
            #             'des': 'Apr 21, 2022 · By Ligaya Mishan April 21, 2022 SAY “THE ARTIST’S LIFE” and already we are in thrall to the old romantic myths: the garret in winter with wind lisping through the cracks, the dissolving nights at...'}, 
            #         'excludeByUrl': False, 
            #         'paraphrase': 'false'
            #     }]
            # }
            
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
#             json_data={
#                 'percent' : response.json()['percentPlagiarism']
#             }
#         except:
#             json_data={
#                 'percent' : 0
#             }
#         return JsonResponse(json_data)
        