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
  Flower('Lolo', 'tabby', 'Kinda rude.', 3),
  Flower('Sachi', 'tortoiseshell', 'Looks like a turtle.', 0),
  Flower('Fancy', 'bombay', 'Happy fluff ball.', 4),
  Flower('Bonk', 'selkirk rex', 'Meows loudly.', 6)
]

# Create your views here.
def home(request):
  return HttpResponse('<h1>Hello there!</h1>')

def about(request):
  return render(request, 'about.html')

def flowers_index(request):
  return render(request, 'flowers/index.html', { 'flowers': flowers})