from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('advices/', views.advice_list, name='advice_list'),
    path('advices/write/', views.advice_write, name='advice_write'),
    path('advices/<int:advice_id>/edit/', views.advice_edit, name='advice_edit'),
    path('advices/<int:advice_id>/', views.advice_detail, name='advice_detail'),
    path('advices/<int:advice_id>/delete/', views.advice_delete, name='advice_delete'),
    path('advices/<int:advice_id>/like/', views.advice_like, name='advice_like'),
    path('advices/<int:advice_id>/scrap/', views.advice_scrap, name='advice_scrap'),
]