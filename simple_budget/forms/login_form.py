from django import forms


class LoginForm(forms.Form):

    next = forms.CharField(widget=forms.HiddenInput(),
                           required=True)

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-large',
                                      'autocomplete': 'off'}))

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control form-large',
                                          'autocomplete': 'off'}))