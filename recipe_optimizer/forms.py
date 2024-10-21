from django import forms
from .models import Recipe, RecipeStep


class RecipeForm(forms.ModelForm):
    """
    A form for creating and editing Recipe objects.

    :param name: Name of the recipe.
    :param description: Short description of the recipe.
    :returns: A form instance for creating or editing a Recipe object.
    :raises ValidationError: Raises validation error if data is invalid.
    """

    class Meta:
        model = Recipe
        fields = ['name', 'description']


class RecipeStepForm(forms.ModelForm):
    """
    A form for creating and editing RecipeStep objects.

    :param name: Name of the step.
    :param duration: Duration of the step in minutes.
    :param occupies_chef: Boolean indicating if the step requires the chef.
    :param prerequisites: Multiple checkbox input for selecting prerequisite steps from the same recipe.
    :returns: A form instance for creating or editing a RecipeStep object.
    :raises ValidationError: Raises validation error if data is invalid.

    Custom Widgets:
    - Name field with a text input and placeholder.
    - Duration field with a number input, minimum value of 1, and placeholder.
    - Occupies chef field with a checkbox input.
    - Prerequisites field with multiple checkboxes for selecting prerequisite steps.
    """

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
            'prerequisites': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check'
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Initializes the form with the provided recipe.

        :param recipe: The recipe instance to filter prerequisites by.
        :returns: A RecipeStepForm instance with customized field labels and prerequisite filtering.
        :raises KeyError: Raises if 'recipe' is not provided in kwargs.
        """
        recipe = kwargs.pop('recipe')  # Extract the recipe from kwargs
        super().__init__(*args, **kwargs)
        self.fields['occupies_chef'].label = "Requires Chef"  # Checkbox label
        self.fields['prerequisites'].label = "Prerequisites"  # Checkbox label

        # Filter prerequisites to only show those related to the given recipe
        self.fields['prerequisites'].queryset = RecipeStep.objects.filter(recipe=recipe)
