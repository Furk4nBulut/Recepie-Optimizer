from django import forms
from .models import RecipeStep

class RecipeStepForm(forms.ModelForm):
    class Meta:
        model = RecipeStep
        fields = ['name', 'duration', 'occupies_chef', 'prerequisites']
        widgets = {
            'prerequisites': forms.CheckboxSelectMultiple(),
        }
