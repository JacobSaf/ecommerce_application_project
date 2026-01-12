# orders/forms.py

from django import forms

class GuestCheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=255, label="Full name")
    email = forms.EmailField(label="Email")
    address = forms.CharField(max_length=255, label="Address")
    city = forms.CharField(max_length=100, label="City")
    state = forms.CharField(max_length=100, label="State")
    zip_code = forms.CharField(max_length=20, label="ZIP / Postal code")
    phone = forms.CharField(max_length=20, required=False, label="Phone (optional)")