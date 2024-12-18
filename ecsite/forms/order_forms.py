from django import forms
from ecsite.models.order import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'last_name',
            'first_name',
            'username',
            'email',
            'address',
            'address2',
            'country',
            'state',
            'zip_code',
            'card_name',
            'card_number',
            'card_expiration',
            'card_cvv',
        ]
        widgets = {
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'address2': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'country': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'state': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'card_name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'card_number': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'card_expiration': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'MM/YY',
            }),
            'card_cvv': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['country'].widget.choices = [
            ('', '選択してください'),
            ('日本', '日本'),
        ]

        self.fields['state'].widget.choices = [
            ('', '選択してください'),
            ('北海道', '北海道'),
            ('東京都', '東京都'),
            ('大阪府', '大阪府'),
            ('神奈川県', '神奈川県'),
            ('埼玉県', '埼玉県'),
            ('千葉県', '千葉県'),
            ('愛知県', '愛知県'),
            ('福岡県', '福岡県'),
        ]

    def clean_card_expiration(self):
        expiration = self.cleaned_data.get('card_expiration')
        if expiration:
            if not '/' in expiration:
                raise forms.ValidationError('有効期限は MM/YY の形式で入力してください')
            try:
                month, year = expiration.split('/')
                if not (1 <= int(month) <= 12 and len(year) == 2):
                    raise forms.ValidationError('有効期限の形式が正しくありません')
            except ValueError:
                raise forms.ValidationError('有効期限の形式が正しくありません')
        return expiration

    def clean_card_number(self):
        number = self.cleaned_data.get('card_number')
        if number:
            if not number.isdigit():
                raise forms.ValidationError('カード番号は数字のみを入力してください')
            if not len(number) == 16:
                raise forms.ValidationError('カード番号は16桁で入力してください')
        return number

    def clean_card_cvv(self):
        cvv = self.cleaned_data.get('card_cvv')
        if cvv:
            if not cvv.isdigit():
                raise forms.ValidationError('セキュリティコードは数字のみを入力してください')
            if not len(cvv) in [3, 4]:
                raise forms.ValidationError('セキュリティコードは3桁または4桁で入力してください')
        return cvv
