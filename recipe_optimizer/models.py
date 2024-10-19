from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    duration = models.PositiveIntegerField()  # Adım süresi (dakika)
    occupies_chef = models.BooleanField(default=True)  # Şefi meşgul ediyor mu?
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)  # Önceki adımlar

    def __str__(self):
        return f"{self.name} - {self.recipe.name}"
