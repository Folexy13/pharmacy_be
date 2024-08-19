from django import forms
from .models import Supplement, Category, SubCategory

class SupplementForm(forms.ModelForm):
    class Meta:
        model = Supplement
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            'price': forms.NumberInput(attrs={'step': 0.01}),
            'categories': forms.SelectMultiple(attrs={'class': 'select2'}),
            'subcategories': forms.SelectMultiple(attrs={'class': 'select2'}),
        }

    def __init__(self, *args, **kwargs):
        super(SupplementForm, self).__init__(*args, **kwargs)

        # Initialize empty querysets for category and subcategory
        self.fields['categories'].queryset = Category.objects.none()
        self.fields['subcategories'].queryset = SubCategory.objects.none()

        if 'main_category' in self.data:
            try:
                main_category_id = int(self.data.get('main_category'))
                self.fields['categories'].queryset = Category.objects.filter(main_category_id=main_category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['categories'].queryset = Category.objects.filter(main_category=self.instance.main_category)

        if 'categories' in self.data:
            try:
                # Expect multiple category ids, handle them correctly
                category_ids = self.data.getlist('categories')
                self.fields['subcategories'].queryset = SubCategory.objects.filter(category__in=category_ids)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategories'].queryset = SubCategory.objects.filter(
                category__in=self.instance.categories.all()
            )

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise forms.ValidationError('The price must be greater than zero.')
        return price
