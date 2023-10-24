import base64

from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from statistics import mode

from backend.para_txt import Para_txt
from backend.models import User,Paraphrase,ParaDetail,Replacement,RepDetail

url = 'http://127.0.0.1:8000'

@csrf_exempt
def reg(request):
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

                {url}/acc/register/confirm/{uid_b64}/{token}/

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
            return JsonResponse({"registered":True})
        except:
            return JsonResponse({"registered":False})
    

@csrf_exempt
def log(request):
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
def para_txt(request):
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
    user=User.objects.filter(uname=request.POST['uname']).values().first()
    pref,dataset = learn_user(user['user_id'])
    obj = Para_txt()
    words_dict, words_data, words, sen = obj.para_txt(txt, pref)
    # print(words_dict,words,sen)
    
    for ind,ent in words_dict.items():
        for det,rep in ent.items():
            rep_dict[det.lower()] = rep[0].lower()    

    json_data={
        'words_dict' : words_dict,
        'words_data' : words_data,
        'words' : words,
    }            
    return JsonResponse(json_data)


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
