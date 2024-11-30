from django import forms
from .models import Product, ProductImage


class ModelFormWithFormSetMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formset = self.formset_class(
            instance=self.instance,
            data=self.data if self.is_bound else None,
            files=self.files if self.is_bound else None,
        )

    def is_valid(self):
        form_valid = super().is_valid()
        formset_valid = self.formset.is_valid()

        if not formset_valid:
            for form in self.formset:
                for field, errors in form.errors.items():
                    self.add_error(None, f"{field}: {
                                   ', '.join(str(e) for e in errors)}")

        return form_valid and formset_valid

    def save(self, commit=True):
        saved_instance = super().save(commit)
        self.formset.save(commit)
        return saved_instance


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'image_alt']

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        image_alt = cleaned_data.get('image_alt', '').strip()

        if not image:
            cleaned_data['image_alt'] = Product.DEFAULT_IMAGE_ALT
        elif not image_alt:
            self.add_error('image_alt', '画像が設定されている場合は、代替テキストを入力してください。')
        elif image_alt == Product.DEFAULT_IMAGE_ALT:
            self.add_error('image_alt', '画像を設定する場合は、適切な代替テキストを入力してください。')

        return cleaned_data


ProductImageFormSet = forms.inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    can_delete=False,
    extra=1,
    max_num=1,
)


class ProductForm(ModelFormWithFormSetMixin, forms.ModelForm):
    formset_class = ProductImageFormSet

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']
