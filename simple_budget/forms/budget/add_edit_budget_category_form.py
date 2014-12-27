from django import forms
from simple_budget.models.budget.budget_type import BudgetType


class AddEditBudgetCategoryForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(AddEditBudgetCategoryForm, self).__init__(*args, **kwargs)

        self.fields['budget_type_id'].choices = \
            [('', 'Please select a budget type')] + \
            [(str(o.budget_type_id), str(o.budget_type))
             for o in BudgetType.objects.all().order_by('ordering')]


    budget_category_id = forms.CharField(widget=forms.HiddenInput(),
                                         required=False)

    referer = forms.CharField(widget=forms.HiddenInput(),
                              required=False)

    budget_category = \
        forms.CharField(
            label="Budget Catgeory",
            max_length=200, required=True,
            widget=forms.TextInput(attrs={'class': 'form-control',
                                          'autocomplete': 'off'}))

    budget_type_id = \
        forms.ChoiceField(
            label="Budget Type",
            required=True,
            widget=forms.Select(attrs={'class': 'form-control'}))