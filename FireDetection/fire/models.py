from django.db import models

# Create your models here.

class Interfaces(models.Model):
    name = models.CharField(max_length=20, unique=True)
    url = models.URLField("接口地址", max_length=200)
    desc = models.CharField("描述", max_length=500, blank=True)

    def __str__(self):
        return self.name
    