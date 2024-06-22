import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)


    class Meta:
            ordering = ('title',)
            verbose_name = 'category'
            verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('movie_app:movie_by_category', args=[self.slug])

    def __str__(self):
        return '{}'.format(self.title)


class Movies(models.Model):
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    poster = models.ImageField(upload_to="movies", blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    release_date = models.DateField()
    available = models.BooleanField(default=True)
    actors=models.CharField(max_length=255)
    youtube_link=models.URLField()
    averageRating=models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + '-' + str(uuid.uuid4())
        super(Movies, self).save(*args, **kwargs)
    class Meta:
        ordering = ('title',)
        verbose_name = 'movie'
        verbose_name_plural = 'movies'



    def get_url(self):
        return reverse('movie_app:details', args=[self.id])

    def __str__(self):
        return '{}'.format(self.title)
class Review(models.Model):
    movies=models.ForeignKey(Movies,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    comment=models.TextField(max_length=1000)
    rating=models.FloatField(default=0)


    def __str__(self):
        return self.user.username
