from django import forms
from simple_budget.models.budget_category import BudgetCategory


class AddEditTransactionCategory(forms.Form):

    budget_categories = \
        [('', 'Please select a budget category')] + \
        [(o.budget_category_id, str(o.budget_category))
         for o in BudgetCategory.objects.all().order_by('budget_category')]

    transaction_category_id = forms.CharField(widget=forms.HiddenInput(),
                                              required=False)

    transaction_category = forms.CharField(max_length=200, required=True,
                                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'autocomplete': 'off'}))

    budget_category = forms.ChoiceField(choices=budget_categories, required=True,
                                        widget=forms.Select(attrs={'class': 'form-control'}))