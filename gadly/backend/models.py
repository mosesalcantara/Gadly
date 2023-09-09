from django.db import models

class Dataset(models.Model):
    word_id = models.BigAutoField(primary_key=True)
    word = models.CharField(max_length=255)
    sen = models.CharField(max_length=255)
    gen = models.CharField(max_length=255, null=True)

class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    uname = models.CharField(max_length=255)
    pswd = models.CharField(max_length=255)
    utype = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)
    token = models.CharField(max_length=255,default=None)
    
class Paraphrase(models.Model):
    para_id = models.BigAutoField(primary_key=True)
    para_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    txt = models.TextField(null=True,default=None)
    
class ParaDetail(models.Model):
    paradet_id = models.BigAutoField(primary_key=True)
    det = models.CharField(max_length=255)
    rep = models.CharField(max_length=255)
    para = models.ForeignKey(Paraphrase, on_delete=models.CASCADE)
    
class Replacement(models.Model):
    repl_id = models.BigAutoField(primary_key=True)
    repl_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class RepDetail(models.Model):
    repdet_id = models.BigAutoField(primary_key=True)
    det = models.CharField(max_length=255)
    rep = models.CharField(max_length=255)
    repl = models.ForeignKey(Replacement, on_delete=models.CASCADE)
    
