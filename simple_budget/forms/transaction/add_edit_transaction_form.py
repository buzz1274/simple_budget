# -*- coding: utf-8 -*-
from django import forms
from simple_budget.models.transaction.transaction_category import \
    TransactionCategory
import re


class AddEditTransactionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(AddEditTransactionForm, self).__init__(*args, **kwargs)

        self.fields['transaction_category_id'].choices = \
            [('', 'Please select a transaction category')] + \
            [(o.transaction_category_id, str(o.category))
             for o in TransactionCategory.
                transaction_category_mapping(sort=None,
                                             budget_category=None)[1]]

    transaction_line_id = forms.CharField(widget=forms.HiddenInput(),
                                          required=False)

    transaction_category_id = \
        forms.ChoiceField(
            required=True,
            label='Transaction Category',
            widget=forms.Select(attrs={'class': 'form-control form-large'}))

    transaction_date = \
        forms.DateField(
            required=True, input_formats=['%d %B, %Y'],
            label='Transaction Date',
            widget=forms.DateInput(format="%d %B, %Y",
                                   attrs={'class': 'form-control form-medium',
                                          'readonly': 'readonly',
                                          'autocomplete': 'off'}))

    amount = forms.CharField(
        max_length=200, required=True,
        label="Amount(£)",
        widget=forms.TextInput(attrs={'class': 'form-control form-medium',
                                      'autocomplete': 'off'}))

    def is_valid(self):
        """
        custom validation add transaction line
        """
        invalid_float_error_message = 'Please enter a valid decimal'
        valid = super(AddEditTransactionForm, self).is_valid()

        if 'amount' in self.cleaned_data and self.cleaned_data['amount']:
            try:
                float(self.cleaned_data['amount'])

                if (re.search(r'\.', self.cleaned_data['amount']) and
                    len(self.cleaned_data['amount'].rsplit('.')[-1]) != 2):
                    self._errors['amount'] = \
                        self.error_class([invalid_float_error_message])
                    valid = False
            except ValueError:
                self._errors['amount'] = \
                    self.error_class([invalid_float_error_message])
                valid = False

        return valid