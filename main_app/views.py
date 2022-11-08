from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .models import Flower, Garden
from .forms import CareForm

# Create your views here.
class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

@login_required
def flowers_index(request):
  flowers = Flower.objects.filter(user=request.user)
  return render(request, 'flowers/index.html', { 'flowers': flowers })

@login_required
def flowers_detail(request, flower_id):
  flower = Flower.objects.get(id=flower_id)
  gardens_not_planted_in = Garden.objects.exclude(id__in = flower.gardens.all().values_list('id'))
  care_form = CareForm()
  return render(request, 'flowers/detail.html', {
    'flower': flower, 'care_form': care_form, 'gardens' : gardens_not_planted_in
  })

class FlowerCreate(LoginRequiredMixin, CreateView):
  model = Flower
  fields = ['name', 'type', 'location', 'description']

  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)

class FlowerUpdate(LoginRequiredMixin, UpdateView):
  model = Flower
  fields = ['name', 'type','location', 'description']

class FlowerDelete(LoginRequiredMixin, DeleteView):
  model = Flower
  success_url = '/flowers/'

@login_required
def add_care(request, flower_id):
  form = CareForm(request.POST)
  if form.is_valid():
    new_care = form.save(commit=False)
    new_care.flower_id = flower_id
    new_care.save()
  return redirect('flowers_detail', flower_id=flower_id)

class GardenCreate(LoginRequiredMixin, CreateView):
  model = Garden
  fields = '__all__'

class GardenList(LoginRequiredMixin, ListView):
  model = Garden

class GardenDetail(LoginRequiredMixin, DetailView):
  model = Garden

class GardenUpdate(LoginRequiredMixin, UpdateView):
  model = Garden
  fields = ['name', 'location']

class GardenDelete(LoginRequiredMixin, DeleteView):
  model = Garden
  success_url = '/gardens/'

@login_required
def assoc_garden(request, flower_id, garden_id):
  # Note that you can pass a garden's id instead of the whole object
  Flower.objects.get(id=flower_id).gardens.add(garden_id)
  return redirect('flowers_detail', flower_id=garden_id) 

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in
      login(request, user)
      return redirect('flowers_index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)
  # Same as: return render(request, 'signup.html', {'form': form, 'error_message': error_message})