from django.db import models


class Pattern(models.Model):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    pattern = models.TextField()

    def __str__(self):
        return self.name


class Alert(models.Model):
    message = models.TextField()
    content = models.TextField(null=True, blank=True)
    channel = models.TextField()
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE)

    def __str__(self):
        return self.message
