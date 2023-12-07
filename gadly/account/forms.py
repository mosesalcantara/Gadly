from django import forms
from backend.models import User
from django.contrib.auth.hashers import check_password

class RegForm(forms.ModelForm):
    con_pswd = forms.CharField(label='',min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','class':'form-control','style':'width:250px'}))
    class Meta:
        model = User
        exclude = ['user_id','verified','token']
        widgets = {
            'name' : forms.TextInput(attrs={'placeholder':'Fullname','class':'form-control','style':'width:525px'}),
            'phone' : forms.TextInput(attrs={'placeholder':'Phone Number','class':'form-control','style':'width:250px'}),
            'email' : forms.EmailInput(attrs={'placeholder':'Email','class':'form-control','style':'width:250px'}),
            'uname' : forms.TextInput(attrs={'placeholder':'Username','class':'form-control','style':'width:525px'}),
            'pswd' : forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control','style':'width:250px'}),
            'utype' : forms.Select(attrs={'class':'form__input','style':'width:525px; height:55px; font-size:15px;'})
        }
        
    def clean(self):
        cleaned_data = super().clean()
        pswd = cleaned_data.get('pswd')
        con_pswd = cleaned_data.get('con_pswd')
        email = cleaned_data.get('email')
        uname = cleaned_data.get('uname')
        
        if pswd != con_pswd:
            raise forms.ValidationError('Passwords do not match')
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('Email is already taken')
        if User.objects.filter(uname=uname).count() > 0:
            raise forms.ValidationError('Username is already taken')
    
class LogForm(forms.Form):
    uname = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Username','class':'form-control'}))
    pswd = forms.CharField(label='',min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control'}))
    
    def clean(self):
        cleaned_data = super().clean()
        uname = cleaned_data.get('uname')
        pswd = cleaned_data.get('pswd')
        
        user = User.objects.filter(uname=uname).values()
        if len(user) == 1:
            if user[0]['verified'] == 1:
                if check_password(pswd, user[0]['pswd']) == False:
                    raise forms.ValidationError('Invalid username or password')
            else:
                raise forms.ValidationError('User is not verified')
        else:
            raise forms.ValidationError('Invalid username or password')