from django.db import models


class Foo(models.Model):
    name = models.CharField(null=False, blank=False, max_length=64)
    age = models.IntegerField(null=False)
