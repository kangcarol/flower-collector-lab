from django.shortcuts import render
# Add UdpateView & DeleteView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Flower

# # Add the Flower class & list and view function below the imports
# class Flower:  # Note that parens are optional if not inheriting from another class
#   def __init__(self, name, type, description, color):
#     self.name = name
#     self.type = type
#     self.description = description
#     self.color = color

# flowers = [
#   Flower('Camelia', 'common', 'Found in eastern and southern Asia, from the Himalayas east to Japan and Indonesia.', 'Pink'),
#   Flower('Gloriosa', 'rare', 'Native in tropical and southern Africa to Asia, and naturalised in Australia and the Pacific as well as being widely cultivated.', 'Multi-colored'),
#   Flower('Peony', 'common', 'Native to Asia, Europe and Western North America.', 'Coral'),
#   Flower('Hydrangea', 'common', 'Native to Asia and the Americas. By far the greatest species diversity is in eastern Asia, notably China, Korea, and Japan.', 'Blue')
# ]

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
  return render(request, 'flowers/detail.html', { 'flower': flower })

class FlowerCreate(CreateView):
  model = Flower
  fields = '__all__'
  # success_url = '/flowers/'

class FlowerUpdate(UpdateView):
  model = Flower
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['name', 'type','location', 'description']

class FlowerDelete(DeleteView):
  model = Flower
  success_url = '/flowers/'