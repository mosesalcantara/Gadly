from django import forms

class RegForm(forms.Form):
    name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Fullname','class':'form-control','style':'width:525px'}))
    phone = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Phone Number','class':'form-control','style':'width:250px'}))
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={'placeholder':'Email','class':'form-control','style':'width:250px'}))
    uname = forms.CharField(label='',min_length=8,widget=forms.TextInput(attrs={'placeholder':'Username','class':'form-control','style':'width:525px'}))
    pswd = forms.CharField(label='',min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control','style':'width:250px'}))
    con_pswd = forms.CharField(label='',min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','class':'form-control','style':'width:250px'}))
    utypes = (('user','User'),('admin','Admin'))
    utype = forms.ChoiceField(label='',choices=utypes,widget=forms.Select(attrs={'class':'form__input','style':'width:525px; height:55px; font-size:15px;'}))
    
    def clean(self):
        cleaned_data = super().clean()
        pswd = cleaned_data.get('pswd')
        con_pswd = cleaned_data.get('con_pswd')
        uname = cleaned_data.get('uname')
        
        if pswd != con_pswd:
            raise forms.ValidationError('Passwords do not match')
    
class LogForm(forms.Form):
    uname = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Username','class':'form-control'}))
    pswd = forms.CharField(label='',min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control'}))