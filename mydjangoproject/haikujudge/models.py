from django.db import models

# Create your models here.

class Haiku(models.Model):
    content = models.TextField()
    author = models.CharField(max_length=20)
    score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.content