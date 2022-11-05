from django.db import models
from django.urls import reverse

class Flower(models.Model):
  name = models.CharField(max_length=100)
  type = models.CharField(max_length=100)
  location = models.TextField(max_length=250)
  description = models.TextField(max_length=250)

  def __str__(self):
    return self.name

  # Add this class method
  def get_absolute_url(self):
    return reverse('flowers_detail', kwargs={'flower_id': self.id})