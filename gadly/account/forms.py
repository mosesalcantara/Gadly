from django import forms

class RegForm(forms.Form):
    name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Fullname','class':'form__input'}))
    phone = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Phone Number','class':'form__input'}))
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={'placeholder':'Email','class':'form__input'}))
    uname = forms.CharField(label='',min_length=8,widget=forms.TextInput(attrs={'placeholder':'Username','class':'form__input'}))
    pswd = forms.CharField(label='',min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form__input'}))
    con_pswd = forms.CharField(label='',min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','class':'form__input'}))
    utypes = (('user','User'),('admin','Admin'))
    utype = forms.ChoiceField(label='',choices=utypes,widget=forms.Select(attrs={'class':'form__input'}))
    
    def clean(self):
        cleaned_data = super().clean()
        pswd = cleaned_data.get('pswd')
        con_pswd = cleaned_data.get('con_pswd')
        uname = cleaned_data.get('uname')
        
        if pswd != con_pswd:
            raise forms.ValidationError('Passwords do not match')
    
class LogForm(forms.Form):
    uname = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Username','class':'form__input'}))
    pswd = forms.CharField(label='',min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form__input'}))