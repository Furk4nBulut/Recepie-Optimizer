from django import forms
from .models import Recipe, RecipeStep

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description']




class RecipeStepForm(forms.ModelForm):
    class Meta:
        model = RecipeStep
        fields = ['name', 'duration', 'occupies_chef', 'prerequisites']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter step name',
                'required': 'required'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duration in minutes',
                'min': '1',
                'required': 'required'
            }),
            'occupies_chef': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'prerequisites': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'multiple': 'multiple'
            }),
        }

    def __init__(self, recipe=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if recipe is not None:
            self.fields['prerequisites'].queryset = RecipeStep.objects.filter(recipe=recipe)
        self.fields['occupies_chef'].label = "Requires Chef"  # Checkbox label
        self.fields['prerequisites'].label = "Prerequisites"  # Dropdown label
