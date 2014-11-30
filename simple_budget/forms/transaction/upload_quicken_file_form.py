from django import forms

class UploadQuickenFileForm(forms.Form):
    file = forms.FileField()

    referer = forms.CharField(widget=forms.HiddenInput(),
                              required=False)