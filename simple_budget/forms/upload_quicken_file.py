from django import forms

class UploadQuickenFile(forms.Form):
    file = forms.FileField()