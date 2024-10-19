from django.db import models

class RecipeStep(models.Model):
    name = models.CharField(max_length=200)
    duration = models.PositiveIntegerField()  # Adım süresi (dakika)
    occupies_chef = models.BooleanField(default=True)  # Şefi meşgul ediyor mu?
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)  # Önceki adımlar

    def __str__(self):
        return self.name
