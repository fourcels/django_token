from django.db import models

# Create your models here.


class Hero(models.Model):
    name = models.CharField('名字', max_length=60)
    alias = models.CharField('别名', max_length=60)

    def __str__(self):
        return self.name
