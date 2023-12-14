from django import forms

# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ('first_name', 'last_name', 'address', 'zipcode', 'city',)
        
class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your coupon code',
    }))