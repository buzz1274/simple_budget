from django import forms
from simple_budget.models.budget import Budget


class AddEditBudgetForm(forms.Form):

    def __init__(self, *args, **kwargs):
        try:
            transactions = kwargs.pop('transactions')
        except KeyError:
            transactions = False

        try:
            edit_budget = kwargs.pop('edit_budget')
        except KeyError:
            edit_budget = False

        super(AddEditBudgetForm, self).__init__(*args, **kwargs)

        if transactions:
            for transaction in transactions:
                field_id = "budget_category_%s" % \
                           (transaction.budget_category_id,)

                self.fields[field_id] = \
                    forms.CharField(
                        max_length=8, required=False,
                        widget=forms.HiddenInput(attrs=
                            {'id':field_id,
                             'class': 'budget_category_hidden'}))

                if edit_budget:
                    self.fields[field_id].initial = transaction.budget_amount

                    field_id = "budget_category_%s_future" % \
                               (transaction.budget_category_id,)

                    self.fields[field_id] = \
                        forms.CharField(
                            max_length=8, required=False,
                            widget=forms.HiddenInput(attrs=
                                                     {'id':field_id,
                                                      'class': 'budget_category_hidden'}))

                    self.fields[field_id].initial = \
                        transaction.budget_amount_future

    budget_id = forms.CharField(widget=forms.HiddenInput(),
                                required=False)

    referer = forms.CharField(widget=forms.HiddenInput(),
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

    budget_master = forms.BooleanField(label="Master", required=False)

    def clean_budget_master(self):
        """
        ensure only one budget is flagged as master
        :return:
        """
        budget_master = self.cleaned_data['budget_master']
        budget_id = self.cleaned_data['budget_id']

        if budget_master:
            master_budget = Budget.objects.filter(budget_master=True)

            if (master_budget and
                (not budget_id or
                 int(budget_id) != master_budget[0].budget_id)):
                raise forms.ValidationError(
                    "Another budget is already flagged as master.")

