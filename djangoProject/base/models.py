from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name
