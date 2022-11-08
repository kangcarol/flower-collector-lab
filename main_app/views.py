from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Flower, Garden
from .forms import CareForm

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def flowers_index(request):
  flowers = Flower.objects.all()
  return render(request, 'flowers/index.html', { 'flowers': flowers })

def flowers_detail(request, flower_id):
  flower = Flower.objects.get(id=flower_id)
  gardens_not_planted_in = Garden.objects.exclude(id__in = flower.gardens.all().values_list('id'))
  care_form = CareForm()
  return render(request, 'flowers/detail.html', {
    'flower': flower, 'care_form': care_form, 'gardens' : gardens_not_planted_in
  })

class FlowerCreate(CreateView):
  model = Flower
  fields = ['name', 'type', 'location', 'description']
  # success_url = '/flowers/'

class FlowerUpdate(UpdateView):
  model = Flower
  fields = ['name', 'type','location', 'description']

class FlowerDelete(DeleteView):
  model = Flower
  success_url = '/flowers/'

def add_care(request, flower_id):
  form = CareForm(request.POST)
  if form.is_valid():
    new_care = form.save(commit=False)
    new_care.flower_id = flower_id
    new_care.save()
  return redirect('flowers_detail', flower_id=flower_id)

class GardenCreate(CreateView):
  model = Garden
  fields = '__all__'

class GardenList(ListView):
  model = Garden

class GardenDetail(DetailView):
  model = Garden

class GardenUpdate(UpdateView):
  model = Garden
  fields = ['name', 'location']

class GardenDelete(DeleteView):
  model = Garden
  success_url = '/gardens/'

def assoc_garden(request, flower_id, garden_id):
  # Note that you can pass a garden's id instead of the whole object
  Flower.objects.get(id=flower_id).gardens.add(garden_id)
  return redirect('flowers_detail', flower_id=garden_id) 