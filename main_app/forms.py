from django.forms import ModelForm
from .models import Care

class CareForm(ModelForm):
  class Meta:
    model = Care
    fields = ['date', 'care']