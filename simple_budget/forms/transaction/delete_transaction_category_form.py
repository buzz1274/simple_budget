from django import forms
from simple_budget.models.transaction.transaction_category import \
    TransactionCategory


class DeleteTransactionCategoryForm(forms.Form):

    def __init__(self, *args, **kwargs):
        try:
            current_tc_id = kwargs.pop('current_tc_id')
        except KeyError:
            current_tc_id = False

        try:
            select_new_category = kwargs.pop('select_new_category')
        except KeyError:
            select_new_category = False

        super(DeleteTransactionCategoryForm, self).__init__(*args, **kwargs)

        self.fields['transfer_transaction_category_id'].choices = \
            [('', 'Please select a transaction category')]

        self.fields['transfer_transaction_category_id'].required = \
            select_new_category

        for o in TransactionCategory.\
            transaction_category_mapping(sort=None, budget_category_id=None)[1]:
            if (not current_tc_id or
                o.transaction_category_id != int(current_tc_id)):
                self.fields['transfer_transaction_category_id'].choices +=\
                    [(o.transaction_category_id, str(o.category))]

    transaction_category_id = forms.CharField(widget=forms.HiddenInput(),
                                              required=True)

    transfer_transaction_category_id = \
        forms.ChoiceField(
            label='Transaction Category',
            widget=forms.Select(attrs={'class': 'form-control form-large'}))

    referer = forms.CharField(widget=forms.HiddenInput(),
                              required=False)