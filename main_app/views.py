from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .models import Flower, Garden, Photo
from .forms import CareForm
import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'carolkang-the-botanists-library'

# Create your views here.
class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

@login_required
  # flowers = Flower.objects.filter(user=request.user)
def flowers_index(request):
  flowers = Flower.objects.all()
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
    form.instance.user = self.request.user  # form.instance is the flower
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

def add_photo(request, flower_id):
  # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
		# uuid.uuid4().hex generates a random hexadecimal Universally Unique Identifier
    # Add on the file extension using photo_file.name[photo_file.name.rfind('.'):]
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      # build the full url string
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      # we can assign to flower_id or flower (if you have a flower object)
      photo = Photo(url=url, flower_id=flower_id)
      # Remove old photo if it exists
      flower_photo = Photo.objects.filter(flower_id=flower_id)
      if flower_photo.first():
        flower_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('flowers_detail', flower_id=flower_id)