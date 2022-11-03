from django.shortcuts import render

from django.http import HttpResponse

# Add the Flower class & list and view function below the imports
class Flower:  # Note that parens are optional if not inheriting from another class
  def __init__(self, name, type, description, color):
    self.name = name
    self.type = type
    self.description = description
    self.color = color

flowers = [
  Flower('Camelia', 'common', '', 'Pink'),
  Flower('Gloriosa', 'rare', '', 'Multi-colored'),
  Flower('Peony', 'common', '', 'Coral'),
  Flower('Hydrangea', 'common', '', 'Blue')
]

# Create your views here.
def home(request):
  return HttpResponse('<h1>Hello there!</h1>')

def about(request):
  return render(request, 'about.html')

def flowers_index(request):
  return render(request, 'flowers/index.html', { 'flowers': flowers})