from django.db import models

class Recipe(models.Model):
    """
    Model representing a recipe.

    :param name: The name of the recipe (max length: 200 characters).
    :param description: A detailed description of the recipe.
    :param created_at: The timestamp when the recipe was created (automatically added).
    :returns: A Recipe instance representing a cooking recipe.
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        :returns: The name of the recipe as a string representation.
        """
        return self.name


class RecipeStep(models.Model):
    """
    Model representing a step in a recipe.

    :param recipe: ForeignKey linking the step to a specific recipe.
    :param name: The name of the step (max length: 200 characters).
    :param duration: The duration of the step in minutes.
    :param occupies_chef: Boolean indicating if the step occupies the chef.
    :param prerequisites: Many-to-many relationship for prerequisites, linking to other steps.
    :returns: A RecipeStep instance representing a single step within a recipe.
    """
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    duration = models.PositiveIntegerField()
    occupies_chef = models.BooleanField(default=True)
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        """
        :returns: A string representation combining the step name and associated recipe name.
        """
        return f"{self.name} - {self.recipe.name}"
