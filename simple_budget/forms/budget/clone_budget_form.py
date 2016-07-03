from django import forms
from simple_budget.models.budget import Budget


class CloneBudgetForm(forms.Form):


    budget_id = forms.CharField(widget=forms.HiddenInput(),
                                required=False)

    referrer = forms.CharField(widget=forms.HiddenInput(),
                              required=False)

    budget_name = \
        forms.CharField(
            max_length=200, required=True, label="Name",
            widget=forms.TextInput(attrs={'class': 'form-control',
                                          'autocomplete': 'off'}))

    budget_description = \
        forms.CharField(
            max_length=200, required=True, label="Description",
            widget=forms.TextInput(attrs={'class': 'form-control',
                                          'autocomplete': 'off'}))

    def clean_budget_name(self):
        """
        ensure only one budget is flagged as master
        :return:
        """
        if Budget.objects.filter(budget_name=self.cleaned_data['budget_name']):
            raise forms.ValidationError(
                "Budget with this name already exists.")

        return self.cleaned_data['budget_name']

