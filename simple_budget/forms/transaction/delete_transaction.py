# -*- coding: utf-8 -*-
from django import forms


class DeleteTransactionForm(forms.Form):

    transaction_line_id = forms.CharField(widget=forms.HiddenInput(),
                                          required=True)

    referer = forms.CharField(widget=forms.HiddenInput(),
                              required=False)