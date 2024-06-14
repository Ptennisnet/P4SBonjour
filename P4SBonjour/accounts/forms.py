from django import forms


class MFAForm(forms.Form):
    code = forms.CharField(max_length=6, required=True)
