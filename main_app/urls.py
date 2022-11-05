from django.urls import path
from . import views


urlpatterns = [
  # localhost:8000/
  path('', views.home, name='home'),
  # localhost:8000/about
  path('about/', views.about ,name='about'),
  # localhost:8000/flowers
  path('flowers/', views.flowers_index ,name='flowers_index'),
  # localhost:8000/flowers/int:flower_id
  path('flowers/<int:flower_id>/', views.flowers_detail, name='flowers_detail'),
  # new route used to show a form and create a flower
  path('flowers/create/', views.FlowerCreate.as_view(), name='flowers_create'),
]
