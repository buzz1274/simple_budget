from django import forms

class UploadQuickenFile(forms.Form):
    file = forms.FileField()

    referer = forms.CharField(widget=forms.HiddenInput(),
                              required=False)