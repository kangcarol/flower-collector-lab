from django.urls import path
from . import views

urlpatterns = [
  # localhost:8000/
  path('', views.Home.as_view(), name='home'),
  # localhost:8000/about
  path('about/', views.about ,name='about'),
  # localhost:8000/flowers
  path('flowers/', views.flowers_index ,name='flowers_index'),
  # localhost:8000/flowers/int:flower_id
  path('flowers/<int:flower_id>/', views.flowers_detail, name='flowers_detail'),
  # new route used to show a form and create a flower
  path('flowers/create/', views.FlowerCreate.as_view(), name='flowers_create'),
  # new route used to update a flower
  path('flowers/<int:pk>/update/', views.FlowerUpdate.as_view(), name='flowers_update'),
  # new route used to delete a flower
  path('flowers/<int:pk>/delete/', views.FlowerDelete.as_view(), name='flowers_delete'),
  path('flowers/<int:flower_id>/add_care/', views.add_care, name='add_care'),
    # associate a toy with a cat (M:M)
  path('flowers/<int:flower_id>/assoc_garden/<int:garden_id>/', views.assoc_garden, name='assoc_garden'),
  path('gardens/create/', views.GardenCreate.as_view(), name='gardens_create'),
  path('gardens/<int:pk>/', views.GardenDetail.as_view(), name='gardens_detail'),
  path('gardens/', views.GardenList.as_view(), name='gardens_index'),
  path('gardens/<int:pk>/update/', views.GardenUpdate.as_view(), name='gardens_update'),
  path('gardens/<int:pk>/delete/', views.GardenDelete.as_view(), name='gardens_delete'),
  path('accounts/signup/', views.signup, name='signup'),
  path('flowers/<int:flower_id>/add_photo/', views.add_photo, name='add_photo'),
]
