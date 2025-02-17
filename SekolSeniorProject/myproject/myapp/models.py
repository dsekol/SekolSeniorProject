from django.db import models

# Create your models here.

class YourModel(models.Model):
    name = models.CharField(max_length=100)


class AllenStreet(models.Model):
    document = models.CharField(max_length=255)
    north_of = models.CharField(max_length=255)
    south_of = models.CharField(max_length=255)
    no = models.CharField(max_length=255)
    h = models.CharField(max_length=255)
    rel_to_head = models.CharField(max_length=255)
    no_mem = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    given_name = models.CharField(max_length=255)
    nativity = models.CharField(max_length=255)
    sex = models.CharField(max_length=10)
    born = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    arrived = models.CharField(max_length=255)
    years_in_usa = models.CharField(max_length=255)
    cit_al = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    business = models.CharField(max_length=255)
    comment = models.TextField()