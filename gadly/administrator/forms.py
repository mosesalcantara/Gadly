from django import forms
from backend.models import User
        
class AddUserForm(forms.ModelForm):
    con_pswd = forms.CharField(label='',min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','class':'form-control mb-2'}))
    class Meta:
        model = User
        exclude = ['user_id','verified','token']
        widgets = {
            'name' : forms.TextInput(attrs={'placeholder':'Fullname','class':'form-control mb-2'}),
            'phone' : forms.TextInput(attrs={'placeholder':'Phone Number','class':'form-control mb-2'}),
            'email' : forms.EmailInput(attrs={'placeholder':'Email','class':'form-control mb-2'}),
            'uname' : forms.TextInput(attrs={'placeholder':'Username','class':'form-control mb-2'}),
            'pswd' : forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control mb-2'}),
            'utype' : forms.Select(attrs={'class':'form-select','style':'height:55px; font-size:15px;'})
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
        
class UpdUserForm(forms.ModelForm):
    user_id = forms.CharField(widget=forms.HiddenInput(attrs={'id':'user_id'}))
    con_pswd = forms.CharField(label='',min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','class':'form-control mb-2','id':'con_pswd'}))
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'name' : forms.TextInput(attrs={'placeholder':'Fullname','class':'form-control mb-2','id':'name'}),
            'phone' : forms.TextInput(attrs={'placeholder':'Phone Number','class':'form-control mb-2','id':'phone'}),
            'email' : forms.EmailInput(attrs={'placeholder':'Email','class':'form-control mb-2','id':'email'}),
            'uname' : forms.TextInput(attrs={'placeholder':'Username','class':'form-control mb-2','id':'uname'}),
            'pswd' : forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control mb-2','id':'pswd'}),
            'utype' : forms.Select(attrs={'class':'form-select','style':'height:55px; font-size:15px;','id':'utype'}),
            'verified' : forms.Select(attrs={'class':'form-select','style':'height:55px; font-size:15px;','id':'verif'}),
            'token' : forms.TextInput(attrs={'placeholder':'Token','class':'form-control mb-2','id':'token'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        pswd = cleaned_data.get('pswd')
        con_pswd = cleaned_data.get('con_pswd')
        
        user_id = cleaned_data.get('user_id')
        user = User.objects.filter(user_id=user_id).values()
        user = user[0]
        
        email = cleaned_data.get('email')
        uname = cleaned_data.get('uname')
        
        if pswd != con_pswd:
            raise forms.ValidationError('Passwords do not match')
        if User.objects.filter(email=email).count() > 0 and user['email'] != email:
            raise forms.ValidationError('Email is already taken')
        if User.objects.filter(uname=uname).count() > 0 and user['uname'] != uname:
            raise forms.ValidationError('Username is already taken')