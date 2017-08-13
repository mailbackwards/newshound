from django.core import validators
from django.db import models
from django.urls import reverse

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
    group = models.ForeignKey(BreedGroup, blank=True, null=True, related_name='breeds')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


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
    is_good = models.BooleanField(default=True)
    breeds = models.ManyToManyField(
        Breed,
        related_name='dogs',
        through=DogBreedRelationship,
        blank=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('admin:newshound_dog_change', args=[self.pk])

    class Meta:
        ordering = ('name',)


class Post(models.Model):
    PUB_STATUS_DRAFT = 'D'
    PUB_STATUS_EDIT = 'E'
    PUB_STATUS_PUBLISHED = 'P'
    PUB_STATUS_CHOICES = (
        (PUB_STATUS_DRAFT, 'Draft'),
        (PUB_STATUS_EDIT, 'Edit'),
        (PUB_STATUS_PUBLISHED, 'Published')
    )

    headline = models.CharField(max_length=512, blank=False, null=False)
    pub_date = models.DateTimeField('Publication date', auto_now_add=True)
    publication_status = models.CharField(max_length=1,
        choices=PUB_STATUS_CHOICES, default=PUB_STATUS_DRAFT)
    body = models.TextField(blank=True, default=u'')
    dogs_mentioned = models.ManyToManyField(Dog, related_name='posts', blank=True)

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse('admin:newshound_post_change', args=[self.pk])

    class Meta:
        ordering = ('-pub_date',)
