from django import forms
from simple_budget.models.budget.budget_category import BudgetCategory


class DeleteBudgetCategoryForm(forms.Form):

    def __init__(self, *args, **kwargs):
        try:
            current_budget_category_id = kwargs.pop('current_budget_category_id')
        except KeyError:
            current_budget_category_id = False

        try:
            select_new_category = kwargs.pop('select_new_category')
        except KeyError:
            select_new_category = False

        super(DeleteBudgetCategoryForm, self).__init__(*args, **kwargs)

        self.fields['transfer_budget_category_id'].choices = \
            [('', 'Please select a budget category')]

        self.fields['transfer_budget_category_id'].required = \
            select_new_category

        for o in BudgetCategory.objects.exclude(
                    budget_category_id=current_budget_category_id).\
                order_by('budget_category'):
            if (not current_budget_category_id or
                o.budget_category_id != int(current_budget_category_id)):
                self.fields['transfer_budget_category_id'].choices +=\
                    [(o.budget_category_id, str(o.budget_category))]

    budget_category_id = forms.CharField(widget=forms.HiddenInput(),
                                              required=True)

    transfer_budget_category_id = \
        forms.ChoiceField(
            label='Budget Category',
            widget=forms.Select(attrs={'class': 'form-control form-large'}))

    referer = forms.CharField(widget=forms.HiddenInput(),
                              required=False)