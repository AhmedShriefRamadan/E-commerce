from django import forms
from django.utils.translation import gettext_lazy as _

PPRODUCT_QUANTITY_CHOCIES = [(i, str(i)) for i in range(1,21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PPRODUCT_QUANTITY_CHOCIES,
        coerce=int,
        label=_('Quantity')
    )
    override = forms.BooleanField(required=False,
                                    initial=False,
                                    widget=forms.HiddenInput)