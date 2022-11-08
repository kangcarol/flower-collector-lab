from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

CARE = (
  ('W', 'Water'),
  ('F', 'Fertilizer'),
  ('R', 'Repotting')
)

class Garden(models.Model):
  name = models.CharField(max_length=50)
  location = models.CharField(max_length=20)

  class Meta:
    ordering = ['name']

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('gardens_detail', kwargs={'pk': self.id})

  def save(self, *args, **kwargs):
    for field_name in ['name', 'location']:
      val = getattr(self, field_name, False)
      if val:
        setattr(self, field_name, val.upper())
    super(Garden, self).save(*args, **kwargs)

class Flower(models.Model):
  name = models.CharField(max_length=100)
  type = models.CharField(max_length=100)
  location = models.TextField(max_length=250)
  description = models.TextField(max_length=250)
    # Add the M:M relationship
  gardens = models.ManyToManyField(Garden)
    # Add the foreign key linking to a user instance
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  
  class Meta:
    ordering = ['name']

  def __str__(self):
    return self.name

  # Add this class method
  def get_absolute_url(self):
    return reverse('flowers_detail', kwargs={'flower_id': self.id})

  def care_for_month(self):
    return self.care_set.filter(date=date.month.today()).count() >= len(CARE)

  def save(self, *args, **kwargs):
    for field_name in ['name']:
      val = getattr(self, field_name, False)
      if val:
        setattr(self, field_name, val.upper())
    super(Flower, self).save(*args, **kwargs)

class Care(models.Model):
  date = models.DateField('Date')
  care = models.CharField(
    max_length=1,
    choices=CARE,
    default=CARE[0][0]
  )

  flower = models.ForeignKey(Flower, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.get_care_display()} on {self.date}"

  class Meta:
    ordering = ['-date']

    
