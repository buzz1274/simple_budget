from django import forms


class DeleteBudgetForm(forms.Form):

    budget_id = forms.CharField(widget=forms.HiddenInput(),
                                required=True)

    referer = forms.CharField(widget=forms.HiddenInput(),
                              required=False)