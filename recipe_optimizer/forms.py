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

    def __init__(self, *args, **kwargs):
        recipe = kwargs.pop('recipe')  # Extract the recipe from kwargs
        super().__init__(*args, **kwargs)
        self.fields['occupies_chef'].label = "Requires Chef"  # Checkbox label
        self.fields['prerequisites'].label = "Prerequisites"  # Dropdown label

        # Filter prerequisites to only show those related to the given recipe
        self.fields['prerequisites'].queryset = RecipeStep.objects.filter(recipe=recipe)
