from django import forms

class AddUserForm(forms.Form):
    name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Fullname','class':'form-control mb-2'}))
    phone = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Phone Number','class':'form-control mb-2','style':'witdth:200px'}))
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={'placeholder':'Email','class':'form-control mb-2','style':'witdth:200px'}))
    uname = forms.CharField(label='',min_length=8,widget=forms.TextInput(attrs={'placeholder':'Username','class':'form-control mb-2','style':'witdth:200px'}))
    pswd = forms.CharField(label='',min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control mb-2','style':'witdth:200px'}))
    con_pswd = forms.CharField(label='',min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','class':'form-control mb-2'}))
    utypes = (('user','User'),('admin','Admin'))
    utype = forms.ChoiceField(label='',choices=utypes,widget=forms.Select(attrs={'class':'form-select','style':'height:55px; font-size:15px;'}))
    
    def clean(self):
        cleaned_data = super().clean()
        pswd = cleaned_data.get('pswd')
        con_pswd = cleaned_data.get('con_pswd')
        uname = cleaned_data.get('uname')
        
        if pswd != con_pswd:
            raise forms.ValidationError('Passwords do not match')