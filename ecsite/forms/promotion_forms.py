from django import forms
from ecsite.models.promotion import PromotionCode


class PromotionCodeForm(forms.Form):
    code = forms.CharField(
        max_length=7,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'プロモーションコード'
        })
    )

    def clean_code(self):
        code = self.cleaned_data.get('code')
        try:
            promotion = PromotionCode.objects.get(code=code, is_used=False)
            return code
        except PromotionCode.DoesNotExist:
            raise forms.ValidationError('無効なプロモーションコードです')
