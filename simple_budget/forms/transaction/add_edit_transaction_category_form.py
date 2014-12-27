from django import forms
from simple_budget.models.budget.budget_category import BudgetCategory
from simple_budget.models.transaction.transaction_category import \
    TransactionCategory


class AddEditTransactionCategoryForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(AddEditTransactionCategoryForm, self).__init__(*args, **kwargs)

        self.fields['transaction_category_parent_id'].choices = \
            [('', 'Please select a transaction category')] + \
            [(str(o.transaction_category_id), str(o.transaction_category))
             for o in TransactionCategory.
                objects.filter(transaction_category_parent=None).
                order_by("transaction_category")]

        self.fields['budget_category'].choices = \
            [('', 'Please select a budget category')] + \
            [(str(o.budget_category_id), str(o.budget_category))
             for o in BudgetCategory.objects.all().order_by('budget_category')]


    transaction_category_id = forms.CharField(widget=forms.HiddenInput(),
                                              required=False)

    referer = forms.CharField(widget=forms.HiddenInput(),
                              required=False)

    transaction_category = \
        forms.CharField(
            max_length=200, required=True,
            label='Transaction Category',
            widget=forms.TextInput(attrs={'class': 'form-control',
                                          'autocomplete': 'off'}))

    transaction_category_parent_id = \
        forms.ChoiceField(
            required=False,
            label='Transaction Parent Category',
            widget=forms.Select(attrs={'class': 'form-control form-large'}))

    budget_category = \
        forms.ChoiceField(
            required=True,
            label='Budget Category',
            widget=forms.Select(attrs={'class': 'form-control'}))