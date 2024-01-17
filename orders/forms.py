from django import forms
from localflavor.ar.forms import ARPostalCodeField

from .models import Order

class OrderCreateForm(forms.ModelForm):
    postal_code = ARPostalCodeField()
    class Meta:
        model = Order
        fields = ['first_name','last_name','email','address',
                    'postal_code','postal_code','city']
        