from django.core import validators
from django.db import models

from django_countries.fields import CountryField


class BreedGroup(models.Model):
    name = models.CharField(max_length=64, blank=False, unique=True)
    country_of_origin = CountryField(blank=True)

    def __str__(self):
        return self.name


class Breed(models.Model):
    SIZE_CHOICES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('G', 'Giant')
    )

    name = models.CharField(max_length=64, blank=False, unique=True)
    slug = models.SlugField()
    blurb = models.CharField(max_length=512, blank=True, default=u'')
    intro = models.TextField(default=u'')
    sample_photo = models.URLField(blank=True, default='http://via.placeholder.com/350x150')
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, default='S')
    group = models.ForeignKey(BreedGroup, blank=True, null=True)

    def __str__(self):
        return self.name


class DogBreedRelationship(models.Model):
    breed = models.ForeignKey(Breed, related_name='dog_relations')
    dog = models.ForeignKey('Dog', related_name='breed_relations')
    percent = models.PositiveIntegerField(
        default=100,
        validators=[
            validators.MaxValueValidator(100),
            validators.MinValueValidator(1)]
    )


class Dog(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    date_of_birth = models.DateField(null=True)
    photo = models.URLField(blank=True, default='http://via.placeholder.com/350x150')
    breeds = models.ManyToManyField(
        Breed,
        related_name='dogs',
        through=DogBreedRelationship,
        blank=True
    )

    def __str__(self):
        return self.name


class Post(models.Model):
    headline = models.CharField(max_length=512, blank=False, null=False)
    body = models.TextField(blank=True, default=u'')
    dogs_mentioned = models.ManyToManyField(Dog, related_name='posts', blank=True)

    def __str__(self):
        return self.headline
